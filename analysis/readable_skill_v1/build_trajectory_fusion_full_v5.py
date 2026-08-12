"""Build Full-v5 by fusing human phase trajectories with live platform routing.

The public strategic graph remains the successful Full-v3 positive/default graph plus
contrastive lessons. DeepSeek Flash (non-reasoning) compresses aggregate human graph
evidence into one structured target/veto/recheck policy per game phase. Experiment
telemetry is private and only prioritizes execution risks; it cannot invent strategy.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any


BASE_METHOD = "full_contrastive_graph_v3"
OUTPUT_METHOD = "full_trajectory_fusion_graph_v5"
MODEL_KEY = "DeepSeek-V4-flash"
PHASE_ORDER = ("early_game", "early_midgame", "midgame", "late_midgame")
FORBIDDEN_PUBLIC_TERMS = (
    "experiment", "evaluation", "win rate", "loss rate", "failed game", "replay",
    "training sample", "run index", "private evidence", "v3", "v4",
)

SYSTEM = """You distill aggregate human StarCraft II trajectories into compact phase policies
for a live macro decision agent. Human positive/default graph evidence is the strategic authority;
adverse human evidence supplies a veto. Private agent telemetry may only prioritize an execution
risk and must never create a strategy direction. Return exactly one policy for every supplied phase,
in supplied order. Each policy has one observable trigger, one strategic target, one veto, one live
recheck, and one short routing summary. Preserve the opening identity and partial-observation wording.
Do not output a build order, action sequence, fixed facility count, universal timing threshold,
historical/provenance language, experiment result, causal claim, reasoning, or chain of thought.
When a phase contains several human contexts, synthesize a safe default plus an Enemy Intelligence
branch instead of copying only the highest-support unknown-state node. A veto must name an
overcommitment or neglected safety check; it must never categorically forbid army production,
production growth, or economy merely because enemy information is incomplete.
Return strict JSON only."""


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    temp.replace(path)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(text.rstrip() + "\n", encoding="utf-8")
    temp.replace(path)


def json_object(text: str) -> dict[str, Any]:
    try:
        value = json.loads(text)
    except Exception:
        match = re.search(r"\{[\s\S]*\}", text or "")
        value = json.loads(match.group()) if match else {}
    return value if isinstance(value, dict) else {}


def opening_paths(base_root: Path) -> dict[str, Path]:
    return {path.parent.name: path.parent for path in base_root.glob("*/*/*/SKILL.md")}


def direction(signature: dict[str, Any]) -> dict[str, str]:
    return {
        key: str(value)
        for key, value in signature.items()
        if key.endswith("_direction") or key in {"tempo", "confidence"}
    }


def human_phase_evidence(repo_root: Path, opening_id: str) -> tuple[list[dict[str, Any]], dict[str, str]]:
    stage1 = repo_root / "analysis/outputs_readable_skill_v1/01_method_ir"
    stage2 = repo_root / "analysis/outputs_readable_skill_v1/02_observation_projection"
    stage3 = repo_root / "analysis/outputs_readable_skill_v1/03_semantic_annotation"
    public_projection = read_json(stage2 / "ablation_positive_only" / f"{opening_id}.json")
    public_semantic = read_json(stage3 / "ablation_positive_only" / f"{opening_id}.json")
    signed_projection = read_json(stage2 / "full_signed_graph" / f"{opening_id}.json")
    signed_ir = read_json(stage1 / "full_signed_graph" / f"{opening_id}.json")
    public_annotations = {
        str(node.get("node_id")): node
        for node in (public_semantic.get("annotation") or {}).get("nodes", [])
        if isinstance(node, dict)
    }
    transitions = {
        str(item.get("source_edge_id") or ""): item
        for item in signed_ir.get("transitions") or []
        if isinstance(item, dict)
    }
    adverse_by_phase: dict[str, list[dict[str, Any]]] = {}
    for node in signed_projection.get("nodes") or []:
        linked = [transitions[x] for x in node.get("source_edge_ids") or [] if x in transitions]
        total = sum(int(x.get("support") or 0) for x in linked)
        enrichment = (
            sum(float((x.get("value_fields") or {}).get("win_enrichment") or 0) * int(x.get("support") or 0) for x in linked) / total
            if total else 0.0
        )
        if node.get("node_type") != "negative" and enrichment >= -0.005:
            continue
        adverse_by_phase.setdefault(str(node.get("phase") or "unknown"), []).append({
            "support": int(node.get("support") or 0),
            "direction_to_avoid": direction(node.get("policy_signature") or {}),
            "own_posture": ((node.get("own_state") or {}).get("obs_style_summary_seed") or {}).get("own_posture", ""),
            "opponent_cues": ((node.get("opponent_state") or {}).get("obs_style_summary_seed") or {}).get("enemy_intelligence", ""),
        })
    preferred_by_phase: dict[str, list[dict[str, Any]]] = {}
    node_phases: dict[str, str] = {}
    for node in public_projection.get("nodes") or []:
        node_id = str(node.get("node_id"))
        phase = str(node.get("phase") or "unknown")
        node_phases[node_id] = phase
        annotation = public_annotations.get(node_id) or {}
        preferred_by_phase.setdefault(phase, []).append({
            "node_id": node_id,
            "node_type": node.get("node_type"),
            "support": int(node.get("support") or 0),
            "frequency": round(float(node.get("frequency") or 0), 4),
            "own_posture": ((node.get("own_state") or {}).get("obs_style_summary_seed") or {}).get("own_posture", ""),
            "opponent_cues": ((node.get("opponent_state") or {}).get("obs_style_summary_seed") or {}).get("enemy_intelligence", ""),
            "policy_signature": direction(node.get("policy_signature") or {}),
            "annotated_trigger": annotation.get("trigger_summary") or "",
            "annotated_direction": annotation.get("decision_direction") or "",
            "annotated_recheck": annotation.get("exit_or_recheck_condition") or "",
        })
    phases = [phase for phase in PHASE_ORDER if phase in preferred_by_phase]
    evidence = []
    for phase in phases:
        evidence.append({
            "phase": phase,
            "preferred_aggregate_nodes": sorted(preferred_by_phase[phase], key=lambda x: (x["support"], x["frequency"]), reverse=True),
            "adverse_aggregate_nodes": sorted(adverse_by_phase.get(phase, []), key=lambda x: x["support"], reverse=True)[:4],
        })
    return evidence, node_phases


def private_feedback(analysis: dict[str, Any], opening_id: str) -> dict[str, Any]:
    race = opening_id[0]
    matchup = opening_id[:3]
    return {
        "global": analysis.get("global") or {},
        "race": {
            "v3": ((analysis.get("by_race") or {}).get("v3") or {}).get(race) or {},
            "v4": ((analysis.get("by_race") or {}).get("v4") or {}).get(race) or {},
        },
        "matchup": {
            "v3": ((analysis.get("by_matchup") or {}).get("v3") or {}).get(matchup) or {},
            "v4": ((analysis.get("by_matchup") or {}).get("v4") or {}).get(matchup) or {},
        },
        "opening": {
            "v3": ((analysis.get("by_skill") or {}).get("v3") or {}).get(opening_id) or {},
            "v4": ((analysis.get("by_skill") or {}).get("v4") or {}).get(opening_id) or {},
        },
        "use_boundary": "Prioritize execution risks only; never infer the strategic target from agent outcomes.",
    }


def validate_annotation(payload: dict[str, Any], phases: list[str]) -> None:
    policies = payload.get("phase_policies")
    if not isinstance(policies, list) or [x.get("phase") for x in policies if isinstance(x, dict)] != phases:
        raise ValueError(f"phase policy identity/order mismatch; expected {phases}")
    required = {"phase", "title", "applies_when", "target", "veto", "live_check", "routing_summary"}
    for policy in policies:
        if set(policy) != required:
            raise ValueError(f"unexpected policy fields: {sorted(policy)}")
        for field in required - {"phase"}:
            value = str(policy.get(field) or "").strip()
            if not value or len(value.split()) > 75:
                raise ValueError(f"invalid {field} in {policy.get('phase')}")
        blob = json.dumps(policy, ensure_ascii=False).lower()
        if any(term in blob for term in FORBIDDEN_PUBLIC_TERMS):
            raise ValueError(f"private provenance leaked in {policy.get('phase')}")
        veto = str(policy.get("veto") or "").lower()
        unsafe_vetoes = (
            "do not strengthen ground", "do not build army", "do not increase production",
            "unless you have confirmed enemy", "unless you have confirmed opponent",
        )
        if any(term in veto for term in unsafe_vetoes):
            raise ValueError(f"unsafe categorical veto in {policy.get('phase')}")


def call_one(
    *, repo_root: Path, opening_id: str, root_excerpt: str,
    human_evidence: list[dict[str, Any]], feedback: dict[str, Any], attempts: int,
) -> dict[str, Any]:
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    from API_Tools.llm_caller import call_openai_detailed, load_agent_pool

    config_path = repo_root / "API_config/config.json"
    model = (load_agent_pool(config_path=str(config_path), force_reload=True).get("llm_agents_pool") or {}).get(MODEL_KEY)
    if not isinstance(model, dict) or model.get("is_reasoning") is not False:
        raise RuntimeError(f"{MODEL_KEY} must exist with is_reasoning=false")
    phases = [x["phase"] for x in human_evidence]
    contract = {"phase_policies": [
        {"phase": phase, "title": "", "applies_when": "", "target": "", "veto": "", "live_check": "", "routing_summary": ""}
        for phase in phases
    ]}
    user = json.dumps({
        "opening_id": opening_id,
        "opening_skill_excerpt": root_excerpt[:6000],
        "aggregate_human_phase_evidence": human_evidence,
        "private_agent_execution_feedback": feedback,
        "platform_contract": {
            "decision_interval_game_seconds": 60,
            "queue_semantics": "complete replacement queue; prerequisites are never inserted; structures mean one additional structure",
            "runtime_router": "selects current phase and one immediate race-aware bottleneck",
            "race_mechanics": "Protoss powered producers; Terran parents/add-ons; Zerg larvae/inject and worker-army larva competition",
        },
        "task": "Compress each phase's aggregate human preferred direction and adverse contrast into one operational target/veto/recheck policy. Keep strategy from human evidence and use telemetry only to sharpen execution checks.",
        "required_output": contract,
    }, ensure_ascii=False)
    errors = []
    for attempt in range(1, attempts + 1):
        result = call_openai_detailed(
            messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}],
            model_key=MODEL_KEY, config_path=str(config_path), is_reasoning=False,
            temperature=0.1, max_tokens=5000, response_format={"type": "json_object"}, timeout=360,
        )
        try:
            if result.get("is_reasoning") is not False or result.get("reasoning"):
                raise ValueError("non-reasoning contract violated")
            if result.get("error"):
                raise ValueError(str(result["error"]))
            annotation = json_object(str(result.get("content") or ""))
            validate_annotation(annotation, phases)
            return {
                "schema_version": 1, "method": OUTPUT_METHOD, "opening_id": opening_id,
                "annotation_source": "llm", "annotation": annotation,
                "llm_metadata": {
                    "model_key": result.get("model_key") or MODEL_KEY, "model": result.get("model"),
                    "is_reasoning": result.get("is_reasoning"), "reasoning_present": bool(result.get("reasoning")),
                    "usage": result.get("usage") or result.get("token_usage") or {}, "attempt": attempt, "error": "",
                },
                "private_inputs": {
                    "agent_visible": False,
                    "human_evidence_digest": hashlib.sha256(json.dumps(human_evidence, sort_keys=True).encode()).hexdigest(),
                    "experiment_feedback_digest": hashlib.sha256(json.dumps(feedback, sort_keys=True).encode()).hexdigest(),
                    "human_phase_evidence": human_evidence,
                    "experiment_feedback": feedback,
                },
            }
        except Exception as exc:
            errors.append(f"attempt {attempt}: {exc}")
            if attempt < attempts:
                time.sleep(3 * attempt)
    raise RuntimeError(f"{opening_id} v5 annotation failed: {'; '.join(errors)}")


def race_bridge(opening_id: str) -> str:
    line = {
        "P": "For Protoss, spend through completed powered compatible producers before adding capacity; preserve opening tempo and never force a new facility solely from a clock threshold.",
        "T": "For Terran, use completed parents before scaling capacity, and order parent before add-on or dependent work; persistent bank plus low army favors executable unit throughput.",
        "Z": "For Zerg, production capacity is bases plus larva/inject throughput; Overlords and Drones consume the same larva as army, so do not translate facility-count rules from other races.",
    }[opening_id[0]]
    return "\n".join([
        "## V5 Human-Trajectory / Runtime Bridge", "",
        "- The phase policy below supplies the strategic target distilled from aggregate trajectory states; it is not an action sequence.",
        "- The live router supplies exactly one current execution bottleneck. Resolve it without replacing the phase target with a generic macro rule.",
        f"- {line}",
        "- Current Threat Flags and severe live disadvantage may veto optional economy or technology; otherwise preserve the opening's strategic identity.", "",
    ])


def phase_index(policies: list[dict[str, Any]]) -> str:
    lines = ["## V5 Phase Policy Index", "", "Use only the policy for the current routed phase.", ""]
    for policy in policies:
        lines.extend([f"- **{policy['phase']} — {policy['title']}:** {policy['routing_summary']}"])
    lines.append("")
    return "\n".join(lines)


def node_policy(policy: dict[str, Any]) -> str:
    return "\n".join([
        "## V5 Phase-Conditioned Trajectory Policy", "",
        f"**Applies when:** {policy['applies_when']}", "",
        f"**Strategic target:** {policy['target']}", "",
        f"**Veto:** {policy['veto']}", "",
        f"**Live recheck:** {policy['live_check']}", "",
    ])


def compile_one(base_dir: Path, output_root: Path, opening_id: str, result: dict[str, Any], node_phases: dict[str, str]) -> None:
    destination = output_root / base_dir.relative_to(base_dir.parents[2])
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(base_dir, destination)
    policies = result["annotation"]["phase_policies"]
    by_phase = {x["phase"]: x for x in policies}

    index_path = destination / "index.json"
    index = read_json(index_path)
    index["method"] = OUTPUT_METHOD
    for node_id, raw in index.get("nodes", {}).items():
        phase = node_phases.get(node_id, "")
        raw["phase"] = phase
        raw["policy_summary"] = (by_phase.get(phase) or {}).get("routing_summary", "")
    write_json(index_path, index)

    root_path = destination / "SKILL.md"
    root = root_path.read_text(encoding="utf-8")
    root = root.replace("- Method: Contrastive Full V3", "- Method: Trajectory-Fusion Full V5")
    marker = "## Contrastive Lessons"
    if marker not in root:
        raise ValueError(f"missing contrastive marker in {root_path}")
    root = root.replace(marker, race_bridge(opening_id) + "\n" + phase_index(policies) + "\n" + marker, 1)
    decision_marker = "## Decision Nodes"
    if decision_marker in root:
        root = root.split(decision_marker, 1)[0].rstrip() + "\n\n## Runtime-Routed Decision Nodes\n\nThe live platform exposes the unread node whose mined phase and trigger best match the current observation.\n"
    write_text(root_path, root)

    for node_path in sorted((destination / "nodes").glob("*.md")):
        phase = node_phases.get(node_path.stem, "")
        policy = by_phase.get(phase)
        if not policy:
            continue
        text = node_path.read_text(encoding="utf-8")
        marker = "## What This Does NOT Mean"
        if marker not in text:
            raise ValueError(f"missing node marker in {node_path}")
        write_text(node_path, text.replace(marker, node_policy(policy) + "\n" + marker, 1))

    provenance = destination / "provenance"
    provenance.mkdir(exist_ok=True)
    write_json(provenance / "trajectory_fusion_synthesis.json", result)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--analysis", type=Path, default=None)
    parser.add_argument("--workers", type=int, default=8)
    parser.add_argument("--attempts", type=int, default=3)
    parser.add_argument("--openings", default="")
    parser.add_argument("--no-resume", action="store_true")
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()
    base_root = repo_root / "SKILL_MINING_V2_READABLE" / BASE_METHOD
    output_root = repo_root / "SKILL_MINING_V2_READABLE" / OUTPUT_METHOD
    result_root = repo_root / "analysis/outputs_readable_skill_v1/10_full_trajectory_fusion_v5"
    analysis_path = args.analysis or (repo_root / "SC2-Agent-human-skill/game_records/_human_skill_ablation/full_v5_global_analysis.json")
    analysis = read_json(analysis_path)
    base_dirs = opening_paths(base_root)
    ids = sorted(base_dirs)
    if args.openings:
        requested = {x.strip() for x in args.openings.split(",") if x.strip()}
        ids = [x for x in ids if x in requested]
        if set(ids) != requested:
            raise ValueError(f"unknown openings: {sorted(requested - set(ids))}")

    evidence_cache: dict[str, list[dict[str, Any]]] = {}
    node_phase_cache: dict[str, dict[str, str]] = {}
    feedback_cache: dict[str, dict[str, Any]] = {}

    def work(opening_id: str):
        evidence, node_phases = human_phase_evidence(repo_root, opening_id)
        feedback = private_feedback(analysis, opening_id)
        evidence_cache[opening_id] = evidence
        node_phase_cache[opening_id] = node_phases
        feedback_cache[opening_id] = feedback
        out = result_root / f"{opening_id}.json"
        if out.exists() and not args.no_resume:
            cached = read_json(out)
            validate_annotation(cached.get("annotation") or {}, [x["phase"] for x in evidence])
            return opening_id, cached
        result = call_one(
            repo_root=repo_root, opening_id=opening_id,
            root_excerpt=(base_dirs[opening_id] / "SKILL.md").read_text(encoding="utf-8"),
            human_evidence=evidence, feedback=feedback, attempts=args.attempts,
        )
        write_json(out, result)
        return opening_id, result

    completed = {}
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(work, opening_id): opening_id for opening_id in ids}
        for future in as_completed(futures):
            opening_id, result = future.result()
            completed[opening_id] = result
            print(f"[trajectory-fusion-v5] {opening_id}: {result['annotation_source']}", flush=True)
    for opening_id in ids:
        compile_one(base_dirs[opening_id], output_root, opening_id, completed[opening_id], node_phase_cache[opening_id])
    summary = {
        "schema_version": 1, "method": OUTPUT_METHOD, "base_method": BASE_METHOD,
        "model_key": MODEL_KEY, "skills": len(ids),
        "phase_policies": sum(len(x["annotation"]["phase_policies"]) for x in completed.values()),
        "annotation_sources": sorted({x["annotation_source"] for x in completed.values()}),
        "reasoning_present": sum(bool(x["llm_metadata"]["reasoning_present"]) for x in completed.values()),
        "api_errors": sum(bool(x["llm_metadata"]["error"]) for x in completed.values()),
        "agent_visible_private_feedback": 0,
    }
    write_json(result_root / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
