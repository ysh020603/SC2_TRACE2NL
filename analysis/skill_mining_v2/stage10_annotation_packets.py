"""Stage 10 — build LLM annotation packets (no LLM calls)."""

from __future__ import annotations

from typing import Any

import pandas as pd

from analysis.skill_mining_v2.common.io import ensure_dir, read_json, write_json
from analysis.skill_mining_v2.config import PipelineConfig


def _knowledge_neighborhood(
    entities: set[str], action_index: dict[str, Any], max_per_rel: int = 8
) -> dict[str, Any]:
    out = {}
    for ent in entities:
        if ent in action_index:
            payload = {}
            for k, vals in action_index[ent].items():
                payload[k] = list(vals)[:max_per_rel]
            out[ent] = payload
            # 1-hop expand
            for vals in list(payload.values()):
                for v in vals[:3]:
                    if v in action_index and v not in out:
                        out[v] = {kk: list(vv)[:4] for kk, vv in action_index[v].items()}
    return out


def run_stage10(cfg: PipelineConfig) -> dict[str, Any]:
    out_dir = ensure_dir(cfg.stage_dir(10, "10_annotation_packets"))
    if cfg.resume and (out_dir / "packet_index.json").exists():
        print(f"[stage10] resume {out_dir}", flush=True)
        return {"index": read_json(out_dir / "packet_index.json")}

    catalog = read_json(cfg.stage_dir(4, "04_openings") / "opening_catalog.json")
    medoids = read_json(cfg.stage_dir(4, "04_openings") / "opening_medoid.json")
    state_catalog = read_json(cfg.stage_dir(6, "06_states") / "state_catalog.json")
    response_clusters = read_json(cfg.stage_dir(7, "07_transitions") / "response_clusters.json")
    edges = pd.read_parquet(cfg.stage_dir(8, "08_transition_value") / "edge_values.parquet")
    graph_index = read_json(cfg.stage_dir(9, "09_graphs") / "graph_index.json")
    action_index = read_json(cfg.stage_dir(2, "02_semantics") / "action_semantic_index.json")

    index = {}
    for opening_id, ginfo in graph_index.items():
        pruned = read_json(cfg.output_root / ginfo["pruned"])
        g_edges = edges[edges["opening_id"] == opening_id] if len(edges) else edges
        preferred = g_edges[g_edges["edge_label"] == "preferred"].to_dict(orient="records")
        harmful = g_edges[g_edges["edge_label"] == "harmful"].to_dict(orient="records")
        default = g_edges[g_edges["edge_label"] == "default"].to_dict(orient="records")

        # entities from responses
        entities: set[str] = set()
        for rid in set(g_edges["response_id"].astype(str)) if len(g_edges) else set():
            for item in (response_clusters.get(rid) or {}).get("top_actions") or []:
                if isinstance(item, dict) and item.get("name"):
                    entities.add(item["name"])

        opening_meta = None
        for mu, items in catalog.items():
            if opening_id in items:
                opening_meta = items[opening_id]
                break

        own_states = {
            e.get("own_state_id"): state_catalog.get("own", {}).get(e.get("own_state_id"))
            for e in preferred + harmful + default
            if e.get("own_state_id")
        }
        opp_states = {
            e.get("opp_state_id"): state_catalog.get("opp", {}).get(e.get("opp_state_id"))
            for e in preferred + harmful + default
            if e.get("opp_state_id")
        }

        packet = {
            "opening_id": opening_id,
            "opening": opening_meta,
            "medoid": medoids.get(opening_id),
            "state_profiles": {"own": own_states, "opp": opp_states},
            "preferred_edges": preferred[:20],
            "default_edges": default[:20],
            "harmful_edges": harmful[:20],
            "positive_paths": [
                {
                    "from": e.get("own_state_id"),
                    "opp": e.get("opp_state_id"),
                    "response": e.get("response_id"),
                    "next": e.get("next_own_state_id"),
                    "lift": e.get("adjusted_lift"),
                }
                for e in preferred[:10]
            ],
            "negative_paths": [
                {
                    "from": e.get("own_state_id"),
                    "opp": e.get("opp_state_id"),
                    "response": e.get("response_id"),
                    "next": e.get("next_own_state_id"),
                    "lift": e.get("adjusted_lift"),
                }
                for e in harmful[:10]
            ],
            "response_clusters": {
                rid: response_clusters.get(rid)
                for rid in (
                    set(g_edges["response_id"].astype(str)) if len(g_edges) else set()
                )
            },
            "sc2_knowledge": _knowledge_neighborhood(entities, action_index),
            "graph_pruned_ref": ginfo["pruned"],
            "run_id": cfg.run_id,
            "visibility_note": "Opponent states are oracle_trace from full replay actions.",
        }
        path = out_dir / f"packet_{opening_id}.json"
        write_json(path, packet)
        index[opening_id] = str(path.relative_to(cfg.output_root))

    write_json(out_dir / "packet_index.json", index)
    print(f"[stage10] packets={len(index)}", flush=True)
    return {"index": index}
