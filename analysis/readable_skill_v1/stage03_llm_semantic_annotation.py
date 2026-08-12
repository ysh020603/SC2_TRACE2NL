from __future__ import annotations

import json
import re
from copy import deepcopy

from .common.io import read_json, write_json
from .common.knowledge_grounding import KnowledgeStore
from .common.method_policy import policy
from .config import LLM_MODEL_KEY, PipelineConfig

SYSTEM = """You are compiling reusable strategic knowledge for an SC2 macro decision-making agent.
This is NOT a build-order generation task. Human trajectory evidence supplies the immutable statistical sign and broad response direction. The SC2 knowledge capsule may only interpret, constrain, or qualify that trajectory evidence; it must never create a preferred/harmful label.
Do not output an ordered action list, replay actions, canonical action sequences, exact unseen counts, oracle state IDs, cluster IDs, or causal claims. Never mention a concrete SC2 entity unless it is in allowed_entity_mentions. Every counter/synergy statement must be represented by an exact supported relation_id in knowledge_claims. Opponent descriptions must use partial-observation wording compatible with Enemy Intelligence. Explicitly separate applicability checks from repair/recheck conditions. For negative nodes, name the general process failure rather than a race-specific symptom. Historical association is not causality. Return strict JSON only."""


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


def _fallback(projection: dict, capsules: dict | None = None) -> dict:
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
    capsules = capsules or {}
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
        capsule = capsules.get(node["node_id"]) or {}
        trajectory_entities = capsule.get("trajectory_entities") or []
        trajectory_text = (
            "The human response evidence contains broad investment involving " + ", ".join(trajectory_entities[:5]) + "; retain its statistical sign without copying an action sequence."
            if trajectory_entities else
            "The human response evidence supports only the supplied broad investment direction; no exact entity choice is asserted."
        )
        annotations.append({
            "node_id": node["node_id"], "node_type": node_type, "title": title,
            "trigger_summary": trigger, "own_situation": own, "opponent_situation": opp,
            "decision_direction": direction, "strategic_reason": "This direction matches the retained evidence boundary for the current method and should be reassessed against the live observation.",
            "avoid_direction": risk, "transition_goal": "Reach a stable posture where the next economy, production, technology, and army trade-off can be re-evaluated from current information.",
            "exit_or_recheck_condition": "Recheck when Enemy Intelligence, army posture, resources, supply, Completed, Under Construction, or Active Queues materially change.",
            "next_state_summary": "A later observable posture may warrant a separate node." if policy(method)["graph"] else "",
            "trajectory_interpretation": trajectory_text,
            "applicability_checks": [
                "The live phase and own macro posture still resemble the node trigger.",
                "Current resources, supply, producers, prerequisites, and active queues can support the direction.",
                "Enemy Intelligence has not materially contradicted the remembered opponent posture.",
            ],
            "knowledge_claims": [],
            "failure_mode": "stale_or_infeasible_historical_response" if node_type == "negative" else "none_observed",
            "repair_or_recheck_condition": "Stop or revise the direction when its prerequisites are unavailable, the queue cannot execute, or fresh Enemy Intelligence changes the threat class.",
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
    if re.search(r"(?:own|opp)_s\d+|(?:own|opp)_state_id|source_edge_id|response_id", blob, re.I):
        return False
    forbidden = {
        "ablation_single_trace": ("population", "positive", "negative", "preferred", "harmful"),
        "ablation_static_population": ("positive", "negative", "preferred", "harmful"),
        "ablation_flat_adaptive": ("possible next", "next node", "graph successor", "multi-hop"),
        "ablation_positive_only": ("negative", "harmful", "worse outcome"),
        "ablation_frequency_only": ("positive", "preferred", "better outcome", "adjusted lift", "win enrichment"),
    }.get(projection["method"], ())
    return not any(term in blob for term in forbidden)


def _contract(projection: dict) -> dict:
    return {
        "opening": {"opening_name": "", "opening_family": "", "opening_summary": "", "strategic_goal": "", "economy_character": "", "production_character": "", "technology_character": "", "army_character": "", "flexibility_note": ""},
        "nodes": [{"node_id": n["node_id"], "node_type": n["node_type"], "title": "", "trigger_summary": "", "own_situation": "", "opponent_situation": "", "decision_direction": "", "strategic_reason": "", "avoid_direction": "", "transition_goal": "", "exit_or_recheck_condition": "", "next_state_summary": "", "trajectory_interpretation": "", "applicability_checks": [], "knowledge_claims": [{"relation_id": "", "subject": "", "relation": "", "object": ""}], "failure_mode": "", "repair_or_recheck_condition": ""} for n in projection.get("nodes", [])],
    }


def _method_specific_rule(method: str) -> str:
    return {
        "ablation_single_trace": "Never mention population, positive, negative, preferred, harmful, or adaptive comparison.",
        "ablation_static_population": "Use only own phase/posture triggers; never claim opponent-conditioned evidence or value signs.",
        "ablation_flat_adaptive": "Never mention graph paths, successors, next nodes, or multi-hop guidance.",
        "ablation_positive_only": "Never mention removed negative, harmful, or worse-outcome evidence.",
        "ablation_frequency_only": "Never call frequent evidence positive, preferred, best, better, or outcome-improving.",
    }.get(method, "Preserve positive, negative, and default signs exactly.")


def _public_node_projection(node: dict) -> dict:
    public = deepcopy(node)
    for key in ("next_state_id", "source_state_id", "source_state_ids", "source_edge_ids"):
        public.pop(key, None)
    for state_key in ("own_state", "opponent_state"):
        state = public.get(state_key)
        if isinstance(state, dict):
            for key in ("state_id", "source_state_ids"):
                state.pop(key, None)
    return public


def _merge_opening_defaults(annotation: dict, fallback: dict) -> dict:
    merged = deepcopy(annotation)
    supplied = merged.get("opening") if isinstance(merged.get("opening"), dict) else {}
    defaults = fallback.get("opening") if isinstance(fallback.get("opening"), dict) else {}
    merged["opening"] = {
        key: supplied.get(key) if supplied.get(key) not in (None, "") else value
        for key, value in defaults.items()
    }
    for key, value in supplied.items():
        if key not in merged["opening"]:
            merged["opening"][key] = value
    return merged


def _call_payload(user_payload: dict) -> tuple[dict, dict]:
    from API_Tools.llm_caller import call_openai_detailed, load_agent_pool

    pool = (load_agent_pool().get("llm_agents_pool") or {}).get(LLM_MODEL_KEY) or {}
    if pool.get("is_reasoning") is not False:
        raise RuntimeError("API_config/config.json must mark DeepSeek-V4-flash as is_reasoning=false")
    user = json.dumps(user_payload, ensure_ascii=False)
    result = call_openai_detailed(messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}], model_key=LLM_MODEL_KEY, is_reasoning=False, temperature=0.15, max_tokens=9000, response_format={"type": "json_object"}, timeout=180)
    parsed = _json_object(result.get("content") or "")
    metadata = {"model_key": result.get("model_key"), "model": result.get("model"), "is_reasoning": result.get("is_reasoning"), "reasoning_present": bool(result.get("reasoning")), "reasoning_source": result.get("reasoning_source"), "error": result.get("error") or ""}
    return parsed, metadata


