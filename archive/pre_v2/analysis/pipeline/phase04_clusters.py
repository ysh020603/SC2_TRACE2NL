"""Phase 4: race-global and matchup strategy discovery (plan.md §7–8)."""

from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.cluster import HDBSCAN, AgglomerativeClustering
from sklearn.metrics import adjusted_rand_score, pairwise_distances, silhouette_score
from sklearn.preprocessing import StandardScaler

from analysis.pipeline.io_utils import PRIMARY_HORIZON, ensure_dir, write_json

META_COLS = {
    "replay_id",
    "player_id",
    "race",
    "opponent_race",
    "matchup_dir",
    "result",
    "mmr",
    "mmr_diff",
    "map_name",
    "version",
    "base_build",
    "region",
    "horizon",
    "opening_observed_to",
    "early_terminated",
    "key_sequence",
}


def _feature_matrix(df: pd.DataFrame) -> tuple[np.ndarray, list[str]]:
    cols = []
    for c in df.columns:
        if c in META_COLS:
            continue
        if c.endswith("_z") or c.endswith("_observed") or c.startswith("path_") or c.startswith("ng_"):
            cols.append(c)
        elif c.startswith("idx_"):
            cols.append(c)
    # prefer scaled timing if present
    use = []
    seen_base = set()
    for c in cols:
        if c.endswith("_time") and f"{c}_z" in df.columns:
            continue
        if c.startswith("ordered_") and f"{c}_z" in df.columns:
            continue
        use.append(c)
    X = df[use].fillna(0.0).to_numpy(dtype=np.float64)
    # replace inf
    X[~np.isfinite(X)] = 0.0
    return X, use


