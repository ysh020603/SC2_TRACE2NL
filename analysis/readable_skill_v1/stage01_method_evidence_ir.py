from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from .common.io import opening_ids, read_json, write_json
from .common.method_policy import policy
from .common.schemas import validate_ir
from .config import PipelineConfig, RACE


def _catalog_lookup(catalog: dict, opening_id: str) -> dict:
    return (catalog.get(opening_id[:3]) or {}).get(opening_id) or {}


def _state_payload(state_catalog: dict, side: str, state_id: str | None) -> dict:
    if not state_id:
        return {}
    return dict((state_catalog.get(side) or {}).get(state_id) or {"state_id": state_id, "profile": {}})


def _normal_edges(cfg: PipelineConfig, opening_id: str, method: str) -> list[dict]:
    graph_name = "full" if method in {"ablation_frequency_only", "ablation_static_population"} else "pruned"
    path = cfg.input_root / "09_graphs" / f"strategy_graph_{graph_name}_{opening_id}.json"
    graph = read_json(path)
    edges = [e for e in graph.get("edges", []) if e.get("response_id") and not str(e.get("edge_id", "")).startswith("synthetic_")]
    if method == "ablation_positive_only":
        edges = [e for e in edges if e.get("edge_label") != "harmful"]
    if method == "ablation_frequency_only":
        grouped: dict[tuple, list[dict]] = defaultdict(list)
        for edge in edges:
            grouped[(edge.get("source"), edge.get("opponent_condition"), edge.get("source_time"))].append(edge)
        edges = [max(items, key=lambda x: (float(x.get("transition_probability") or 0), int(x.get("support") or 0))) for items in grouped.values()]
    if method == "ablation_static_population":
        grouped = defaultdict(list)
        for edge in edges:
            grouped[(edge.get("source"), edge.get("source_time"))].append(edge)
        edges = [max(items, key=lambda x: (float(x.get("transition_probability") or 0), int(x.get("support") or 0))) for items in grouped.values()]
    return edges


def _single_trace(cfg: PipelineConfig, opening_id: str, bulk: tuple | None = None) -> tuple[dict, list[dict], list[dict]]:
    import pandas as pd

    if bulk is None:
        assignments = pd.read_parquet(cfg.input_root / "04_openings" / "opening_assignments.parquet", filters=[("opening_id", "=", opening_id)])
        state_frame = None
    else:
        assignments, state_frame = bulk
        assignments = assignments[assignments["opening_id"] == opening_id]
    winners = assignments[assignments["is_win"] == 1]
    chosen = (winners if not winners.empty else assignments).sort_values(["replay_id", "player_id"]).iloc[0]
    replay_id, player_id = str(chosen["replay_id"]), int(chosen["player_id"])
    cols = ["replay_id", "player_id", "opening_id", "t", "own_state_id", "own_cum_economy", "own_cum_production", "own_cum_technology", "own_cum_ground", "own_cum_air", "own_cum_defense", "own_cum_upgrade", "own_cum_expansion", "own_ordered_combat", "own_ordered_air", "own_ordered_tech"]
    if state_frame is None:
        states = pd.read_parquet(cfg.input_root / "06_states" / "state_assignments.parquet", columns=cols, filters=[("opening_id", "=", opening_id), ("replay_id", "=", replay_id), ("player_id", "=", player_id)])
    else:
        states = state_frame[(state_frame["opening_id"] == opening_id) & (state_frame["replay_id"].astype(str) == replay_id) & (state_frame["player_id"] == player_id)]
    states = states.sort_values("t")
    own_states, transitions = [], []
    records = states.to_dict("records")
    for row in records:
        profile = {k: row.get(k) for k in row if k.startswith("own_cum_")}
        own_states.append({"state_id": row.get("own_state_id"), "time": int(row["t"]), "profile": profile, "representative_cues": [row.get("own_ordered_combat"), row.get("own_ordered_air"), row.get("own_ordered_tech")]})
    for current, nxt in zip(records, records[1:]):
        transitions.append({"source_state_id": current.get("own_state_id"), "opponent_state_id": None, "next_state_id": nxt.get("own_state_id"), "phase": [int(current["t"]), int(nxt["t"])], "statistical_label": "trace", "response_id": None, "response_cluster_features": {}, "support": 1, "value_fields": {}, "source_trace": {"replay_id": replay_id, "player_id": player_id}})
    return {"replay_id": replay_id, "player_id": player_id, "is_win": int(chosen["is_win"])}, own_states, transitions


