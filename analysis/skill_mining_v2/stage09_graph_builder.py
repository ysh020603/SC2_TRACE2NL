"""Stage 09 — signed temporal strategy evolution graphs."""

from __future__ import annotations

from typing import Any

import pandas as pd

from analysis.skill_mining_v2.common.io import ensure_dir, write_json
from analysis.skill_mining_v2.common.plotting import plot_graph_summary
from analysis.skill_mining_v2.common.validation import validate_graph
from analysis.skill_mining_v2.config import (
    MAX_DEFAULT_EDGES,
    MAX_HARMFUL_EDGES,
    MAX_PREFERRED_EDGES,
    PipelineConfig,
)


def _prune_edges(edges: pd.DataFrame) -> pd.DataFrame:
    if edges.empty:
        return edges
    keep = []
    for (opening, own, t), g in edges.groupby(["opening_id", "own_state_id", "t"], dropna=False):
        pref = g[g["edge_label"] == "preferred"].sort_values("adjusted_lift", ascending=False).head(MAX_PREFERRED_EDGES)
        harm = g[g["edge_label"] == "harmful"].sort_values("adjusted_lift").head(MAX_HARMFUL_EDGES)
        default = g[g["edge_label"] == "default"].sort_values("p_response", ascending=False).head(MAX_DEFAULT_EDGES)
        # if no default labeled, take highest frequency uncertain/default-ish
        if default.empty:
            default = g.sort_values("p_response", ascending=False).head(MAX_DEFAULT_EDGES)
            default = default.copy()
            default["edge_label"] = default["edge_label"].where(
                default["edge_label"].isin(["preferred", "harmful"]), "default"
            )
        keep.append(pd.concat([pref, harm, default], ignore_index=True))
    return pd.concat(keep, ignore_index=True) if keep else edges.iloc[0:0]


def _build_graph_for_opening(
    opening_id: str,
    edges: pd.DataFrame,
    catalog_openings: dict[str, Any],
) -> dict[str, Any]:
    nodes = {}
    # opening node
    nodes[f"OPEN::{opening_id}"] = {
        "id": f"OPEN::{opening_id}",
        "kind": "opening",
        "label": opening_id,
        "time": 0,
        "opening_id": opening_id,
    }
    graph_edges = []
    for _, e in edges.iterrows():
        src = f"{e['own_state_id']}@t{int(e['t'])}"
        tgt_state = e.get("next_own_state_id") or f"UNK_{e['response_id']}"
        tgt = f"{tgt_state}@t{int(e['t_next']) if pd.notna(e.get('t_next')) else int(e['t']) + 60}"
        if "t_next" not in e or pd.isna(e.get("t_next")):
            # infer
            t_next = int(e["t"]) + 60
            tgt = f"{tgt_state}@t{t_next}"
        else:
            t_next = int(e["t_next"])
        nodes[src] = {
            "id": src,
            "kind": "own_state",
            "label": e["own_state_id"],
            "time": int(e["t"]),
            "state_id": e["own_state_id"],
            "opening_id": opening_id,
        }
        nodes[tgt] = {
            "id": tgt,
            "kind": "own_state",
            "label": str(tgt_state),
            "time": t_next,
            "state_id": str(tgt_state),
            "opening_id": opening_id,
        }
        graph_edges.append(
            {
                "edge_id": e.get("edge_id"),
                "source": src,
                "target": tgt,
                "opponent_condition": e.get("opp_state_id"),
                "response_id": e.get("response_id"),
                "next_state": str(tgt_state),
                "support": int(e.get("support") or 0),
                "transition_probability": float(e.get("p_response") or 0),
                "win_enrichment": float(e.get("win_enrichment") or 0),
                "loss_enrichment": float(e.get("loss_enrichment") or 0),
                "adjusted_value": float(e.get("adjusted_lift") or 0),
                "edge_label": e.get("edge_label"),
                "source_time": int(e["t"]),
                "target_time": t_next,
            }
        )

    # link opening to earliest states
    earliest_t = None
    earliest_states = set()
    for n in nodes.values():
        if n["kind"] != "own_state":
            continue
        if earliest_t is None or n["time"] < earliest_t:
            earliest_t = n["time"]
            earliest_states = {n["id"]}
        elif n["time"] == earliest_t:
            earliest_states.add(n["id"])
    for sid in earliest_states:
        graph_edges.append(
            {
                "edge_id": f"synthetic_open_{opening_id}_{sid}",
                "source": f"OPEN::{opening_id}",
                "target": sid,
                "opponent_condition": None,
                "response_id": None,
                "next_state": nodes[sid]["state_id"],
                "support": 0,
                "transition_probability": 1.0,
                "win_enrichment": 0.0,
                "loss_enrichment": 0.0,
                "adjusted_value": 0.0,
                "edge_label": "default",
                "source_time": 0,
                "target_time": nodes[sid]["time"],
            }
        )

    meta = catalog_openings.get(opening_id.split("_")[0], {}).get(opening_id) if False else None
    # catalog is nested by matchup
    opening_meta = {}
    return {
        "opening_id": opening_id,
        "nodes": list(nodes.values()),
        "edges": graph_edges,
        "opening_meta": opening_meta,
    }


