from __future__ import annotations

import json
import re

from .common.io import read_json, write_json
from .common.method_policy import policy
from .config import LLM_MODEL_KEY, PipelineConfig

SYSTEM = """You are compiling reusable strategic knowledge for an SC2 macro decision-making agent.
This is NOT a build-order generation task. Do not output an ordered action list, replay actions, canonical action sequences, exact unseen counts, oracle state IDs, cluster IDs, or causal claims. Use natural-language situation, direction, trade-off, risk, adaptation, and transition goals. Opponent descriptions must use partial-observation wording compatible with Enemy Intelligence. The statistical node_type is supplied by the pipeline and is immutable. Historical association is not causality. Return strict JSON only."""


def _json_object(text: str) -> dict:
    try:
        return json.loads(text)
    except Exception:
        match = re.search(r"\{[\s\S]*\}", text or "")
        if match:
            try:
                return json.loads(match.group())
            except Exception:
                pass
    return {}


def _direction_text(signature: dict) -> str:
    army = signature.get("army_direction", "maintain_current_army_path").replace("_", " ")
    production = signature.get("production_direction", "maintain").replace("_", " ")
    economy = signature.get("economy_direction", "maintain").replace("_", " ")
    return f"{army.capitalize()} while keeping production on a {production} course and economy on a {economy} course; reconcile the exact choice with the live observation."


def _fallback(projection: dict) -> dict:
    method = projection["method"]
    opening = projection["opening_projection"]
    if method == "ablation_single_trace":
        summary = "This opening is distilled from one representative human trajectory and preserves its broad macro phases without turning them into a fixed sequence."
    elif method == "ablation_frequency_only":
        summary = "This opening summarizes common historical macro patterns; frequency describes recurrence and does not express an outcome judgment."
    elif method == "ablation_static_population":
        summary = "This opening summarizes common macro posture and phase continuation across the historical sample without adaptive enemy-conditioned rules."
    else:
        summary = opening["strategic_goal_seed"] + " Historical associations guide re-evaluation but do not establish causality."
    annotations = []
    for node in projection.get("nodes", []):
        node_type = node["node_type"]
        own = ((node.get("own_state") or {}).get("obs_style_summary_seed") or {}).get("own_posture", "Use the live observation to assess the current macro posture.")
        opp = ((node.get("opponent_state") or {}).get("obs_style_summary_seed") or {}).get("enemy_intelligence", "")
        domain = (node.get("opponent_state") or {}).get("army_domain", "current")
        direction = _direction_text(node.get("policy_signature") or {})
        if method == "ablation_single_trace":
            trigger = f"The live posture resembles the {node['phase'].replace('_', ' ')} phase represented by this trajectory."
            title = f"Continue the {node['phase'].replace('_', ' ')} trajectory phase"
        elif method == "ablation_static_population":
            trigger = f"Your live posture resembles a common {node['phase'].replace('_', ' ')} stage of this opening."
            title = f"Common {node['phase'].replace('_', ' ')} continuation"
        else:
            trigger = opp or f"Enemy Intelligence does not yet show a dominant signal during the {node['phase'].replace('_', ' ')}."
            title = f"{node_type.title()} response to {domain} posture"
        risk = "Avoid deepening this direction until the live army, production, queues, supply, and threat flags have been rechecked." if node_type == "negative" else "Do not treat this direction as a command or ignore current resources, prerequisites, supply, queues, or threats."
        annotations.append({
            "node_id": node["node_id"], "node_type": node_type, "title": title,
            "trigger_summary": trigger, "own_situation": own, "opponent_situation": opp,
            "decision_direction": direction, "strategic_reason": "This direction matches the retained evidence boundary for the current method and should be reassessed against the live observation.",
            "avoid_direction": risk, "transition_goal": "Reach a stable posture where the next economy, production, technology, and army trade-off can be re-evaluated from current information.",
            "exit_or_recheck_condition": "Recheck when Enemy Intelligence, army posture, resources, supply, Completed, Under Construction, or Active Queues materially change.",
            "next_state_summary": "A later observable posture may warrant a separate node." if policy(method)["graph"] else "",
        })
    return {
        "opening": {
            "opening_name": opening["opening_name_seed"], "opening_family": opening["opening_family_seed"],
            "opening_summary": summary, "strategic_goal": opening["strategic_goal_seed"],
            "economy_character": opening["economy_character"], "production_character": opening["production_character"],
            "technology_character": opening["technology_character"], "army_character": opening["army_character"],
            "flexibility_note": opening["flexibility_note"],
        },
        "nodes": annotations,
    }


def _valid_response(payload: dict, projection: dict) -> bool:
    expected = {node["node_id"]: node["node_type"] for node in projection.get("nodes", [])}
    actual = {node.get("node_id"): node.get("node_type") for node in payload.get("nodes", []) if isinstance(node, dict)}
    if not (isinstance(payload.get("opening"), dict) and actual == expected):
        return False
    blob = json.dumps(payload, ensure_ascii=False).lower()
    forbidden = {
        "ablation_single_trace": ("population", "positive", "negative", "preferred", "harmful"),
        "ablation_static_population": ("positive", "negative", "preferred", "harmful"),
        "ablation_flat_adaptive": ("possible next", "next node", "graph successor", "multi-hop"),
        "ablation_positive_only": ("negative", "harmful", "worse outcome"),
        "ablation_frequency_only": ("positive", "preferred", "better outcome", "adjusted lift", "win enrichment"),
    }.get(projection["method"], ())
    return not any(term in blob for term in forbidden)