def _call(projection: dict, capsules: dict, failure_context: dict | None = None) -> tuple[dict, dict]:
    from concurrent.futures import ThreadPoolExecutor

    method = projection["method"]
    opening_contract = _contract({"nodes": []})["opening"]
    opening, opening_meta = _call_payload({
        "task": "opening_level_human_trajectory_summary", "method": method,
        "information_boundary": policy(method), "method_specific_rule": _method_specific_rule(method),
        "opening_projection": projection.get("opening_projection"), "required_output": {"opening": opening_contract},
    })
    opening = opening.get("opening") if isinstance(opening.get("opening"), dict) else opening

    def annotate_node(node: dict) -> tuple[dict, dict]:
        node_id = str(node.get("node_id"))
        required = _contract({"nodes": [node]})["nodes"][0]
        parsed, metadata = _call_payload({
            "task": "single_node_knowledge_grounded_human_trajectory_annotation",
            "method": method, "information_boundary": policy(method),
            "method_specific_rule": _method_specific_rule(method),
            "opening_context": {
                "opening_id": projection.get("opening_id"), "race": projection.get("race"),
                "opponent_race": projection.get("opponent_race"), "opening_projection": projection.get("opening_projection"),
            },
            "node_projection": _public_node_projection(node),
            "knowledge_capsule_for_this_node_only": capsules.get(node_id) or {},
            "cross_match_failure_context": failure_context or {},
            "strict_entity_rule": "Do not transfer entities from any other node. Concrete entities must be in this node's allowed_entity_mentions.",
            "required_output": {"node": required},
        })
        candidate = parsed.get("node") if isinstance(parsed.get("node"), dict) else parsed
        return candidate, metadata

    nodes = list(projection.get("nodes") or [])
    with ThreadPoolExecutor(max_workers=min(6, max(1, len(nodes)))) as executor:
        results = list(executor.map(annotate_node, nodes))
    parsed_nodes = [item[0] for item in results]
    node_meta = [item[1] for item in results]
    metadata = {
        "model_key": opening_meta.get("model_key"), "model": opening_meta.get("model"), "is_reasoning": False,
        "reasoning_present": bool(opening_meta.get("reasoning_present")) or any(x.get("reasoning_present") for x in node_meta),
        "reasoning_source": "node_or_opening" if bool(opening_meta.get("reasoning_present")) or any(x.get("reasoning_present") for x in node_meta) else None,
        "error": "; ".join(x for x in [opening_meta.get("error")] + [m.get("error") for m in node_meta] if x),
        "call_count": 1 + len(node_meta),
    }
    return {"opening": opening, "nodes": parsed_nodes}, metadata