def run_stage09(cfg: PipelineConfig, edges: pd.DataFrame | None = None) -> dict[str, Any]:
    out_dir = ensure_dir(cfg.stage_dir(9, "09_graphs"))
    if cfg.resume and (out_dir / "graph_index.json").exists():
        print(f"[stage09] resume {out_dir}", flush=True)
        return {"index": __import__("json").loads((out_dir / "graph_index.json").read_text())}

    if edges is None:
        edges = pd.read_parquet(cfg.stage_dir(8, "08_transition_value") / "edge_values.parquet")
    # need t_next on edges
    transitions = pd.read_parquet(cfg.stage_dir(7, "07_transitions") / "transition_table.parquet")
    if not edges.empty and not transitions.empty:
        tnext = (
            transitions.groupby(["opening_id", "own_state_id", "opp_state_id", "t", "response_id"])["t_next"]
            .agg(lambda s: int(s.value_counts().index[0]))
            .reset_index()
        )
        edges = edges.merge(
            tnext,
            on=["opening_id", "own_state_id", "opp_state_id", "t", "response_id"],
            how="left",
        )

    catalog = __import__("json").loads(
        (cfg.stage_dir(4, "04_openings") / "opening_catalog.json").read_text()
    )
    fig_dir = ensure_dir(cfg.figures_dir("graphs"))
    index = {}
    validation = {}

    all_openings = [
        opening_id
        for matchup_items in catalog.values()
        for opening_id in matchup_items
    ]
    for opening_id in all_openings:
        g = (
            edges[edges["opening_id"] == opening_id]
            if not edges.empty
            else pd.DataFrame()
        )
        full = _build_graph_for_opening(opening_id, g, catalog)
        pruned_edges_df = _prune_edges(g)
        pruned = _build_graph_for_opening(opening_id, pruned_edges_df, catalog)
        # enrich opening meta from catalog
        for mu, items in catalog.items():
            if opening_id in items:
                full["opening_meta"] = items[opening_id]
                pruned["opening_meta"] = items[opening_id]
                break

        full_path = out_dir / f"strategy_graph_full_{opening_id}.json"
        pruned_path = out_dir / f"strategy_graph_pruned_{opening_id}.json"
        write_json(full_path, full)
        write_json(pruned_path, pruned)
        errs = validate_graph(pruned)
        validation[opening_id] = errs
        index[opening_id] = {
            "full": str(full_path.relative_to(cfg.output_root)),
            "pruned": str(pruned_path.relative_to(cfg.output_root)),
            "n_nodes_full": len(full["nodes"]),
            "n_edges_full": len(full["edges"]),
            "n_nodes_pruned": len(pruned["nodes"]),
            "n_edges_pruned": len(pruned["edges"]),
            "validation_errors": errs,
        }
        try:
            plot_graph_summary(pruned["nodes"], pruned["edges"], fig_dir / f"strategy_graph_{opening_id}")
            # plot data
            pd.DataFrame(pruned["nodes"]).to_csv(
                cfg.figures_dir("data") / f"graph_plot_nodes_{opening_id}.csv", index=False
            )
            pd.DataFrame(pruned["edges"]).to_csv(
                cfg.figures_dir("data") / f"graph_plot_edges_{opening_id}.csv", index=False
            )
        except Exception as exc:
            print(f"[stage09] plot warn {opening_id}: {exc}", flush=True)

    write_json(out_dir / "graph_index.json", index)
    write_json(out_dir / "graph_validation.json", validation)
    print(f"[stage09] graphs={len(index)}", flush=True)
    return {"index": index}
