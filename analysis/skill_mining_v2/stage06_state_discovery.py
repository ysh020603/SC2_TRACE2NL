"""Stage 06 — own/opponent strategic state discovery."""

from __future__ import annotations

from typing import Any

import numpy as np
import pandas as pd
from tqdm import tqdm

from analysis.skill_mining_v2.common.clustering import (
    medoid_indices,
    prepare_matrix,
    recursive_cluster,
)
from analysis.skill_mining_v2.common.features import numeric_feature_cols
from analysis.skill_mining_v2.common.io import ensure_dir, write_json
from analysis.skill_mining_v2.common.plotting import embed_2d, plot_embedding_scatter, plot_feature_heatmap
from analysis.skill_mining_v2.config import STATE_CLUSTER_K_RANGE, adaptive_min_support, PipelineConfig


OWN_PREFIXES = ("own_cum_", "own_cnt_cum_", "own_recent_", "own_ordered_")
OPP_PREFIXES = ("opp_cum_", "opp_cnt_cum_", "opp_recent_", "opp_ordered_")


def _cluster_side(
    df: pd.DataFrame,
    prefixes: tuple[str, ...],
    id_prefix: str,
    min_size: int,
    seed: int,
) -> tuple[list[str], dict[str, Any], np.ndarray, list[str]]:
    cols = [c for c in df.columns if c.startswith(prefixes)]
    cols = numeric_feature_cols(cols) if cols else []
    # fallback: any matching prefix
    if not cols:
        cols = [c for c in df.columns if any(c.startswith(p) for p in prefixes)]
    if not cols or len(df) < max(10, min_size):
        labels = [f"{id_prefix}01"] * len(df)
        return labels, {}, np.zeros((len(df), 2)), cols

    X, _, _, _ = prepare_matrix(df, cols, max_dim=30)
    k_min, k_max = STATE_CLUSTER_K_RANGE
    raw = recursive_cluster(
        X,
        k_range=(k_min, k_max),
        min_cluster_size=min_size,
        seed=seed,
        max_depth=1,
    )
    mapping = {}
    next_i = 1
    out_ids = []
    for lab in raw:
        lab = int(lab)
        if lab not in mapping:
            mapping[lab] = f"{id_prefix}{next_i:02d}"
            next_i += 1
        out_ids.append(mapping[lab])

    profiles = {}
    med = medoid_indices(X, raw)
    for lab, sid in mapping.items():
        mask = raw == lab
        prof = {c: float(df.loc[mask, c].mean()) for c in cols[:40]}
        profiles[sid] = {
            "state_id": sid,
            "support": int(mask.sum()),
            "profile": prof,
            "medoid_index": int(med[lab]) if lab in med else None,
        }
    return out_ids, profiles, X, cols


def run_stage06(cfg: PipelineConfig, snapshots: pd.DataFrame | None = None) -> dict[str, Any]:
    out_dir = ensure_dir(cfg.stage_dir(6, "06_states"))
    out_path = out_dir / "state_assignments.parquet"
    if cfg.resume and out_path.exists() and (out_dir / "state_catalog.json").exists():
        print(f"[stage06] resume {out_dir}", flush=True)
        return {
            "assignments": pd.read_parquet(out_path),
            "catalog": __import__("json").loads((out_dir / "state_catalog.json").read_text()),
        }

    if snapshots is None:
        snapshots = pd.read_parquet(cfg.stage_dir(5, "05_snapshots") / "snapshots.parquet")

    snap = snapshots.copy()
    snap["phase"] = snap["t"].map(lambda t: f"T{int(t)}")

    assign_parts = []
    catalog: dict[str, Any] = {"own": {}, "opp": {}}
    fig_dir = ensure_dir(cfg.figures_dir("state_space"))
    data_dir = ensure_dir(cfg.figures_dir("data"))

    # Cumulative counts are strongly time-dependent. Pooling 300s and 360s in one
    # cluster mostly discovers elapsed time rather than strategic state, so state
    # discovery is performed at each exact snapshot.
    group_keys = ["directional_matchup", "opening_id", "phase"]
    groups = list(snap.groupby(group_keys, dropna=False))
    for keys, g in tqdm(groups, desc="stage06"):
        g = g.reset_index(drop=True)
        mu, oid, phase = keys
        if len(g) < 25:
            g = g.copy()
            g["own_state_id"] = f"{mu}_{oid}_{phase}_OWN_S00"
            g["opp_state_id"] = f"{mu}_{oid}_{phase}_OPP_S00"
            assign_parts.append(g)
            continue
        min_size = adaptive_min_support(len(g), default=80, frac=0.05)
        own_ids, own_prof, own_X, own_cols = _cluster_side(
            g, OWN_PREFIXES, f"{mu}_{oid}_{phase}_OWN_S", min_size, cfg.seed
        )
        opp_ids, opp_prof, opp_X, opp_cols = _cluster_side(
            g, OPP_PREFIXES, f"{mu}_{oid}_{phase}_OPP_S", min_size, cfg.seed + 1
        )
        g = g.copy()
        g["own_state_id"] = own_ids
        g["opp_state_id"] = opp_ids
        assign_parts.append(g)
        catalog["own"].update(own_prof)
        catalog["opp"].update(opp_prof)

        # one figure per major group
        if len(g) >= 80 and own_X is not None and len(own_X):
            try:
                xy = embed_2d(own_X, seed=cfg.seed)
                plot_embedding_scatter(
                    xy,
                    own_ids,
                    fig_dir,
                    f"own_state_{mu}_{oid}_{phase}",
                    title=f"{mu} {oid} {phase} own states",
                )
                # centroid heatmap
                rows = []
                for sid, info in own_prof.items():
                    row = {"state_id": sid}
                    for k, v in info["profile"].items():
                        short = k.replace("own_", "")
                        row[short] = v
                    rows.append(row)
                if rows:
                    hdf = pd.DataFrame(rows).set_index("state_id")
                    # keep compact columns
                    keep = [c for c in hdf.columns if "cum_" in c or "ordered_" in c][:12]
                    if keep:
                        hz = hdf[keep]
                        hz = (hz - hz.mean()) / (hz.std(ddof=0) + 1e-6)
                        plot_feature_heatmap(
                            hz,
                            fig_dir,
                            data_dir,
                            f"own_state_heat_{mu}_{oid}_{phase}",
                            title=f"{mu} {oid} {phase}",
                        )
            except Exception as exc:
                print(f"[stage06] plot warn: {exc}", flush=True)

    assignments = pd.concat(assign_parts, ignore_index=True) if assign_parts else snap
    # keep essential columns + state ids + response features
    assignments.to_parquet(out_path, index=False)
    write_json(out_dir / "state_catalog.json", catalog)
    write_json(
        out_dir / "state_summary.json",
        {
            "n_rows": int(len(assignments)),
            "n_own_states": len(catalog["own"]),
            "n_opp_states": len(catalog["opp"]),
            "run_id": cfg.run_id,
        },
    )
    print(
        f"[stage06] own_states={len(catalog['own'])} opp_states={len(catalog['opp'])}",
        flush=True,
    )
    return {"assignments": assignments, "catalog": catalog}