def _repair(projection: dict, capsules: dict, candidate: dict, errors: list[str]) -> tuple[dict, dict]:
    from concurrent.futures import ThreadPoolExecutor

    method = projection["method"]
    candidate_by_id = {str(n.get("node_id")): n for n in candidate.get("nodes") or [] if isinstance(n, dict)}
    bad_ids = {error.split(":", 1)[0] for error in errors if re.match(r"^N\d+:", error)}
    if not bad_ids:
        bad_ids = {str(n.get("node_id")) for n in projection.get("nodes") or []}

    def repair_node(node: dict) -> tuple[dict, dict]:
        node_id = str(node.get("node_id"))
        if node_id not in bad_ids:
            return candidate_by_id.get(node_id) or {}, {"reasoning_present": False, "error": ""}
        node_errors = [error for error in errors if error.startswith(node_id + ":")]
        required = _contract({"nodes": [node]})["nodes"][0]
        parsed, metadata = _call_payload({
            "task": "repair_single_invalid_knowledge_grounded_node",
            "method": method, "method_specific_rule": _method_specific_rule(method),
            "validation_errors_for_this_node": node_errors,
            "candidate_node": candidate_by_id.get(node_id) or {}, "node_projection": _public_node_projection(node),
            "knowledge_capsule_for_this_node_only": capsules.get(node_id) or {},
            "repair_rules": [
                "Delete every concrete entity named in an ungrounded_entity_mention error.",
                "Do not add replacement entities unless they occur in allowed_entity_mentions for this node.",
                "Use only exact supported relation triples and preserve node_id and node_type.",
            ],
            "required_output": {"node": required},
        })
        repaired = parsed.get("node") if isinstance(parsed.get("node"), dict) else parsed
        return repaired, metadata

    nodes = list(projection.get("nodes") or [])
    with ThreadPoolExecutor(max_workers=min(6, max(1, len(bad_ids)))) as executor:
        results = list(executor.map(repair_node, nodes))
    metadata_items = [item[1] for item in results]
    metadata = {
        "model_key": LLM_MODEL_KEY, "is_reasoning": False,
        "reasoning_present": any(x.get("reasoning_present") for x in metadata_items),
        "error": "; ".join(str(x.get("error")) for x in metadata_items if x.get("error")),
        "call_count": len(bad_ids),
    }
    return {"opening": candidate.get("opening") or {}, "nodes": [item[0] for item in results]}, metadata


