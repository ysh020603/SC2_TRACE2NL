from __future__ import annotations

from collections import defaultdict

from .common.io import read_json, write_json
from .common.method_policy import policy
from .common.obs_vocabulary import combat_cues, load_vocabulary, split_names
from .common.schemas import validate_projection
from .config import PipelineConfig


def _phase(seconds: int) -> str:
    if seconds < 240:
        return "early_game"
    if seconds < 420:
        return "early_midgame"
    if seconds < 600:
        return "midgame"
    return "late_midgame"


def _level(value: float, low: float = 0.08, high: float = 0.35) -> str:
    if value >= high:
        return "heavy"
    if value >= low:
        return "moderate"
    return "light_or_uncertain"


def _profile_value(profile: dict, side: str, family: str) -> float:
    for key in (f"{side}_cum_{family}", f"{side}_recent_{family}"):
        if key in profile:
            return float(profile.get(key) or 0)
    return 0.0


def _state_projection(state: dict, side: str, race: str, raw: dict, vocabulary: dict) -> dict:
    profile = state.get("profile") or {}
    ground, air = _profile_value(profile, side, "ground"), _profile_value(profile, side, "air")
    if air > max(0.08, ground * 1.15):
        domain = "air"
    elif ground > max(0.08, air * 1.15):
        domain = "ground"
    elif ground + air > 0.08:
        domain = "mixed"
    else:
        domain = "unknown"
    names = []
    for value in raw.values():
        names.extend(split_names(value, vocabulary))
    names.extend(split_names(state.get("representative_cues"), vocabulary))
    cues = combat_cues(names, vocabulary, race)
    cue_text = ", ".join(cues) if cues else "no reliably grounded combat-unit cue"
    production = _level(_profile_value(profile, side, "production"))
    technology = _level(_profile_value(profile, side, "technology"))
    defense = _level(_profile_value(profile, side, "defense"), 0.05, 0.2)
    if side == "opp":
        summary = f"Enemy Intelligence is consistent with a {domain} posture; representative observed or remembered cues may include {cue_text}. Production appears {production}, technology investment appears {technology}, and exact hidden counts remain unknown."
    else:
        summary = f"Your completed or developing posture is broadly {domain}-oriented, with {production} production and {technology} technology investment. Check live Completed, Under Construction, Active Queues, resources, supply, and army strength before choosing exact actions."
    return {
        "state_id": state.get("state_id"), "side": "opponent" if side == "opp" else "own",
        "phase": _phase(int(str(state.get("state_id", "T0")).split("_T")[-1].split("_")[0]) if "_T" in str(state.get("state_id")) else 0),
        "army_domain": domain, "army_style": f"{domain}_macro_posture" if domain != "unknown" else "unknown",
        "representative_unit_cues": [{"unit": name, "strength": "representative"} for name in cues],
        "air_presence": _level(air), "production_posture": production, "technology_posture": technology,
        "economy_posture": _level(_profile_value(profile, side, "economy")),
        "expansion_posture": _level(_profile_value(profile, side, "expansion"), 0.03, 0.15),
        "defense_posture": defense, "pressure_posture": "possible" if domain != "unknown" else "unknown",
        "special_threats": [], "confidence": "medium" if profile else "low",
        "obs_style_summary_seed": {"enemy_intelligence" if side == "opp" else "own_posture": summary},
        "source_state_ids": [state.get("state_id")],
    }


def _sample_raw_states(cfg: PipelineConfig, opening_id: str) -> dict[str, dict]:
    try:
        import json
        import pandas as pd
        columns = ["replay_id", "player_id", "opening_id", "t", "own_state_id", "opp_state_id"]
        frame = pd.read_parquet(cfg.input_root / "06_states" / "state_assignments.parquet", columns=columns, filters=[("opening_id", "=", opening_id)])
    except Exception:
        return {}
    representatives = []
    for side in ("own", "opp"):
        for row in frame.drop_duplicates(f"{side}_state_id").to_dict("records"):
            row = dict(row)
            row["side"] = side
            row["state_id"] = row.get(f"{side}_state_id")
            representatives.append(row)
    replay_cache = {}
    result = {}
    for row in representatives:
        replay_id = str(row["replay_id"])
        if replay_id not in replay_cache:
            matches = list((cfg.repo_root / "data" / "action_json").glob(f"*/{replay_id}.json"))
            replay_cache[replay_id] = json.loads(matches[0].read_text(encoding="utf-8")) if matches else {}
        replay = replay_cache[replay_id]
        players = replay.get("players") or []
        perspective_id = int(row["player_id"])
        player = next((x for x in players if int(x.get("player_id") or -1) == perspective_id), None) if row["side"] == "own" else next((x for x in players if int(x.get("player_id") or -1) != perspective_id), None)
        if not player:
            continue
        actions = player.get("build_order") or []
        names = [str(action.get("name")) for action in actions if isinstance(action, dict) and float(action.get("second") or 0) <= float(row["t"]) and action.get("name")]
        result[str(row["state_id"])] = {"grounded_names_before_phase": " ".join(names)}
    return result


def _direction(value: float, strong: float = 0.12) -> str:
    if value >= strong:
        return "increase"
    if value > 0.025:
        return "continue"
    return "maintain"