def build_ir(cfg: PipelineConfig, opening_id: str, method: str, catalog: dict, states: dict, responses: dict, single_trace_bulk: tuple | None = None) -> dict:
    race, opponent_race = RACE[opening_id[0]], RACE[opening_id[2]]
    allowed = policy(method)
    opening = _catalog_lookup(catalog, opening_id)
    if method == "ablation_single_trace":
        source_trace, own_states, transitions = _single_trace(cfg, opening_id, single_trace_bulk)
        opening_evidence = {"opening_id": opening_id, "source_trace": source_trace}
        opponent_states = []
        source_files = ["04_openings/opening_assignments.parquet", "06_states/state_assignments.parquet"]
    else:
        raw_edges = _normal_edges(cfg, opening_id, method)
        transitions, own_ids, opp_ids = [], set(), set()
        for edge in raw_edges:
            source_id = str(edge.get("source") or "").split("@t", 1)[0]
            next_id = edge.get("next_state") if allowed["graph"] else None
            opponent_id = edge.get("opponent_condition") if allowed["opponent"] else None
            raw_label = edge.get("edge_label") or "default"
            if method == "ablation_frequency_only":
                raw_label = "frequency"
            elif method == "ablation_static_population":
                raw_label = "default"
            value_fields = {}
            if allowed["value"]:
                value_fields = {"adjusted_lift": edge.get("adjusted_value"), "win_enrichment": edge.get("win_enrichment"), "loss_enrichment": edge.get("loss_enrichment")}
            response = responses.get(edge.get("response_id")) or {}
            transitions.append({
                "source_state_id": source_id, "opponent_state_id": opponent_id, "next_state_id": next_id,
                "phase": [int(edge.get("source_time") or 0), int(edge.get("target_time") or int(edge.get("source_time") or 0) + 60)],
                "statistical_label": raw_label, "response_id": edge.get("response_id"),
                "response_cluster_features": {
                    "profile": response.get("profile") or {},
                    "representative_names": [x.get("name") for x in (response.get("top_actions") or []) if isinstance(x, dict)][:12],
                },
                "support": int(edge.get("support") or 0),
                "frequency": float(edge.get("transition_probability") or 0), "value_fields": value_fields,
                "source_edge_id": edge.get("edge_id"),
            })
            own_ids.add(source_id)
            if next_id:
                own_ids.add(str(next_id))
            if opponent_id:
                opp_ids.add(str(opponent_id))
        own_states = [_state_payload(states, "own", x) for x in sorted(own_ids)]
        opponent_states = [_state_payload(states, "opp", x) for x in sorted(opp_ids)]
        opening_evidence = opening if allowed["population"] else {"opening_id": opening_id}
        source_files = [f"09_graphs/strategy_graph_{'full' if method in {'ablation_frequency_only', 'ablation_static_population'} else 'pruned'}_{opening_id}.json", "06_states/state_catalog.json", "07_transitions/response_clusters.json"]
    payload = {
        "method": method, "opening_id": opening_id, "race": race, "opponent_race": opponent_race,
        "opening_evidence": opening_evidence, "own_states": own_states, "opponent_states": opponent_states,
        "transitions": transitions, "allowed_information": allowed,
        "provenance": {"source_files": source_files, "method_boundary_applied_before_annotation": True},
    }
    validate_ir(payload)
    return payload


def run(cfg: PipelineConfig) -> dict:
    catalog = read_json(cfg.input_root / "04_openings" / "opening_catalog.json")
    states = read_json(cfg.input_root / "06_states" / "state_catalog.json")
    responses = read_json(cfg.input_root / "07_transitions" / "response_clusters.json")
    selected = list(cfg.openings) or opening_ids(cfg.input_root)
    single_trace_bulk = None
    if "ablation_single_trace" in cfg.methods:
        import pandas as pd
        assignments = pd.read_parquet(cfg.input_root / "04_openings" / "opening_assignments.parquet")
        assignments = assignments[assignments["opening_id"].isin(selected)]
        chosen_keys = []
        for opening_id in selected:
            group = assignments[assignments["opening_id"] == opening_id]
            winners = group[group["is_win"] == 1]
            row = (winners if not winners.empty else group).sort_values(["replay_id", "player_id"]).iloc[0]
            chosen_keys.append((opening_id, str(row["replay_id"]), int(row["player_id"])))
        replay_ids = sorted({replay for _, replay, _ in chosen_keys})
        cols = ["replay_id", "player_id", "opening_id", "t", "own_state_id", "own_cum_economy", "own_cum_production", "own_cum_technology", "own_cum_ground", "own_cum_air", "own_cum_defense", "own_cum_upgrade", "own_cum_expansion", "own_ordered_combat", "own_ordered_air", "own_ordered_tech"]
        state_frame = pd.read_parquet(cfg.input_root / "06_states" / "state_assignments.parquet", columns=cols, filters=[("replay_id", "in", replay_ids)])
        single_trace_bulk = (assignments, state_frame)
    index = {}
    for method in cfg.methods:
        for opening_id in selected:
            out = cfg.stage_dir(1) / method / f"{opening_id}.json"
            if not (cfg.resume and out.exists()):
                write_json(out, build_ir(cfg, opening_id, method, catalog, states, responses, single_trace_bulk))
            index.setdefault(method, {})[opening_id] = str(out.relative_to(cfg.output_root))
    write_json(cfg.stage_dir(1) / "index.json", index)
    return index
