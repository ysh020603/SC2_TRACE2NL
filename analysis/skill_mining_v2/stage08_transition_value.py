"""Stage 08 — transition value estimation and edge labeling."""

from __future__ import annotations

import json
from typing import Any

import numpy as np
import pandas as pd

from analysis.skill_mining_v2.common.io import ensure_dir, write_json
from analysis.skill_mining_v2.common.plotting import plot_forest, plot_value_heatmap
from analysis.skill_mining_v2.common.statistics import classify_edge, estimate_response_values
from analysis.skill_mining_v2.config import adaptive_ess, adaptive_min_support, PipelineConfig


def _attach_robustness(
    values: pd.DataFrame,
    transitions: pd.DataFrame,
    context_cols: list[str],
) -> pd.DataFrame:
    if values.empty:
        return values
    grouped = {
        keys if isinstance(keys, tuple) else (keys,): group
        for keys, group in transitions.groupby(context_cols, dropna=False)
    }
    rows = []
    for _, edge in values.iterrows():
        key = tuple(edge[c] for c in context_cols)
        context = grouped.get(key, transitions.iloc[0:0])
        response = context[context["response_id"].astype(str) == str(edge["response_id"])]
        other = context[context["response_id"].astype(str) != str(edge["response_id"])]
        expected_sign = np.sign(float(edge.get("adjusted_lift") or 0.0))
        subgroup_lifts = []
        for col in ("map", "patch", "base_build", "region"):
            if col not in context.columns:
                continue
            for value, subgroup in context.groupby(col, dropna=False):
                treated = subgroup[
                    subgroup["response_id"].astype(str) == str(edge["response_id"])
                ]
                control = subgroup[
                    subgroup["response_id"].astype(str) != str(edge["response_id"])
                ]
                if len(treated) >= 5 and len(control) >= 5:
                    subgroup_lifts.append(
                        {
                            "factor": col,
                            "value": str(value),
                            "lift": float(treated["is_win"].mean() - control["is_win"].mean()),
                        }
                    )
        if "mmr_diff" in context.columns and context["mmr_diff"].notna().sum() >= 30:
            ranked = context.assign(
                _mmr_band=pd.qcut(
                    context["mmr_diff"].rank(method="first"),
                    q=3,
                    labels=["low", "mid", "high"],
                )
            )
            for value, subgroup in ranked.groupby("_mmr_band", observed=True):
                treated = subgroup[
                    subgroup["response_id"].astype(str) == str(edge["response_id"])
                ]
                control = subgroup[
                    subgroup["response_id"].astype(str) != str(edge["response_id"])
                ]
                if len(treated) >= 5 and len(control) >= 5:
                    subgroup_lifts.append(
                        {
                            "factor": "mmr_band",
                            "value": str(value),
                            "lift": float(treated["is_win"].mean() - control["is_win"].mean()),
                        }
                    )
        signs = [
            np.sign(item["lift"]) == expected_sign
            for item in subgroup_lifts
            if expected_sign != 0 and item["lift"] != 0
        ]
        consistency = float(np.mean(signs)) if signs else None
        if consistency is not None and not np.isfinite(consistency):
            consistency = None
        record = edge.to_dict()
        for key, value in list(record.items()):
            if isinstance(value, (float, np.floating)) and not np.isfinite(value):
                record[key] = None
            elif pd.isna(value):
                record[key] = None
        record["robustness_checks"] = json.dumps(subgroup_lifts, ensure_ascii=False)
        record["robustness_consistency"] = consistency
        record["robustness_pass"] = consistency is None or consistency >= 0.60
        for outcome in ("early_loss_6m", "early_loss_8m", "early_loss_10m"):
            if outcome in context.columns and len(response) and len(other):
                lift = float(response[outcome].mean() - other[outcome].mean())
                record[f"{outcome}_lift"] = lift if np.isfinite(lift) else None
        rows.append(record)
    return pd.DataFrame(rows)