def _policy_signature(features: dict) -> dict:
    profile = features.get("profile") or features
    get = lambda name: float(profile.get(f"resp_d_{name}") or 0)
    return {
        "economy_direction": _direction(get("economy")), "expansion_direction": _direction(get("expansion"), 0.04),
        "production_direction": _direction(get("production"), 0.08), "technology_direction": _direction(get("technology"), 0.1),
        "army_direction": "strengthen_air" if get("air") > get("ground") else "strengthen_ground" if get("ground") > 0.03 else "maintain_current_army_path",
        "air_direction": _direction(get("air"), 0.06), "upgrade_direction": _direction(get("upgrade"), 0.05),
        "defense_direction": _direction(get("defense"), 0.05), "tempo": "stabilize_then_develop" if get("defense") + get("production") > get("economy") else "develop_with_safety_checks",
        "confidence": "medium",
    }


def _opening_projection(ir: dict) -> dict:
    evidence = ir.get("opening_evidence") or {}
    profile = evidence.get("profile") or {}
    ranked = sorted(((key.removeprefix("inv_"), float(value or 0)) for key, value in profile.items() if key.startswith("inv_")), key=lambda x: -x[1])
    primary = [name for name, value in ranked[:3] if value > 0]
    family = " / ".join(primary) if primary else "balanced macro"
    return {
        "opening_name_seed": f"{ir['opening_id']} {family.title()}", "opening_family_seed": f"{family} opening",
        "strategic_goal_seed": f"Develop a {family} posture while preserving flexibility for live observation-driven adaptation.",
        "economy_character": _level(float(profile.get("inv_economy") or 0)),
        "production_character": _level(float(profile.get("inv_production") or 0)),
        "technology_character": _level(float(profile.get("inv_technology") or 0)),
        "army_character": "air-leaning" if float(profile.get("inv_air") or 0) > float(profile.get("inv_ground") or 0) else "ground-leaning",
        "flexibility_note": "This is a strategic template, not a fixed build order.",
    }


def build_projection(cfg: PipelineConfig, ir: dict, vocabulary: dict, raw: dict[str, dict] | None = None) -> dict:
    method, opening_id = ir["method"], ir["opening_id"]
    raw = _sample_raw_states(cfg, opening_id) if raw is None else raw
    projections = {}
    for state in ir.get("own_states", []):
        projections[state.get("state_id")] = _state_projection(state, "own", ir["race"], raw.get(str(state.get("state_id")), {}), vocabulary)
    for state in ir.get("opponent_states", []):
        projections[state.get("state_id")] = _state_projection(state, "opp", ir["opponent_race"], raw.get(str(state.get("state_id")), {}), vocabulary)
    labels = policy(method)["labels"]
    candidates = []
    for transition in ir.get("transitions", []):
        raw_label = transition.get("statistical_label")
        badge = labels.get(raw_label)
        if not badge:
            continue
        own = projections.get(transition.get("source_state_id")) or {}
        opp = projections.get(transition.get("opponent_state_id")) or {}
        signature = _policy_signature(transition.get("response_cluster_features") or {})
        candidates.append({
            "node_type": badge, "phase": _phase(int((transition.get("phase") or [0])[0])),
            "own_state": own, "opponent_state": opp if policy(method)["opponent"] else {},
            "policy_signature": signature, "support": int(transition.get("support") or 0),
            "frequency": float(transition.get("frequency") or 0), "next_state_id": transition.get("next_state_id"),
            "source_state_id": transition.get("source_state_id"),
            "source_state_ids": [transition.get("source_state_id")],
            "source_edge_ids": [transition.get("source_edge_id")] if transition.get("source_edge_id") else [],
        })
    # Consolidate only compatible sign/phase/opponent domain/policy direction groups.
    groups = {}
    for node in candidates:
        key = (node["node_type"], node["phase"], (node.get("opponent_state") or {}).get("army_domain", "none"), node["policy_signature"]["army_direction"], node["policy_signature"]["production_direction"])
        if key not in groups or node["support"] > groups[key]["support"]:
            groups[key] = node
        else:
            groups[key]["source_state_ids"].extend(node["source_state_ids"])
            groups[key]["source_edge_ids"].extend(node["source_edge_ids"])
    consolidated = list(groups.values())
    by_type = {}
    for node in consolidated:
        if node["node_type"] not in by_type or node["support"] > by_type[node["node_type"]]["support"]:
            by_type[node["node_type"]] = node
    selected = list(by_type.values())
    seen = {id(x) for x in selected}
    selected.extend(x for x in sorted(consolidated, key=lambda n: (n["support"], n["frequency"]), reverse=True) if id(x) not in seen)
    nodes = selected[: cfg.max_nodes]
    for index, node in enumerate(nodes, 1):
        node["node_id"] = f"N{index:03d}"
    payload = {"method": method, "opening_id": opening_id, "race": ir["race"], "opponent_race": ir["opponent_race"], "opening_projection": _opening_projection(ir), "states": projections, "nodes": nodes, "provenance": {"method_ir": f"01_method_ir/{method}/{opening_id}.json", "projection_is_observation_compatible": True, "allow_exact_obs_counts": False}}
    validate_projection(payload)
    return payload


def run(cfg: PipelineConfig) -> dict:
    index = read_json(cfg.stage_dir(1) / "index.json")
    vocabulary = load_vocabulary(cfg.input_root / "02_semantics" / "entity_index.json")
    out_index = {}
    raw_cache = {}
    for method, openings in index.items():
        for opening_id, rel in openings.items():
            out = cfg.stage_dir(2) / method / f"{opening_id}.json"
            if not (cfg.resume and out.exists()):
                if opening_id not in raw_cache:
                    raw_cache[opening_id] = _sample_raw_states(cfg, opening_id)
                write_json(out, build_projection(cfg, read_json(cfg.output_root / rel), vocabulary, raw_cache[opening_id]))
            out_index.setdefault(method, {})[opening_id] = str(out.relative_to(cfg.output_root))
    write_json(cfg.stage_dir(2) / "index.json", out_index)
    return out_index
