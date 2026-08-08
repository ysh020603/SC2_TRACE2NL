"""Stage 03 — multi-window opening analysis and selection."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import normalized_mutual_info_score
from tqdm import tqdm

from analysis.skill_mining_v2.common.clustering import (
    bootstrap_stability,
    cluster_metrics,
    prepare_matrix,
    recursive_cluster,
    semantic_distinctiveness,
)
from analysis.skill_mining_v2.common.features import numeric_feature_cols, opening_features
from analysis.skill_mining_v2.common.io import ensure_dir, loads_actions, write_json
from analysis.skill_mining_v2.common.plotting import (
    plot_largest_cluster_ratio,
    plot_opening_window_metrics,
    plot_window_similarity_heatmap,
)
from analysis.skill_mining_v2.common.statistics import normalize_series, opponent_leakage_score
from analysis.skill_mining_v2.config import (
    WINDOW_ALPHA,
    WINDOW_BETA,
    WINDOW_DELTA,
    WINDOW_ETA,
    WINDOW_GAMMA,
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
}


def _feature_frame(traj: pd.DataFrame, window: int) -> pd.DataFrame:
    rows = []
    for _, r in traj.iterrows():
        feats = opening_features(loads_actions(r["own_actions"]), window)
        feats.update(
            {
                "replay_id": r["replay_id"],
                "player_id": r["player_id"],
                "directional_matchup": r["directional_matchup"],
                "is_win": r["is_win"],
                "mmr_diff": r.get("mmr_diff"),
            }
        )
        rows.append(feats)
    return pd.DataFrame(rows)


def _opp_feature_frame(traj: pd.DataFrame, window: int) -> pd.DataFrame:
    rows = []
    for _, r in traj.iterrows():
        feats = opening_features(loads_actions(r["opponent_actions"]), window)
        # keep only numeric investment/count features for leakage
        keep = {k: v for k, v in feats.items() if isinstance(v, (int, float)) and not isinstance(v, bool)}
        rows.append(keep)
    return pd.DataFrame(rows).fillna(0.0)


def run_stage03(cfg: PipelineConfig, traj: pd.DataFrame | None = None) -> dict[str, Any]:
    out_dir = ensure_dir(cfg.stage_dir(3, "03_opening_windows"))
    selection_path = out_dir / "window_selection.json"
    if cfg.resume and selection_path.exists():
        print(f"[stage03] resume {selection_path}", flush=True)
        return {"selection": __import__("json").loads(selection_path.read_text())}

    if traj is None:
        traj = pd.read_parquet(cfg.stage_dir(1, "01_trajectories") / "player_trajectories.parquet")

    windows = list(cfg.opening_windows)
    metric_rows = []
    stability_rows = []
    leakage_rows = []
    # labels per matchup/window for similarity
    label_store: dict[str, dict[int, np.ndarray]] = defaultdict(dict)
    fig_dir = ensure_dir(cfg.figures_dir("opening_windows"))
    data_dir = ensure_dir(cfg.figures_dir("data"))

    matchups = [m for m in cfg.matchups if m in set(traj["directional_matchup"])]
    for mu in matchups:
        sub = traj[traj["directional_matchup"] == mu].reset_index(drop=True)
        if len(sub) < 30:
            print(f"[stage03] skip {mu}: n={len(sub)}", flush=True)
            continue
        min_size = adaptive_min_support(len(sub), frac=0.02)
        print(f"[stage03] {mu} n={len(sub)} windows={windows} min_size={min_size}", flush=True)

        for window in tqdm(windows, desc=f"windows:{mu}"):
            feats = _feature_frame(sub, window)
            cols = numeric_feature_cols(feats.columns, exclude=META_EXCLUDE)
            # drop ultra-sparse ngrams
            use_cols = []
            for c in cols:
                if c.startswith("ng_"):
                    if float(feats[c].fillna(0).mean()) < 0.02:
                        continue
                use_cols.append(c)
            if len(use_cols) < 3:
                continue
            X, _, _, _ = prepare_matrix(feats, use_cols)
            labels = recursive_cluster(X, min_cluster_size=min_size, seed=cfg.seed)
            metrics = cluster_metrics(X, labels)
            stab = bootstrap_stability(X, labels, repeats=4, seed=cfg.seed, min_cluster_size=min_size)
            sem = semantic_distinctiveness(feats, labels, use_cols)
            opp_feats = _opp_feature_frame(sub, window)
            # align numeric cols
            opp_cols = [c for c in opp_feats.columns if c.startswith(("inv_", "cnt_", "ordered_", "has_"))]
            leak = opponent_leakage_score(labels, opp_feats[opp_cols], seed=cfg.seed)

            label_store[mu][window] = labels
            metric_rows.append(
                {
                    "directional_matchup": mu,
                    "window": window,
                    "n": metrics["n"],
                    "n_clusters": metrics["n_clusters"],
                    "silhouette": metrics["silhouette"],
                    "calinski_harabasz": metrics["calinski_harabasz"],
                    "davies_bouldin": metrics["davies_bouldin"],
                    "largest_cluster_ratio": metrics["largest_cluster_ratio"],
                    "stability_ari": stab["mean_ari"],
                    "stability_nmi": stab["mean_nmi"],
                    "semantic_distinctiveness": sem,
                    "leakage": leak,
                    "run_id": cfg.run_id,
                }
            )
            stability_rows.append(
                {
                    "directional_matchup": mu,
                    "window": window,
                    "mean_ari": stab["mean_ari"],
                    "mean_nmi": stab["mean_nmi"],
                    "retention": stab["retention"],
                }
            )
            leakage_rows.append(
                {"directional_matchup": mu, "window": window, "leakage": leak}
            )

    metrics_df = pd.DataFrame(metric_rows)
    if metrics_df.empty:
        selection = {
            "global_window": 300,
            "per_matchup": {},
            "reason": "insufficient_data_fallback_300",
            "run_id": cfg.run_id,
        }
        write_json(selection_path, selection)
        return {"selection": selection, "metrics": metrics_df}

    # score
    scored = metrics_df.copy()
    for col in ["silhouette", "stability_ari", "semantic_distinctiveness", "largest_cluster_ratio", "leakage"]:
        if col not in scored.columns:
            scored[col] = 0.0
        # Window scores must be comparable within a matchup. Global normalization
        # lets large/easy matchups distort another matchup's recommended window.
        scored[f"{col}_n"] = scored.groupby("directional_matchup")[col].transform(
            lambda s: normalize_series(s.fillna(0.0))
        )
    scored["opening_score"] = (
        WINDOW_ALPHA * scored["silhouette_n"]
        + WINDOW_BETA * scored["stability_ari_n"]
        + WINDOW_GAMMA * scored["semantic_distinctiveness_n"]
        - WINDOW_DELTA * scored["largest_cluster_ratio_n"]
        - WINDOW_ETA * scored["leakage_n"]
    )

    per_matchup = {}
    for mu, g in scored.groupby("directional_matchup"):
        best = g.loc[g["opening_score"].idxmax()]
        per_matchup[mu] = {
            "window": int(best["window"]),
            "score": float(best["opening_score"]),
            "silhouette": best["silhouette"],
            "stability_ari": best["stability_ari"],
            "leakage": best["leakage"],
            "largest_cluster_ratio": best["largest_cluster_ratio"],
        }

    # global = mode of per-matchup, tie-break by mean score
    mean_by_w = scored.groupby("window")["opening_score"].mean().sort_values(ascending=False)
    global_window = int(mean_by_w.index[0])

    selection = {
        "global_window": global_window,
        "per_matchup": per_matchup,
        "primary_mode": "global",
        "score_weights": {
            "alpha_separability": WINDOW_ALPHA,
            "beta_stability": WINDOW_BETA,
            "gamma_semantic": WINDOW_GAMMA,
            "delta_largest_penalty": WINDOW_DELTA,
            "eta_leakage": WINDOW_ETA,
        },
        "run_id": cfg.run_id,
    }

    metrics_df.to_csv(out_dir / "window_metrics.csv", index=False)
    scored.to_csv(out_dir / "matchup_window_metrics.csv", index=False)
    pd.DataFrame(stability_rows).to_csv(out_dir / "cluster_stability.csv", index=False)
    pd.DataFrame(leakage_rows).to_csv(out_dir / "leakage_proxy.csv", index=False)
    write_json(selection_path, selection)

    # similarity heatmaps for a representative matchup
    for mu, win_map in label_store.items():
        wins = sorted(win_map)
        if len(wins) < 2:
            continue
        mat = pd.DataFrame(index=wins, columns=wins, dtype=float)
        for i in wins:
            for j in wins:
                a, b = win_map[i], win_map[j]
                n = min(len(a), len(b))
                mat.loc[i, j] = float(normalized_mutual_info_score(a[:n], b[:n]))
        plot_window_similarity_heatmap(mat.astype(float), fig_dir, data_dir, name=f"window_nmi_{mu}")
        break

    plot_opening_window_metrics(scored, fig_dir, data_dir)
    plot_largest_cluster_ratio(scored, fig_dir, data_dir)

    report = _write_report(out_dir, selection, scored)
    print(f"[stage03] global_window={global_window}\n{report[:400]}", flush=True)
    return {"selection": selection, "metrics": scored}


def _write_report(out_dir, selection, scored: pd.DataFrame) -> str:
    lines = [
        "# Opening Window Report",
        "",
        f"- Global recommended window: **{selection['global_window']}s**",
        f"- Primary mode: `{selection['primary_mode']}`",
        "",
        "## Per-matchup recommendations",
        "",
    ]
    for mu, info in selection.get("per_matchup", {}).items():
        lines.append(
            f"- **{mu}**: {info['window']}s "
            f"(score={info['score']:.3f}, sil={info['silhouette']}, "
            f"ARI={info['stability_ari']}, leakage={info['leakage']}, "
            f"largest={info['largest_cluster_ratio']:.3f})"
        )
    lines += [
        "",
        "## Interpretation",
        "",
        "- Too-short windows tend to inflate largest-cluster ratio (everyone looks similar).",
        "- Too-long windows increase opponent-leakage proxy (adaptation bleeds into opening).",
        "- Selected window balances separability, bootstrap stability, semantic distinctiveness,",
        "  against largest-cluster penalty and opponent leakage.",
        "",
        "## Mean score by window",
        "",
    ]
    if not scored.empty:
        mean_by_w = scored.groupby("window")["opening_score"].mean()
        for w, s in mean_by_w.items():
            lines.append(f"- {int(w)}s: mean_score={s:.3f}")
    text = "\n".join(lines) + "\n"
    (out_dir / "opening_window_report.md").write_text(text, encoding="utf-8")
    return text