def _cluster_one(X: np.ndarray, min_cluster_size: int, min_samples: int) -> np.ndarray:
    n = X.shape[0]
    if n < max(4, min_cluster_size):
        return np.zeros(n, dtype=int)
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)
    model = HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=min_samples,
        metric="euclidean",
        cluster_selection_method="eom",
        copy=True,
        n_jobs=-1,
    )
    labels = model.fit_predict(Xs)
    n_clusters = len(set(labels) - {-1})
    if n_clusters >= 2:
        return labels
    # fallback for tiny samples: agglomerative into k≈sqrt(n)/2
    k = max(2, min(6, int(round(np.sqrt(n) / 1.5))))
    k = min(k, n // 3 if n >= 6 else 2)
    if k < 2:
        return np.zeros(n, dtype=int)
    agg = AgglomerativeClustering(n_clusters=k, linkage="ward")
    return agg.fit_predict(Xs)


def _bootstrap_stability(
    X: np.ndarray,
    labels: np.ndarray,
    min_cluster_size: int,
    min_samples: int,
    repeats: int | None = None,
    seed: int = 42,
) -> dict[str, Any]:
    rng = np.random.default_rng(seed)
    n = X.shape[0]
    if n < 8 or len(set(labels) - {-1}) < 1:
        return {"repeats": 0, "mean_ari": None, "per_cluster_stability": {}}

    # Full-n bootstrap is too expensive at ~50k+/race; subsample for stability.
    if repeats is None:
        repeats = 5 if n >= 5000 else 10
    sample_size = min(n, 8000 if n >= 5000 else n)

    aris = []
    member_hits: dict[int, list[float]] = defaultdict(list)
    for bi in range(repeats):
        print(f"  bootstrap {bi+1}/{repeats} sample_size={sample_size}", flush=True)
        idx = rng.choice(n, size=sample_size, replace=True)
        uniq = np.unique(idx)
        if len(uniq) < max(4, min_cluster_size):
            continue
        # scale min_cluster_size to subsample
        mcs = max(20, int(min_cluster_size * sample_size / max(n, 1)))
        ms = max(5, min(mcs // 5, min_samples))
        lab_b = _cluster_one(X[uniq], mcs, ms)
        # map bootstrap labels back via ARI on overlapping points
        base = labels[uniq]
        # filter noise for ARI if both have clusters
        mask = (base >= 0) & (lab_b >= 0)
        if mask.sum() >= 4 and len(set(base[mask])) > 1 and len(set(lab_b[mask])) > 1:
            aris.append(float(adjusted_rand_score(base[mask], lab_b[mask])))
        # per-cluster co-membership stability
        for c in set(base) - {-1}:
            members = np.where(base == c)[0]
            if len(members) < 2:
                continue
            # among sampled members, fraction sharing majority bootstrap label
            sampled_pos = [i for i, u in enumerate(uniq) if base[i] == c]
            if len(sampled_pos) < 2:
                continue
            labs = lab_b[sampled_pos]
            labs = labs[labs >= 0]
            if len(labs) == 0:
                member_hits[int(c)].append(0.0)
            else:
                maj = Counter(labs).most_common(1)[0][1] / len(labs)
                member_hits[int(c)].append(float(maj))

    per = {
        str(c): float(np.mean(v)) if v else None for c, v in sorted(member_hits.items())
    }
    return {
        "repeats": repeats,
        "mean_ari": float(np.mean(aris)) if aris else None,
        "per_cluster_stability": per,
    }


def _medoid_indices(X: np.ndarray, labels: np.ndarray, max_sample: int = 1500) -> dict[int, int]:
    medoids = {}
    rng = np.random.default_rng(0)
    for c in sorted(set(labels) - {-1}):
        idx = np.where(labels == c)[0]
        if len(idx) == 0:
            continue
        if len(idx) > max_sample:
            sample = rng.choice(idx, size=max_sample, replace=False)
        else:
            sample = idx
        D = pairwise_distances(X[sample])
        medoids[int(c)] = int(sample[int(np.argmin(D.mean(axis=1)))])
    return medoids


def _enrichment(df: pd.DataFrame, labels: np.ndarray, feature_cols: list[str]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for c in sorted(set(labels) - {-1}):
        mask = labels == c
        base_mask = labels >= 0
        items = []
        for col in feature_cols:
            if not (col.startswith("path_") or col.endswith("_observed") or col.startswith("ng_")):
                continue
            p_s = float(df.loc[mask, col].mean())
            p_b = float(df.loc[base_mask, col].mean()) if base_mask.any() else 0.0
            if p_b <= 0:
                rr = None
            else:
                rr = p_s / p_b
            if p_s >= 0.35 and rr is not None and rr >= 1.25:
                items.append({"feature": col, "cluster_rate": p_s, "baseline_rate": p_b, "risk_ratio": rr})
        items.sort(key=lambda x: (-(x["risk_ratio"] or 0), -x["cluster_rate"]))
        out[str(c)] = items[:12]
    return out


def run_phase04(features_path: Path, out_dir: Path) -> dict[str, Any]:
    ensure_dir(out_dir)
    df_all = pd.read_parquet(features_path)
    # clustering uses only fully observed openings at primary horizon
    df = df_all.loc[df_all["opening_observed_to"]].reset_index(drop=True)

    global_rows = []
    matchup_rows = []
    stability_rows = []
    representatives: dict[str, Any] = {}
    enrich_all: dict[str, Any] = {}

    race_prefix = {"Protoss": "P", "Terran": "T", "Zerg": "Z"}

    for race, g in df.groupby("race"):
        g = g.reset_index(drop=True)
        X, feat_cols = _feature_matrix(g)
        n = len(g)
        print(f"[phase4] race={race} n={n} clustering...", flush=True)
        # plan.md: min_cluster_size ≈ max(100, 0.3%–1% of n); publish n>=100
        min_cluster_size = max(100, int(0.005 * n)) if n >= 500 else max(5, int(0.08 * n))
        min_samples = max(10, min(50, min_cluster_size // 5)) if n >= 500 else max(3, min(10, min_cluster_size // 2))
        labels = _cluster_one(X, min_cluster_size, min_samples)
        print(
            f"[phase4] race={race} raw_clusters={len(set(labels)-{-1})} noise={(labels<0).mean():.1%}",
            flush=True,
        )
        min_publish = max(100, int(0.005 * n)) if n >= 500 else max(5, int(0.04 * n))
        for c in sorted(set(labels) - {-1}):
            if int((labels == c).sum()) < min_publish:
                labels[labels == c] = -1
        # if everything became noise, fall back to agglomerative without tiny filter
        if len(set(labels) - {-1}) == 0:
            labels = _cluster_one(X, max(3, min_cluster_size // 2), max(2, min_samples // 2))
        print(f"[phase4] race={race} bootstrap...", flush=True)
        stab = _bootstrap_stability(X, labels, min_cluster_size, min_samples)
        print(f"[phase4] race={race} medoids/enrichment...", flush=True)
        medoids = _medoid_indices(X, labels)
        enrich = _enrichment(g, labels, feat_cols)
        enrich_all[str(race)] = enrich

        # quality metrics
        valid = labels >= 0
        sil = None
        if valid.sum() >= 4 and len(set(labels[valid])) >= 2:
            try:
                # silhouette is O(n^2); sample for large races
                if int(valid.sum()) > 8000:
                    rng = np.random.default_rng(1)
                    vi = np.where(valid)[0]
                    take = rng.choice(vi, size=8000, replace=False)
                    sil = float(silhouette_score(X[take], labels[take]))
                else:
                    sil = float(silhouette_score(X[valid], labels[valid]))
            except Exception:
                sil = None
        coverage = float(valid.mean()) if n else 0.0
        noise_ratio = float((labels < 0).mean()) if n else 0.0

        pref = race_prefix.get(str(race), "X")
        # assign strategy ids
        cluster_ids = {}
        for local_c in sorted(set(labels) - {-1}):
            cluster_ids[local_c] = f"{pref}-G{local_c+1:02d}"
        meta_idx_cols = [c for c in g.columns if c in META_COLS or c.startswith("idx_")]
        tmp = g[meta_idx_cols].copy()
        tmp["local_cluster"] = labels
        tmp["strategy_id"] = [
            cluster_ids.get(int(lab), f"{pref}-Noise") for lab in labels
        ]
        tmp["is_noise"] = labels < 0
        tmp["cluster_scope"] = "global_race"
        global_rows.extend(tmp.to_dict(orient="records"))

        for local_c, sid in cluster_ids.items():
            idx = medoids.get(local_c)
            reps = []
            members = np.where(labels == local_c)[0]
            # nearest to medoid; subsample candidates if huge
            if idx is not None and len(members):
                cand = members
                if len(cand) > 3000:
                    rng = np.random.default_rng(2 + int(local_c))
                    # always keep medoid in candidate set
                    others = cand[cand != idx]
                    take = rng.choice(others, size=min(2999, len(others)), replace=False)
                    cand = np.unique(np.concatenate([[idx], take]))
                d = pairwise_distances(X[cand], X[idx].reshape(1, -1)).ravel()
                order = cand[np.argsort(d)]
                for j in order[:8]:
                    r = g.iloc[j]
                    reps.append(
                        {
                            "replay_id": r["replay_id"],
                            "player_id": int(r["player_id"]),
                            "matchup_dir": r["matchup_dir"],
                            "key_sequence": r.get("key_sequence"),
                            "is_medoid": bool(j == idx),
                        }
                    )
            representatives[sid] = {
                "race": race,
                "sample_size": int((labels == local_c).sum()),
                "prevalence": float((labels == local_c).mean()),
                "stability": stab["per_cluster_stability"].get(str(local_c)),
                "enriched_features": enrich.get(str(local_c), []),
                "representatives": reps,
            }
            stability_rows.append(
                {
                    "scope": "global_race",
                    "race": race,
                    "strategy_id": sid,
                    "n": int((labels == local_c).sum()),
                    "stability": stab["per_cluster_stability"].get(str(local_c)),
                    "mean_ari": stab["mean_ari"],
                    "silhouette": sil,
                    "coverage": coverage,
                    "noise_ratio": noise_ratio,
                    "min_cluster_size": min_cluster_size,
                    "min_samples": min_samples,
                }
            )

        # matchup variants: label by matchup only (avoid nested HDBSCAN explosion)
        print(f"[phase4] race={race} matchup variants...", flush=True)
        for local_c, sid in cluster_ids.items():
            sub = g.loc[labels == local_c]
            for mdir, mg in sub.groupby("matchup_dir"):
                for row in mg.itertuples(index=False):
                    matchup_rows.append(
                        {
                            "replay_id": row.replay_id,
                            "player_id": row.player_id,
                            "race": race,
                            "opponent_race": row.opponent_race,
                            "matchup_dir": mdir,
                            "global_strategy_id": sid,
                            "strategy_id": f"{sid}-{mdir}-A",
                            "variant_cluster": 0,
                        }
                    )
        print(
            f"[phase4] race={race} done strategies={list(cluster_ids.values())}",
            flush=True,
        )

    global_df = pd.DataFrame(global_rows)
    matchup_df = pd.DataFrame(matchup_rows)
    stab_df = pd.DataFrame(stability_rows)

    global_df.to_parquet(out_dir / "global_clusters.parquet", index=False)
    matchup_df.to_parquet(out_dir / "matchup_clusters.parquet", index=False)
    stab_df.to_csv(out_dir / "cluster_stability.csv", index=False)
    write_json(out_dir / "representative_build_orders.json", representatives)
    write_json(out_dir / "feature_enrichment.json", enrich_all)

    summary = {
        "horizon": PRIMARY_HORIZON,
        "clustered_players": int(len(global_df)),
        "strategies": sorted(representatives.keys()),
        "n_strategies": len(representatives),
        "noise_players": int(global_df["is_noise"].sum()) if len(global_df) else 0,
        "matchup_variants": int(matchup_df["strategy_id"].nunique()) if len(matchup_df) else 0,
    }
    write_json(out_dir / "phase04_summary.json", summary)
    return summary