def _load_failure_context(path) -> dict:
    if not path:
        return {}
    payload = read_json(path)
    aggregate = {}
    for version, report in payload.items():
        for signal, outcomes in (report.get("prevalence_by_outcome") or {}).items():
            defeat = (outcomes.get("Defeat") or {}).get("rate", 0)
            victory = (outcomes.get("Victory") or {}).get("rate", 0)
            item = aggregate.setdefault(signal, {"defeat_rates": [], "victory_rates": [], "versions": []})
            item["defeat_rates"].append(float(defeat or 0))
            item["victory_rates"].append(float(victory or 0))
            item["versions"].append(version)
    priorities = []
    for signal, item in aggregate.items():
        defeat_rate = sum(item["defeat_rates"]) / len(item["defeat_rates"])
        victory_rate = sum(item["victory_rates"]) / len(item["victory_rates"])
        priorities.append({
            "signal": signal, "mean_defeat_rate": round(defeat_rate, 4),
            "mean_victory_rate": round(victory_rate, 4), "defeat_enrichment": round(defeat_rate - victory_rate, 4),
        })
    priorities.sort(key=lambda x: (x["defeat_enrichment"], x["mean_defeat_rate"]), reverse=True)
    return {
        "cross_match_process_priorities": priorities[:5],
        "usage_rule": "Use only cross-match process failures. Do not add matchup- or race-specific patches.",
        "source": str(path),
    }


def _attach_execution_envelopes(annotation: dict, capsules: dict, failure_context: dict) -> dict:
    priorities = [x.get("signal") for x in failure_context.get("cross_match_process_priorities") or []]
    for node in annotation.get("nodes") or []:
        capsule = capsules.get(str(node.get("node_id"))) or {}
        candidates = []
        for name in capsule.get("trajectory_entities") or []:
            entity = (capsule.get("entities") or {}).get(name) or {}
            if entity.get("entity_type") != "Unit" or entity.get("is_structure"):
                continue
            candidates.append({
                "name": name, "cost": entity.get("cost"), "weapon_targets": entity.get("weapon_targets") or [],
                "tech_chain": entity.get("tech_chain") or [],
            })
        node["execution_envelope"] = {
            "trajectory_candidate_pool": candidates[:8],
            "selection_rule": "Choose only a currently reachable candidate after checking live producers, prerequisites, resources, supply, and active queues; this is a candidate pool, not an ordered build list.",
            "resource_conversion_trigger": "When the combined bank is at least 750 and army supply is still below 15 after 05:00, prefer a currently executable combat candidate from this pool before optional greed or deeper technology.",
            "fallback_rule": "If the preferred candidate is not reachable before the next decision, use a cheaper currently producible trajectory candidate; do not queue a long blocked prerequisite chain while army supply is low.",
            "feedback_rule": "If the bank/low-army deficit persists for two decisions, stop repeating the same plan, re-read the best matching node, and choose a different reachable candidate or producer bottleneck repair.",
            "diagnostic_priorities": priorities[:3],
        }
    return annotation


def _deterministic_knowledge_sanitize(annotation: dict, errors: list[str]) -> dict:
    """Remove precisely identified unsupported facts without asking the model to self-police."""
    cleaned = deepcopy(annotation)
    nodes = {str(n.get("node_id")): n for n in cleaned.get("nodes") or [] if isinstance(n, dict)}
    unsupported_entities: dict[str, set[str]] = {}
    unsupported_relations: dict[str, set[str]] = {}
    for error in errors:
        match = re.match(r"^(N\d+):ungrounded_entity_mention:(.+)$", error)
        if match:
            unsupported_entities.setdefault(match.group(1), set()).add(match.group(2))
        match = re.match(r"^(N\d+):unsupported_knowledge_claim:(.+)$", error)
        if match:
            unsupported_relations.setdefault(match.group(1), set()).add(match.group(2))

    def sanitize_value(value, names: set[str]):
        if isinstance(value, dict):
            return {key: sanitize_value(item, names) for key, item in value.items()}
        if isinstance(value, list):
            return [sanitize_value(item, names) for item in value]
        if not isinstance(value, str):
            return value
        for name in sorted(names, key=len, reverse=True):
            value = re.sub(
                rf"(?<![A-Za-z0-9]){re.escape(name)}s?(?![A-Za-z0-9])",
                "a currently reachable knowledge-verified option",
                value,
                flags=re.I,
            )
        return value

    for node_id, names in unsupported_entities.items():
        if node_id in nodes:
            nodes[node_id] = sanitize_value(nodes[node_id], names)
    for node_id, relation_ids in unsupported_relations.items():
        if node_id in nodes:
            nodes[node_id]["knowledge_claims"] = [
                claim for claim in nodes[node_id].get("knowledge_claims") or []
                if str(claim.get("relation_id")) not in relation_ids
            ]
    cleaned["nodes"] = [nodes.get(str(n.get("node_id")), n) for n in cleaned.get("nodes") or []]
    return cleaned


