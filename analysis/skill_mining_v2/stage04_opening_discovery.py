"""Stage 04 — formal opening strategy discovery at selected window."""

from __future__ import annotations

from collections import Counter
from typing import Any

import numpy as np
import pandas as pd
from tqdm import tqdm

from analysis.skill_mining_v2.common.clustering import (
    bootstrap_stability,
    medoid_indices,
    prepare_matrix,
    recursive_cluster,
)
from analysis.skill_mining_v2.common.features import numeric_feature_cols, opening_features
from analysis.skill_mining_v2.common.io import ensure_dir, loads_actions, write_json
from analysis.skill_mining_v2.common.plotting import (
    embed_2d,
    plot_embedding_scatter,
    plot_feature_heatmap,
)
from analysis.skill_mining_v2.config import (
    OPENING_BOOTSTRAP_RETENTION_MIN,
    OPENING_PREVALENCE_MIN,
    adaptive_min_support,
    PipelineConfig,
)

META_EXCLUDE = {
    "run_id",
    "replay_id",
    "player_id",
    "race",
    "opponent_race",
    "directional_matchup",
    "result",
    "is_win",
    "mmr",
    "opponent_mmr",
    "mmr_diff",
    "map",
    "patch",
    "base_build",
    "region",
    "duration",
    "own_actions",
    "opponent_actions",
    "data_quality",
    "source_matchup_dir",
    "key_sequence",
    "horizon",
    "n_actions",
    "opening_id",
    "opening_raw",
}


PROFILE_COLS = [
    "inv_economy",
    "inv_expansion",
    "inv_production",
    "inv_technology",
    "inv_ground",
    "inv_air",
    "inv_defense",
    "inv_upgrade",
    "first_gas_time_z",
    "first_expansion_time_z",
    "first_tech_time_z",
    "first_production_time_z",
]


