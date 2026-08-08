"""Stage 07 — opponent-conditioned transition / response mining."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

import numpy as np
import pandas as pd
from tqdm import tqdm

from analysis.skill_mining_v2.common.clustering import prepare_matrix, recursive_cluster
from analysis.skill_mining_v2.common.features import numeric_feature_cols
from analysis.skill_mining_v2.common.io import ensure_dir, write_json
from analysis.skill_mining_v2.common.plotting import plot_transition_matrix
from analysis.skill_mining_v2.config import RESPONSE_DELTA, RESPONSE_CLUSTER_K_RANGE, adaptive_min_support, PipelineConfig


def run_stage07(cfg: PipelineConfig, states: pd.DataFrame | None = None) -> dict[str, Any]:
    out_dir = ensure_dir(cfg.stage_dir(7, "07_transitions"))
    table_path = out_dir / "transition_table.parquet"
    if cfg.resume and table_path.exists():
        print(f"[stage07] resume {out_dir}", flush=True)
        return {
            "transitions": pd.read_parquet(table_path),
            "response_clusters": __import__("json").loads(
                (out_dir / "response_clusters.json").read_text()
            ),
        }

    if states is None:
        states = pd.read_parquet(cfg.stage_dir(6, "06_states") / "state_assignments.parquet")

    # build next-state links at t -> t+delta
    key_cols = ["replay_id", "player_id", "directional_matchup", "opening_id"]
    st = states.sort_values(key_cols + ["t"]).reset_index(drop=True)
    st["t_next"] = st["t"] + RESPONSE_DELTA
    # map exact next snapshot if present
    next_map = st.set_index(key_cols + ["t"])[["own_state_id"]].to_dict()["own_state_id"]

    rows = []
    for _, r in tqdm(st.iterrows(), total=len(st), desc="stage07-link"):
        nk = (r["replay_id"], r["player_id"], r["directional_matchup"], r["opening_id"], r["t"] + RESPONSE_DELTA)
        # also accept nearest available next time in SNAPSHOT grid
        next_own = next_map.get(nk)
        if next_own is None:
            # try any later snapshot within 2*delta
            for dt in (RESPONSE_DELTA, 120, 180):
                nk2 = (r["replay_id"], r["player_id"], r["directional_matchup"], r["opening_id"], r["t"] + dt)
                next_own = next_map.get(nk2)
                if next_own is not None:
                    nk = nk2
                    break
        if next_own is None:
            continue
        rows.append(
            {
                "run_id": cfg.run_id,
                "replay_id": r["replay_id"],
                "player_id": r["player_id"],
                "directional_matchup": r["directional_matchup"],
                "opening_id": r["opening_id"],
                "t": int(r["t"]),
                "t_next": int(nk[-1]),
                "own_state_id": r["own_state_id"],
                "opp_state_id": r["opp_state_id"],
                "next_own_state_id": next_own,
                "is_win": r["is_win"],
                "mmr_diff": r.get("mmr_diff"),
                "map": r.get("map"),
                "patch": r.get("patch"),
                "base_build": r.get("base_build"),
                "region": r.get("region"),
                "early_loss_6m": r.get("early_loss_6m"),
                "early_loss_8m": r.get("early_loss_8m"),
                "early_loss_10m": r.get("early_loss_10m"),
                **{c: r[c] for c in st.columns if c.startswith("resp_")},
            }
        )
    ctx = pd.DataFrame(rows)
    if ctx.empty:
        write_json(out_dir / "response_clusters.json", {})
        ctx.to_parquet(table_path, index=False)
        print("[stage07] no transitions", flush=True)
        return {"transitions": ctx, "response_clusters": {}}

    # cluster responses globally within matchup
    resp_cols = [c for c in ctx.columns if c.startswith("resp_d_") or c.startswith("resp_dc_")]
    resp_cols = numeric_feature_cols(resp_cols) or resp_cols
    response_clusters: dict[str, Any] = {}
    ctx["response_id"] = "R00"
    for mu, g in ctx.groupby("directional_matchup"):
        idx = g.index.to_numpy()
        if len(g) < 40 or not resp_cols:
            rid = f"{mu}_R01"
            ctx.loc[idx, "response_id"] = rid
            response_clusters[rid] = {"support": int(len(g)), "top_actions": []}
            continue
        min_size = adaptive_min_support(len(g), default=80, frac=0.03)
        X, _, _, _ = prepare_matrix(g, resp_cols, max_dim=25)
        raw = recursive_cluster(
            X,
            k_range=RESPONSE_CLUSTER_K_RANGE,
            min_cluster_size=min_size,
            seed=cfg.seed,
            max_depth=1,
        )
        mapping = {}
        next_i = 1
        ids = []
        for lab in raw:
            lab = int(lab)
            if lab not in mapping:
                mapping[lab] = f"{mu}_R{next_i:02d}"
                next_i += 1
            ids.append(mapping[lab])
        ctx.loc[idx, "response_id"] = ids
        for lab, rid in mapping.items():
            mask = raw == lab
            top = []
            if "resp_top_actions" in g.columns:
                # aggregate top action strings
                c = defaultdict(int)
                for s in g.loc[g.index[mask], "resp_top_actions"].fillna(""):
                    for part in str(s).split(","):
                        if ":" in part:
                            name, cnt = part.rsplit(":", 1)
                            try:
                                c[name] += int(cnt)
                            except ValueError:
                                pass
                top = [{"name": k, "count": v} for k, v in sorted(c.items(), key=lambda x: -x[1])[:10]]
            profile = {c: float(g.loc[g.index[mask], c].mean()) for c in resp_cols[:20]}
            response_clusters[rid] = {
                "response_id": rid,
                "support": int(mask.sum()),
                "top_actions": top,
                "profile": profile,
            }

    # conditional vs default
    cond_rows = []
    for keys, g in ctx.groupby(["opening_id", "own_state_id", "opp_state_id", "t"], dropna=False):
        opening, own_s, opp_s, t = keys
        n = len(g)
        for rid, rg in g.groupby("response_id"):
            cond_rows.append(
                {
                    "opening_id": opening,
                    "own_state_id": own_s,
                    "opp_state_id": opp_s,
                    "t": int(t),
                    "response_id": rid,
                    "support": int(len(rg)),
                    "p_cond": len(rg) / n,
                }
            )
    cond_df = pd.DataFrame(cond_rows)

    default_rows = []
    for keys, g in ctx.groupby(["opening_id", "own_state_id", "t"], dropna=False):
        opening, own_s, t = keys
        n = len(g)
        for rid, rg in g.groupby("response_id"):
            default_rows.append(
                {
                    "opening_id": opening,
                    "own_state_id": own_s,
                    "t": int(t),
                    "response_id": rid,
                    "support": int(len(rg)),
                    "p_default": len(rg) / n,
                }
            )
    def_df = pd.DataFrame(default_rows)
    if not cond_df.empty and not def_df.empty:
        merged = cond_df.merge(def_df, on=["opening_id", "own_state_id", "t", "response_id"], how="left")
        merged["lift_vs_default"] = merged["p_cond"] - merged["p_default"].fillna(0)
        merged["is_conditional"] = merged["lift_vs_default"] >= 0.08
    else:
        merged = cond_df

    ctx.to_parquet(table_path, index=False)
    ctx.to_parquet(out_dir / "contexts.parquet", index=False)
    pd.DataFrame(
        [{"response_id": k, **v} for k, v in response_clusters.items()]
    ).to_parquet(out_dir / "responses.parquet", index=False)
    write_json(out_dir / "response_clusters.json", response_clusters)
    merged.to_parquet(out_dir / "conditional_response_table.parquet", index=False)

    # visualization: one matrix for a frequent opening
    fig_dir = ensure_dir(cfg.figures_dir("transitions"))
    data_dir = ensure_dir(cfg.figures_dir("data"))
    if not ctx.empty:
        top_opening = ctx["opening_id"].value_counts().index[0]
        sub = ctx[ctx["opening_id"] == top_opening]
        mat = pd.crosstab(sub["opp_state_id"], sub["response_id"], normalize="index")
        plot_transition_matrix(
            mat, fig_dir, data_dir, f"response_matrix_{top_opening}", title=f"{top_opening} P(R|Opp)"
        )

    # report
    n_cond = int(merged["is_conditional"].sum()) if "is_conditional" in merged.columns else 0
    lines = [
        "# Transition / Evolution Report",
        "",
        f"- Transitions: {len(ctx)}",
        f"- Response clusters: {len(response_clusters)}",
        f"- Conditional enrichments: {n_cond}",
        "",
        "## Notes",
        "",
        "- Default evolution uses P(R | Opening, OwnState).",
        "- Conditional responses use P(R | Opening, OwnState, OpponentState).",
        "- `is_conditional` marks responses enriched by >=8pp versus default.",
        "",
    ]
    (out_dir / "transition_report.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"[stage07] transitions={len(ctx)} responses={len(response_clusters)}", flush=True)
    return {"transitions": ctx, "response_clusters": response_clusters, "conditional": merged}