def annotate(cfg: PipelineConfig, projection: dict, knowledge: KnowledgeStore | None = None, failure_context: dict | None = None) -> dict:
    knowledge = knowledge or KnowledgeStore.load(cfg.knowledge_root)
    failure_context = failure_context or {}
    capsules = knowledge.capsules_for_projection(projection)
    fallback = _fallback(projection, capsules)
    validation_errors = []
    repair_metadata = None
    if cfg.skip_llm:
        annotation, metadata, source = fallback, {"model_key": LLM_MODEL_KEY, "is_reasoning": False, "reasoning_present": False, "error": "skip_llm_testing_only"}, "deterministic_fallback"
    else:
        parsed, metadata = _call(projection, capsules, failure_context)
        parsed = _merge_opening_defaults(parsed, fallback)
        if metadata["reasoning_present"]:
            raise RuntimeError("non-reasoning annotation returned reasoning content")
        validation_errors = ([] if _valid_response(parsed, projection) else ["structural_or_ablation_boundary_invalid"])
        if not validation_errors:
            validation_errors = knowledge.validate_annotation(parsed, projection, capsules)
        if validation_errors:
            sanitized = _deterministic_knowledge_sanitize(parsed, validation_errors)
            sanitized_errors = ([] if _valid_response(sanitized, projection) else ["sanitized_structural_or_boundary_invalid"])
            if not sanitized_errors:
                sanitized_errors = knowledge.validate_annotation(sanitized, projection, capsules)
            if not sanitized_errors:
                annotation, source = sanitized, "llm_deterministically_sanitized_and_knowledge_validated"
                repair_metadata = {"model_key": LLM_MODEL_KEY, "is_reasoning": False, "reasoning_present": False, "error": "not_needed_after_deterministic_sanitize", "call_count": 0}
                sanitized_errors = None
            else:
                repaired, repair_metadata = _repair(projection, capsules, sanitized, sanitized_errors)
            if sanitized_errors is None:
                pass
            elif repair_metadata["reasoning_present"]:
                raise RuntimeError("non-reasoning repair returned reasoning content")
            else:
                repair_errors = ([] if _valid_response(repaired, projection) else ["repair_structural_or_boundary_invalid"])
                if not repair_errors:
                    repair_errors = knowledge.validate_annotation(repaired, projection, capsules)
                if repair_errors:
                    validation_errors = validation_errors + [f"repair:{x}" for x in repair_errors]
                    annotation, source = fallback, "deterministic_grounded_fallback_after_failed_repair"
                else:
                    annotation, source = repaired, "llm_repaired_and_knowledge_validated"
        else:
            annotation, source = parsed, "llm_knowledge_validated"
    annotation = _attach_execution_envelopes(annotation, capsules, failure_context)
    return {
        "method": projection["method"], "opening_id": projection["opening_id"], "annotation": annotation,
        "annotation_source": source, "llm_metadata": metadata, "repair_llm_metadata": repair_metadata,
        "knowledge_validation": {"valid": not knowledge.validate_annotation(annotation, projection, capsules), "initial_errors": validation_errors},
        "knowledge_capsules": capsules, "cross_match_failure_context": failure_context, "method_specific_annotation": True,
        "projection_path": f"02_observation_projection/{projection['method']}/{projection['opening_id']}.json",
    }


def run(cfg: PipelineConfig) -> dict:
    from concurrent.futures import ThreadPoolExecutor, as_completed

    index = read_json(cfg.stage_dir(2) / "index.json")
    knowledge = KnowledgeStore.load(cfg.knowledge_root)
    failure_context = _load_failure_context(cfg.failure_diagnostics)
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
        result = annotate(cfg, read_json(cfg.output_root / rel), knowledge, failure_context)
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