def _call(projection: dict) -> tuple[dict, dict]:
    from API_Tools.llm_caller import call_openai_detailed, load_agent_pool

    pool = (load_agent_pool().get("llm_agents_pool") or {}).get(LLM_MODEL_KEY) or {}
    if pool.get("is_reasoning") is not False:
        raise RuntimeError("API_config/config.json must mark DeepSeek-V4-flash as is_reasoning=false")
    method = projection["method"]
    contract = {
        "opening": {"opening_name": "", "opening_family": "", "opening_summary": "", "strategic_goal": "", "economy_character": "", "production_character": "", "technology_character": "", "army_character": "", "flexibility_note": ""},
        "nodes": [{"node_id": n["node_id"], "node_type": n["node_type"], "title": "", "trigger_summary": "", "own_situation": "", "opponent_situation": "", "decision_direction": "", "strategic_reason": "", "avoid_direction": "", "transition_goal": "", "exit_or_recheck_condition": "", "next_state_summary": ""} for n in projection.get("nodes", [])],
    }
    user = json.dumps({
        "method": method, "information_boundary": policy(method),
        "method_specific_rules": {
            "ablation_single_trace": "Never mention population, positive, negative, preferred, harmful, or adaptive comparison.",
            "ablation_static_population": "Use only own phase/posture triggers; never claim opponent-conditioned evidence or value signs.",
            "ablation_flat_adaptive": "Never mention graph paths, successors, next nodes, or multi-hop guidance.",
            "ablation_positive_only": "Never mention removed negative, harmful, or worse-outcome evidence.",
            "ablation_frequency_only": "Never call frequent evidence positive, preferred, best, better, or outcome-improving.",
        }.get(method, "Preserve positive, negative, and default signs exactly."),
        "projection": projection, "required_output": contract,
    }, ensure_ascii=False)
    result = call_openai_detailed(messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}], model_key=LLM_MODEL_KEY, is_reasoning=False, temperature=0.2, max_tokens=7000, response_format={"type": "json_object"}, timeout=180)
    parsed = _json_object(result.get("content") or "")
    metadata = {"model_key": result.get("model_key"), "model": result.get("model"), "is_reasoning": result.get("is_reasoning"), "reasoning_present": bool(result.get("reasoning")), "reasoning_source": result.get("reasoning_source"), "error": result.get("error") or ""}
    return parsed, metadata


def annotate(cfg: PipelineConfig, projection: dict) -> dict:
    fallback = _fallback(projection)
    if cfg.skip_llm:
        annotation, metadata, source = fallback, {"model_key": LLM_MODEL_KEY, "is_reasoning": False, "reasoning_present": False, "error": "skip_llm_testing_only"}, "deterministic_fallback"
    else:
        parsed, metadata = _call(projection)
        if metadata["reasoning_present"]:
            raise RuntimeError("non-reasoning annotation returned reasoning content")
        annotation, source = (parsed, "llm") if _valid_response(parsed, projection) else (fallback, "deterministic_fallback_after_llm_error")
    return {"method": projection["method"], "opening_id": projection["opening_id"], "annotation": annotation, "annotation_source": source, "llm_metadata": metadata, "method_specific_annotation": True, "projection_path": f"02_observation_projection/{projection['method']}/{projection['opening_id']}.json"}


def run(cfg: PipelineConfig) -> dict:
    from concurrent.futures import ThreadPoolExecutor, as_completed

    index = read_json(cfg.stage_dir(2) / "index.json")
    out_index = {}
    pending = []
    for method, openings in index.items():
        for opening_id, rel in openings.items():
            out = cfg.stage_dir(3) / method / f"{opening_id}.json"
            out_index.setdefault(method, {})[opening_id] = str(out.relative_to(cfg.output_root))
            if not (cfg.resume and out.exists()):
                pending.append((method, opening_id, rel, out))
    def work(item):
        method, opening_id, rel, out = item
        result = annotate(cfg, read_json(cfg.output_root / rel))
        write_json(out, result)
        return method, opening_id, result["annotation_source"]
    if cfg.llm_workers <= 1:
        completed = map(work, pending)
        for method, opening_id, source in completed:
            print(f"[stage03] {method}/{opening_id}: {source}", flush=True)
    else:
        with ThreadPoolExecutor(max_workers=cfg.llm_workers) as executor:
            futures = [executor.submit(work, item) for item in pending]
            for future in as_completed(futures):
                method, opening_id, source = future.result()
                print(f"[stage03] {method}/{opening_id}: {source}", flush=True)
    write_json(cfg.stage_dir(3) / "index.json", out_index)
    return out_index