def run_stage04(cfg: PipelineConfig, traj: pd.DataFrame | None = None) -> dict[str, Any]:
    out_dir = ensure_dir(cfg.stage_dir(4, "04_openings"))
    assign_path = out_dir / "opening_assignments.parquet"
    if cfg.resume and assign_path.exists() and (out_dir / "opening_catalog.json").exists():
        print(f"[stage04] resume {out_dir}", flush=True)
        return {
            "assignments": pd.read_parquet(assign_path),
            "catalog": __import__("json").loads((out_dir / "opening_catalog.json").read_text()),
        }

    if traj is None:
        traj = pd.read_parquet(cfg.stage_dir(1, "01_trajectories") / "player_trajectories.parquet")
    selection = __import__("json").loads(
        (cfg.stage_dir(3, "03_opening_windows") / "window_selection.json").read_text()
    )
    global_window = int(selection.get("global_window", 300))

    assign_rows = []
    feature_rows = []
    catalog: dict[str, Any] = {}
    medoids_out: dict[str, Any] = {}
    stability_rows = []
    fig_dir = ensure_dir(cfg.figures_dir("opening_clusters"))
    data_dir = ensure_dir(cfg.figures_dir("data"))

    for mu in [m for m in cfg.matchups if m in set(traj["directional_matchup"])]:
        sub = traj[traj["directional_matchup"] == mu].reset_index(drop=True)
        if len(sub) < 30:
            continue
        window = global_window
        if selection.get("primary_mode") == "matchup_specific":
            window = int(selection.get("per_matchup", {}).get(mu, {}).get("window", global_window))

        min_size = adaptive_min_support(len(sub), frac=0.015)
        print(f"[stage04] {mu} window={window} n={len(sub)} min_size={min_size}", flush=True)

        feats_list = []
        for _, r in tqdm(sub.iterrows(), total=len(sub), desc=f"feats:{mu}"):
            f = opening_features(loads_actions(r["own_actions"]), window)
            f.update(
                {
                    "replay_id": r["replay_id"],
                    "player_id": r["player_id"],
                    "directional_matchup": mu,
                    "race": r["race"],
                    "opponent_race": r["opponent_race"],
                    "is_win": r["is_win"],
                    "mmr": r.get("mmr"),
                    "mmr_diff": r.get("mmr_diff"),
                    "map": r.get("map"),
                    "base_build": r.get("base_build"),
                    "region": r.get("region"),
                    "duration": r.get("duration"),
                }
            )
            feats_list.append(f)
        feats = pd.DataFrame(feats_list)
        cols = numeric_feature_cols(feats.columns, exclude=META_EXCLUDE)
        use_cols = [c for c in cols if not c.startswith("ng_") or float(feats[c].fillna(0).mean()) >= 0.02]
        X, _, _, _ = prepare_matrix(feats, use_cols)
        labels = recursive_cluster(X, min_cluster_size=min_size, seed=cfg.seed, max_depth=3)
        stab = bootstrap_stability(X, labels, repeats=5, seed=cfg.seed, min_cluster_size=min_size)
        med_idx = medoid_indices(X, labels)

        # admission
        n = len(sub)
        retained = []
        raw_to_id = {}
        next_i = 1
        for c in sorted(set(int(x) for x in labels)):
            support = int((labels == c).sum())
            prevalence = support / n
            retention = (stab.get("retention") or {}).get(str(c))
            ok = support >= min_size and prevalence >= OPENING_PREVALENCE_MIN
            if retention is not None and retention < OPENING_BOOTSTRAP_RETENTION_MIN and support < 2 * min_size:
                ok = False
            oid = f"{mu}_O{next_i:02d}"
            raw_to_id[c] = oid if ok else f"{mu}_OTHER"
            if ok:
                retained.append(c)
                next_i += 1
            stability_rows.append(
                {
                    "directional_matchup": mu,
                    "raw_cluster": c,
                    "opening_id": raw_to_id[c],
                    "support": support,
                    "prevalence": prevalence,
                    "retention": retention,
                    "admitted": ok,
                }
            )

        opening_ids = [raw_to_id[int(c)] for c in labels]
        feats["opening_id"] = opening_ids
        feats["opening_raw"] = labels
        feature_rows.append(feats)
        for i, (_, r) in enumerate(sub.iterrows()):
            assign_rows.append(
                {
                    "run_id": cfg.run_id,
                    "replay_id": r["replay_id"],
                    "player_id": r["player_id"],
                    "directional_matchup": mu,
                    "race": r["race"],
                    "opponent_race": r["opponent_race"],
                    "opening_window": window,
                    "opening_id": opening_ids[i],
                    "opening_raw": int(labels[i]),
                    "is_win": r["is_win"],
                    "mmr_diff": r.get("mmr_diff"),
                }
            )

        # catalog + medoids
        mu_catalog = {}
        for c in retained:
            oid = raw_to_id[c]
            mask = labels == c
            profile = {}
            for col in PROFILE_COLS:
                if col in feats.columns:
                    profile[col] = float(feats.loc[mask, col].mean())
            # distinctive flags
            flags = []
            for col in feats.columns:
                if col.startswith("has_") or col.endswith("_observed"):
                    rate = float(feats.loc[mask, col].mean())
                    base = float(feats[col].mean())
                    if rate >= 0.35 and base > 0 and rate / base >= 1.25:
                        flags.append({"feature": col, "rate": rate, "baseline": base})
            mi = med_idx.get(c)
            medoid = None
            if mi is not None:
                row = feats.iloc[mi]
                cluster_idx = np.where(mask)[0]
                winning_idx = cluster_idx[
                    feats.iloc[cluster_idx]["is_win"].to_numpy(dtype=int) == 1
                ]
                winning_seeds = []
                if len(winning_idx):
                    distances = np.linalg.norm(X[winning_idx] - X[mi], axis=1)
                    for rank in np.argsort(distances)[:5]:
                        wi = int(winning_idx[rank])
                        wr = feats.iloc[wi]
                        winning_seeds.append(
                            {
                                "replay_id": wr["replay_id"],
                                "player_id": int(wr["player_id"])
                                if pd.notna(wr["player_id"])
                                else None,
                                "key_sequence": wr.get("key_sequence"),
                                "distance_to_medoid": float(distances[rank]),
                            }
                        )
                medoid = {
                    "replay_id": row["replay_id"],
                    "player_id": int(row["player_id"]) if pd.notna(row["player_id"]) else None,
                    "key_sequence": row.get("key_sequence"),
                    "is_win": int(row["is_win"]),
                }
                medoids_out[oid] = {
                    **medoid,
                    "opening_id": oid,
                    "profile": profile,
                    "winning_trace_seeds": winning_seeds,
                }
            mu_catalog[oid] = {
                "opening_id": oid,
                "directional_matchup": mu,
                "support": int(mask.sum()),
                "winrate": float(feats.loc[mask, "is_win"].mean()),
                "profile": profile,
                "distinctive_flags": flags[:12],
                "medoid": medoid,
                "data_driven_name": None,
            }
        catalog[mu] = mu_catalog

        # figures
        try:
            xy = embed_2d(X, seed=cfg.seed)
            plot_embedding_scatter(xy, opening_ids, fig_dir, f"opening_embed_{mu}", title=f"{mu} openings")
            # prototype heatmap
            heat_rows = []
            for oid, info in mu_catalog.items():
                heat_rows.append({"opening_id": oid, **info["profile"]})
            if heat_rows:
                hdf = pd.DataFrame(heat_rows).set_index("opening_id")
                # z-score columns
                hz = (hdf - hdf.mean()) / (hdf.std(ddof=0) + 1e-6)
                plot_feature_heatmap(hz, fig_dir, data_dir, f"opening_heatmap_{mu}", title=f"{mu} opening profiles")
        except Exception as exc:
            print(f"[stage04] plot warn {mu}: {exc}", flush=True)

    assignments = pd.DataFrame(assign_rows)
    features = pd.concat(feature_rows, ignore_index=True) if feature_rows else pd.DataFrame()
    assignments.to_parquet(assign_path, index=False)
    if not features.empty:
        features.to_parquet(out_dir / "opening_features.parquet", index=False)
    write_json(out_dir / "opening_catalog.json", catalog)
    write_json(out_dir / "opening_medoid.json", medoids_out)
    pd.DataFrame(stability_rows).to_csv(out_dir / "opening_stability.csv", index=False)

    # report
    lines = ["# Opening Strategy Report", "", f"- Global window: {global_window}s", ""]
    for mu, items in catalog.items():
        lines.append(f"## {mu} ({len(items)} openings)")
        for oid, info in items.items():
            lines.append(
                f"- `{oid}` support={info['support']} winrate={info['winrate']:.3f} "
                f"medoid={info.get('medoid')}"
            )
        lines.append("")
    (out_dir / "opening_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[stage04] openings admitted: {sum(len(v) for v in catalog.values())}", flush=True)
    return {"assignments": assignments, "catalog": catalog, "features": features}
