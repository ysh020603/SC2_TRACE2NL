"""Stage 12 — compile full signed-graph skills."""

from __future__ import annotations

from typing import Any

import pandas as pd

from analysis.skill_mining_v2.common.io import ensure_dir, estimate_tokens, read_json, write_json
from analysis.skill_mining_v2.config import RACE_CODE, PipelineConfig


def _race_paths(directional: str) -> tuple[str, str, str]:
    # TvP -> terran, Terran, Protoss
    own = RACE_CODE[directional[0]]
    opp = RACE_CODE[directional[2]]
    return own.lower(), own, opp


def _canonical_actions(response_clusters: dict[str, Any], response_id: str) -> list[str]:
    resp = response_clusters.get(response_id) or {}
    return [x["name"] for x in (resp.get("top_actions") or []) if isinstance(x, dict) and x.get("name")]


def compile_one(
    cfg: PipelineConfig,
    opening_id: str,
    packet: dict[str, Any],
    annotation: dict[str, Any],
    graph: dict[str, Any],
    response_clusters: dict[str, Any],
) -> dict[str, Any]:
    dmu = opening_id.split("_")[0]
    race_dir, race, opp_race = _race_paths(dmu)
    opening_ann = annotation.get("opening_annotation") or {}
    state_ann = annotation.get("state_annotations") or {}
    graph_edge_ids = {
        str(e.get("edge_id"))
        for e in (graph.get("edges") or [])
        if e.get("edge_id") is not None
    }

    def grounded_packet_edges(key: str) -> list[dict[str, Any]]:
        return [
            e
            for e in (packet.get(key) or [])
            if e.get("edge_id") is not None and str(e.get("edge_id")) in graph_edge_ids
        ]

    preferred_edges = grounded_packet_edges("preferred_edges")
    harmful_edges = grounded_packet_edges("harmful_edges")
    default_edges = grounded_packet_edges("default_edges")

    preferred_rules = []
    for i, e in enumerate(preferred_edges):
        own = e.get("own_state_id")
        preferred_rules.append(
            {
                "rule_id": f"{opening_id}_PREF_{i+1:02d}",
                "phase": [int(e.get("t") or 0), int(e.get("t") or 0) + 60],
                "own_state": (state_ann.get(own) or {}).get("name") or own,
                "own_state_id": own,
                "opponent_condition": (state_ann.get(e.get("opp_state_id")) or {}).get("name")
                or e.get("opp_state_id"),
                "response": e.get("response_id"),
                "canonical_actions": _canonical_actions(response_clusters, e.get("response_id")),
                "next_state": e.get("next_own_state_id"),
                "evidence_id": e.get("edge_id"),
            }
        )

    avoid_rules = []
    for i, e in enumerate(harmful_edges):
        avoid_rules.append(
            {
                "rule_id": f"{opening_id}_AVOID_{i+1:02d}",
                "phase": [int(e.get("t") or 0), int(e.get("t") or 0) + 60],
                "own_state": (state_ann.get(e.get("own_state_id")) or {}).get("name")
                or e.get("own_state_id"),
                "own_state_id": e.get("own_state_id"),
                "opponent_condition": (state_ann.get(e.get("opp_state_id")) or {}).get("name")
                or e.get("opp_state_id"),
                "avoid_response": e.get("response_id"),
                "risk_description": "Associated with comparatively worse outcomes in comparable historical contexts.",
                "evidence_id": e.get("edge_id"),
            }
        )

    default_evolution = []
    for i, e in enumerate(default_edges):
        default_evolution.append(
            {
                "step_id": f"{opening_id}_DEF_{i+1:02d}",
                "phase": [int(e.get("t") or 0), int(e.get("t") or 0) + 60],
                "own_state_id": e.get("own_state_id"),
                "response": e.get("response_id"),
                "canonical_actions": _canonical_actions(response_clusters, e.get("response_id")),
                "next_state": e.get("next_own_state_id"),
                "evidence_id": e.get("edge_id"),
            }
        )

    opening_meta = packet.get("opening") or {}
    medoid = packet.get("medoid") or {}
    skill = {
        "skill_id": opening_id,
        "opening_id": opening_id,
        "race": race,
        "opponent_race": opp_race,
        "directional_matchup": dmu,
        "method": "full_signed_graph",
        "opening": {
            "id": opening_id,
            "name": opening_ann.get("professional_name") or opening_ann.get("data_driven_name") or opening_id,
            "objective": opening_ann.get("strategic_intent") or "",
            "prototype": [
                t.strip()
                for t in (
                    (medoid.get("key_sequence") or "").split(">")
                    if medoid.get("key_sequence")
                    else []
                )
                if t.strip()
            ],
            "macro_family": opening_ann.get("macro_family"),
        },
        "default_evolution": default_evolution,
        "preferred_rules": preferred_rules,
        "avoid_rules": avoid_rules,
        "strategy_graph": "strategy_graph.json",
        "evidence": "evidence.json",
        "annotation": "annotation.json",
        "run_id": cfg.run_id,
    }

    evidence = {
        "opening": opening_meta,
        "support": int(opening_meta.get("support") or 0),
        "representative_replays": (
            [medoid.get("replay_id")] if medoid.get("replay_id") else []
        ),
        "preferred_edges": preferred_edges,
        "harmful_edges": harmful_edges,
        "default_edges": default_edges,
        "positive_paths": packet.get("positive_paths"),
        "negative_paths": packet.get("negative_paths"),
        "visibility": "oracle_trace",
    }
    return {
        "skill": skill,
        "evidence": evidence,
        "graph": graph,
        "annotation": annotation,
        "race_dir": race_dir,
        "matchup_dir": dmu,
    }