def run_stage08(cfg: PipelineConfig, transitions: pd.DataFrame | None = None) -> dict[str, Any]:
    out_dir = ensure_dir(cfg.stage_dir(8, "08_transition_value"))
    out_path = out_dir / "edge_values.parquet"
    if cfg.resume and out_path.exists():
        print(f"[stage08] resume {out_path}", flush=True)
        return {"edges": pd.read_parquet(out_path)}

    if transitions is None:
        transitions = pd.read_parquet(
            cfg.stage_dir(7, "07_transitions") / "transition_table.parquet"
        )
    if transitions.empty:
        empty = pd.DataFrame()
        empty.to_parquet(out_path, index=False)
        write_json(out_dir / "value_summary.json", {"n_edges": 0})
        return {"edges": empty}

    context_cols = ["opening_id", "own_state_id", "opp_state_id", "t"]
    cov_cols = [
        c
        for c in ("mmr_diff", "map", "patch", "base_build", "region")
        if c in transitions.columns
    ]

    # estimate per matchup for tractability
    parts = []
    for mu, g in transitions.groupby("directional_matchup"):
        print(f"[stage08] estimating values for {mu} n={len(g)}", flush=True)
        vals = estimate_response_values(
            g,
            context_cols=context_cols,
            response_col="response_id",
            outcome_col="is_win",
            covariate_cols=cov_cols or None,
            seed=cfg.seed,
        )
        if vals is None or vals.empty:
            continue
        vals["directional_matchup"] = mu
        vals = _attach_robustness(vals, g, context_cols)
        min_sup = adaptive_min_support(len(g), frac=0.01)
        min_ess = adaptive_ess(len(g))
        vals["edge_label"] = [
            classify_edge(row, min_support=min_sup, min_ess=min_ess) for _, row in vals.iterrows()
        ]
        vals["min_support_threshold"] = min_sup
        vals["min_ess_threshold"] = min_ess
        parts.append(vals)

    edges = pd.concat(parts, ignore_index=True) if parts else pd.DataFrame()
    # attach next-state mode for each context+response
    if not edges.empty:
        nxt = (
            transitions.groupby(context_cols + ["response_id"])["next_own_state_id"]
            .agg(lambda s: s.value_counts().index[0])
            .reset_index()
            .rename(columns={"next_own_state_id": "next_own_state_id"})
        )
        edges = edges.merge(nxt, on=context_cols + ["response_id"], how="left")
        edges["edge_id"] = [
            f"E_{i:05d}_{row.opening_id}_{row.response_id}_{int(row.t)}"
            for i, row in enumerate(edges.itertuples())
        ]
        edges["run_id"] = cfg.run_id

    edges.to_parquet(out_path, index=False)
    edges.to_csv(out_dir / "edge_values.csv", index=False)

    summary = {
        "n_edges": int(len(edges)),
        "by_label": edges["edge_label"].value_counts().to_dict() if len(edges) else {},
        "run_id": cfg.run_id,
    }
    write_json(out_dir / "value_summary.json", summary)

    # figures
    fig_dir = ensure_dir(cfg.figures_dir("value"))
    data_dir = ensure_dir(cfg.figures_dir("data"))
    if not edges.empty:
        # forest of top |lift|
        top = edges.reindex(edges["adjusted_lift"].abs().sort_values(ascending=False).index).head(25)
        forest = top.copy()
        forest["label"] = forest["opening_id"].astype(str) + "|" + forest["response_id"].astype(str)
        forest["lift_ci"] = 0.02
        plot_forest(forest, fig_dir, data_dir)
        # heatmap for top opening
        oid = edges["opening_id"].value_counts().index[0]
        sub = edges[edges["opening_id"] == oid]
        if not sub.empty:
            mat = sub.pivot_table(
                index="opp_state_id",
                columns="response_id",
                values="adjusted_lift",
                aggfunc="mean",
            )
            plot_value_heatmap(mat, fig_dir, data_dir, name=f"value_heatmap_{oid}")

    # report
    lines = [
        "# Transition Value Report",
        "",
        f"- Edges scored: {summary['n_edges']}",
        f"- Labels: {summary['by_label']}",
        "",
        "## Preferred (top)",
        "",
    ]
    if not edges.empty:
        pref = edges[edges["edge_label"] == "preferred"].sort_values("adjusted_lift", ascending=False).head(20)
        for _, r in pref.iterrows():
            lines.append(
                f"- {r['edge_id']}: lift={r['adjusted_lift']:.3f} support={r['support']} "
                f"ctx=({r['opening_id']},{r['own_state_id']},{r['opp_state_id']},t={r['t']}) -> {r['response_id']}"
            )
        lines += ["", "## Harmful (top)", ""]
        harm = edges[edges["edge_label"] == "harmful"].sort_values("adjusted_lift").head(20)
        for _, r in harm.iterrows():
            lines.append(
                f"- {r['edge_id']}: lift={r['adjusted_lift']:.3f} support={r['support']} "
                f"ctx=({r['opening_id']},{r['own_state_id']},{r['opp_state_id']},t={r['t']}) -> {r['response_id']}"
            )
    (out_dir / "value_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[stage08] edges={summary['n_edges']} labels={summary['by_label']}", flush=True)
    return {"edges": edges}