def run_stage12(cfg: PipelineConfig) -> dict[str, Any]:
    out_dir = ensure_dir(cfg.stage_dir(12, "12_skills"))
    skill_root = ensure_dir(cfg.skill_root / "full_signed_graph")
    packet_index = read_json(cfg.stage_dir(10, "10_annotation_packets") / "packet_index.json")
    ann_index = read_json(cfg.stage_dir(11, "11_annotations") / "annotation_index.json")
    graph_index = read_json(cfg.stage_dir(9, "09_graphs") / "graph_index.json")
    response_clusters = read_json(cfg.stage_dir(7, "07_transitions") / "response_clusters.json")

    catalog_rows = []
    index = {}
    for opening_id, rel in packet_index.items():
        packet = read_json(cfg.output_root / rel)
        annotation = read_json(cfg.output_root / ann_index[opening_id])
        ginfo = graph_index.get(opening_id) or {}
        graph = read_json(cfg.output_root / ginfo["pruned"]) if ginfo.get("pruned") else {"nodes": [], "edges": []}
        compiled = compile_one(cfg, opening_id, packet, annotation, graph, response_clusters)
        dest = ensure_dir(skill_root / compiled["race_dir"] / compiled["matchup_dir"] / opening_id)
        write_json(dest / "skill.json", compiled["skill"])
        write_json(dest / "evidence.json", compiled["evidence"])
        write_json(dest / "strategy_graph.json", compiled["graph"])
        write_json(dest / "annotation.json", compiled["annotation"])
        write_json(
            dest / "validation_report.json",
            {
                "skill_id": opening_id,
                "n_preferred": len(compiled["skill"]["preferred_rules"]),
                "n_avoid": len(compiled["skill"]["avoid_rules"]),
                "n_default": len(compiled["skill"]["default_evolution"]),
                "token_estimate": estimate_tokens(compiled["skill"]),
            },
        )
        # also mirror under analysis outputs
        mirror = ensure_dir(out_dir / compiled["race_dir"] / compiled["matchup_dir"] / opening_id)
        for name in ("skill.json", "evidence.json", "strategy_graph.json", "annotation.json", "validation_report.json"):
            write_json(mirror / name, read_json(dest / name))

        index[opening_id] = str(dest.relative_to(cfg.repo_root))
        catalog_rows.append(
            {
                "skill_id": opening_id,
                "race": compiled["skill"]["race"],
                "opponent_race": compiled["skill"]["opponent_race"],
                "name": compiled["skill"]["opening"]["name"],
                "n_preferred": len(compiled["skill"]["preferred_rules"]),
                "n_avoid": len(compiled["skill"]["avoid_rules"]),
                "n_default": len(compiled["skill"]["default_evolution"]),
                "graph_nodes": len(graph.get("nodes") or []),
                "graph_edges": len(graph.get("edges") or []),
                "path": index[opening_id],
            }
        )

    write_json(out_dir / "skill_index.json", index)
    cat_df = pd.DataFrame(catalog_rows)
    if len(cat_df):
        cat_df.to_csv(out_dir / "skill_catalog.csv", index=False)
    lines = ["# Skill Catalog (Full Signed Graph)", ""]
    for row in catalog_rows:
        lines.append(
            f"- `{row['skill_id']}` {row['name']}: pref={row['n_preferred']} avoid={row['n_avoid']} "
            f"default={row['n_default']} graph={row['graph_nodes']}n/{row['graph_edges']}e"
        )
    (out_dir / "skill_catalog.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[stage12] skills={len(index)}", flush=True)
    return {"index": index}
