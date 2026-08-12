"""Build Full-v3 as positive/default guidance plus contrastive lessons.

The public graph is copied from Positive Only.  Private signed-graph evidence
is matched to the closest public situation and sent to DeepSeek Flash in one
non-reasoning annotation call per opening.  Only a concise mistake-to-
correction lesson is published; source nodes, labels, outcomes, and provenance
remain outside the agent-visible skill files.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any


BASE_METHOD = "ablation_positive_only"
EVIDENCE_METHOD = "full_signed_graph"
OUTPUT_METHOD = "full_contrastive_graph_v3"
MODEL_KEY = "DeepSeek-V4-flash"
MAX_LESSONS = 3
FORBIDDEN_PUBLIC_TERMS = (
    "negative node",
    "failure node",
    "failed replay",
    "losing replay",
    "loss label",
    "historical trajectory",
    "source opening",
    "source node",
    "private evidence",
    "training sample",
)
CONTEXT_FIELDS = (
    "army_domain",
    "army_style",
    "air_presence",
    "defense_posture",
    "economy_posture",
    "expansion_posture",
    "pressure_posture",
    "production_posture",
    "technology_posture",
)

SYSTEM = """You compile compact contrastive strategic lessons for a StarCraft II macro agent.
Each private candidate contains one broad direction that should not be copied and one public
positive/default situation that supplies the correction. Convert every candidate into a clear
mistake-to-correction lesson grounded only in live observable conditions. Preserve the supplied
target_node_id and correction direction. Do not expose source nodes, labels, outcomes, replay or
sample provenance, statistical terminology, or hidden counts. Do not output a build order, fixed
action sequence, causal claim, or chain of thought. The current live observation always has
priority. Return strict JSON only."""


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
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


def opening_ids(stage3: Path) -> list[str]:
    return sorted(path.stem for path in (stage3 / BASE_METHOD).glob("*.json"))


def state_similarity(left: dict[str, Any], right: dict[str, Any]) -> float:
    score = 0.0
    if left.get("phase") == right.get("phase"):
        score += 5.0
    for side in ("own_state", "opponent_state"):
        a = left.get(side) or {}
        b = right.get(side) or {}
        for field in CONTEXT_FIELDS:
            if a.get(field) and a.get(field) == b.get(field):
                score += 1.0
        a_threats = set(a.get("special_threats") or [])
        b_threats = set(b.get("special_threats") or [])
        score += 0.5 * len(a_threats & b_threats)
    return score


def direction_text(signature: dict[str, Any]) -> str:
    rendered = []
    for field in (
        "army_direction",
        "production_direction",
        "economy_direction",
        "expansion_direction",
        "technology_direction",
        "defense_direction",
        "air_direction",
        "upgrade_direction",
    ):
        value = str(signature.get(field) or "").strip()
        if value and value != "maintain":
            rendered.append(f"{field.replace('_direction', '').replace('_', ' ')}: {value.replace('_', ' ')}")
    return "; ".join(rendered) or "continue the current macro direction without a fresh safety check"


def collect_private_nodes(
    stage1: Path,
    stage2: Path,
    stage3: Path,
    ids: list[str],
) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for opening_id in ids:
        method_ir = read_json(stage1 / EVIDENCE_METHOD / f"{opening_id}.json")
        projection = read_json(stage2 / EVIDENCE_METHOD / f"{opening_id}.json")
        semantic = read_json(stage3 / EVIDENCE_METHOD / f"{opening_id}.json")
        transitions = {
            str(item.get("source_edge_id") or ""): item
            for item in method_ir.get("transitions", [])
            if isinstance(item, dict)
        }
        annotations = {
            str(node.get("node_id")): node
            for node in semantic.get("annotation", {}).get("nodes", [])
            if isinstance(node, dict)
        }
        for node in projection.get("nodes", []):
            source_transitions = [
                transitions[edge_id]
                for edge_id in node.get("source_edge_ids") or []
                if edge_id in transitions
            ]
            total_support = sum(int(item.get("support") or 0) for item in source_transitions)
            weighted_enrichment = (
                sum(
                    float((item.get("value_fields") or {}).get("win_enrichment") or 0.0)
                    * int(item.get("support") or 0)
                    for item in source_transitions
                )
                / total_support
                if total_support
                else 0.0
            )
            is_signed_harmful = node.get("node_type") == "negative"
            # Some matchups have no node that clears the strict signed-label
            # threshold.  A below-baseline public context from the same
            # matchup still supplies adverse examples without importing units
            # or threats from another enemy race.
            if not is_signed_harmful and weighted_enrichment >= -0.005:
                continue
            annotation = annotations.get(str(node.get("node_id"))) or {}
            records.append(
                {
                    "source_opening": opening_id,
                    "source_node": str(node.get("node_id") or ""),
                    "projection": node,
                    "unsafe_direction": direction_text(node.get("policy_signature") or {}),
                    "risk_hint": str(annotation.get("avoid_direction") or ""),
                    "support": int(node.get("support") or 0),
                    "evidence_kind": (
                        "signed_harmful" if is_signed_harmful else "same_matchup_below_baseline"
                    ),
                    "weighted_win_enrichment": weighted_enrichment,
                }
            )
    if not records:
        raise RuntimeError("signed graph contains no private contrastive evidence")
    return records


def select_pairs(
    opening_id: str,
    public_projection: dict[str, Any],
    public_semantic: dict[str, Any],
    private_nodes: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[str]]:
    public_annotations = {
        str(node.get("node_id")): node
        for node in public_semantic.get("annotation", {}).get("nodes", [])
        if isinstance(node, dict)
    }
    public_nodes = list(public_projection.get("nodes") or [])
    if not public_nodes:
        raise ValueError(f"{opening_id} has no public nodes")

    ranked: list[tuple[float, int, dict[str, Any], dict[str, Any]]] = []
    for private in private_nodes:
        source_opening = private["source_opening"]
        if source_opening[:3] != opening_id[:3]:
            continue
        scope = 2 if source_opening == opening_id else 1
        target = max(
            public_nodes,
            key=lambda node: (
                state_similarity(private["projection"], node),
                int(node.get("support") or 0),
                str(node.get("node_id") or ""),
            ),
        )
        context_score = state_similarity(private["projection"], target)
        ranked.append((scope * 100.0 + context_score, private["support"], private, target))
    if not ranked:
        raise RuntimeError(f"{opening_id} has no same-matchup adverse evidence")
    ranked.sort(key=lambda item: (item[0], item[1]), reverse=True)

    selected: list[tuple[dict[str, Any], dict[str, Any]]] = []
    seen_sources: set[str] = set()
    seen_targets: set[str] = set()
    for prefer_new_target in (True, False):
        for _score, _support, private, target in ranked:
            source_key = f"{private['source_opening']}:{private['source_node']}"
            target_id = str(target.get("node_id") or "")
            if source_key in seen_sources or (prefer_new_target and target_id in seen_targets):
                continue
            selected.append((private, target))
            seen_sources.add(source_key)
            seen_targets.add(target_id)
            if len(selected) >= MAX_LESSONS:
                break
        if len(selected) >= MAX_LESSONS:
            break

    candidates: list[dict[str, Any]] = []
    provenance: list[str] = []
    for index, (private, target) in enumerate(selected, 1):
        target_id = str(target["node_id"])
        target_annotation = public_annotations[target_id]
        source = private["projection"]
        candidates.append(
            {
                "lesson_id": f"L{index:02d}",
                "target_node_id": target_id,
                "live_context": {
                    "phase": target.get("phase"),
                    "own": ((target.get("own_state") or {}).get("obs_style_summary_seed") or {}).get("own_posture", ""),
                    "opponent": ((target.get("opponent_state") or {}).get("obs_style_summary_seed") or {}).get("enemy_intelligence", ""),
                    "public_trigger": target_annotation.get("trigger_summary") or "",
                },
                "direction_to_avoid": private["unsafe_direction"],
                "risk_hint": private["risk_hint"],
                "correct_public_direction": target_annotation.get("decision_direction") or "",
                "correct_reason": target_annotation.get("strategic_reason") or "",
                "existing_recheck": target_annotation.get("exit_or_recheck_condition") or "",
                "private_context": {
                    "phase": source.get("phase"),
                    "own": ((source.get("own_state") or {}).get("obs_style_summary_seed") or {}).get("own_posture", ""),
                    "opponent": ((source.get("opponent_state") or {}).get("obs_style_summary_seed") or {}).get("enemy_intelligence", ""),
                },
            }
        )
        provenance.append(f"{private['source_opening']}:{private['source_node']}->{opening_id}:{target_id}")
    return candidates, provenance


def validate_annotation(payload: dict[str, Any], candidates: list[dict[str, Any]]) -> None:
    lessons = payload.get("lessons")
    if not isinstance(lessons, list):
        raise ValueError("contrastive response lessons must be a list")
    expected = [(item["lesson_id"], item["target_node_id"]) for item in candidates]
    actual = [
        (str(item.get("lesson_id") or ""), str(item.get("target_node_id") or ""))
        for item in lessons
        if isinstance(item, dict)
    ]
    if actual != expected:
        raise ValueError(f"lesson identity/order mismatch: expected={expected}, actual={actual}")
    required = {"lesson_id", "target_node_id", "title", "when", "mistake", "correction", "why", "recheck"}
    for lesson in lessons:
        if set(lesson) != required:
            raise ValueError(f"unexpected lesson fields: {sorted(lesson)}")
        for field in required - {"lesson_id", "target_node_id"}:
            value = str(lesson.get(field) or "").strip()
            if not value or len(value.split()) > 85:
                raise ValueError(f"invalid {field} for {lesson.get('lesson_id')}")
        blob = json.dumps(lesson, ensure_ascii=False).lower()
        if any(term in blob for term in FORBIDDEN_PUBLIC_TERMS):
            raise ValueError(f"private evidence leaked into {lesson.get('lesson_id')}")


def call_one(
    *,
    repo_root: Path,
    opening_id: str,
    candidates: list[dict[str, Any]],
    provenance: list[str],
    attempts: int,
) -> dict[str, Any]:
    from API_Tools.llm_caller import call_openai_detailed, load_agent_pool

    api_config = repo_root / "API_config" / "config.json"
    model_cfg = (
        load_agent_pool(config_path=str(api_config), force_reload=True).get("llm_agents_pool") or {}
    ).get(MODEL_KEY)
    if not isinstance(model_cfg, dict) or model_cfg.get("is_reasoning") is not False:
        raise RuntimeError(f"{MODEL_KEY} must exist and set is_reasoning=false")
    contract = {
        "lessons": [
            {
                "lesson_id": item["lesson_id"],
                "target_node_id": item["target_node_id"],
                "title": "",
                "when": "",
                "mistake": "",
                "correction": "",
                "why": "",
                "recheck": "",
            }
            for item in candidates
        ]
    }
    user = json.dumps(
        {
            "opening_id": opening_id,
            "task": (
                "For every candidate, state the tempting strategic mistake and contrast it with the supplied "
                "public correction. Make the pair operational under live observation, concise enough for an "
                "agent prompt, and preserve the target node and correction direction."
            ),
            "candidates": candidates,
            "required_output": contract,
        },
        ensure_ascii=False,
    )
    errors: list[str] = []
    for attempt in range(1, attempts + 1):
        result = call_openai_detailed(
            messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}],
            model_key=MODEL_KEY,
            config_path=str(api_config),
            is_reasoning=False,
            temperature=0.1,
            max_tokens=5500,
            response_format={"type": "json_object"},
            timeout=360,
        )
        try:
            if result.get("is_reasoning") is not False or result.get("reasoning"):
                raise ValueError("non-reasoning contract violated")
            if result.get("error"):
                raise ValueError(str(result["error"]))
            parsed = json_object(str(result.get("content") or ""))
            validate_annotation(parsed, candidates)
            return {
                "schema_version": 1,
                "method": OUTPUT_METHOD,
                "opening_id": opening_id,
                "annotation_source": "llm",
                "annotation": parsed,
                "llm_metadata": {
                    "model_key": result.get("model_key") or MODEL_KEY,
                    "model": result.get("model"),
                    "is_reasoning": result.get("is_reasoning"),
                    "reasoning_present": bool(result.get("reasoning")),
                    "reasoning_source": result.get("reasoning_source"),
                    "usage": result.get("usage") or result.get("token_usage") or {},
                    "error": "",
                    "attempt": attempt,
                },
                "private_pairing_provenance": {
                    "source_method": EVIDENCE_METHOD,
                    "pair_ids": provenance,
                    "source_digest": hashlib.sha256(
                        json.dumps(candidates, ensure_ascii=False, sort_keys=True).encode("utf-8")
                    ).hexdigest(),
                    "agent_visible": False,
                },
            }
        except Exception as exc:
            errors.append(f"attempt {attempt}: {exc}")
            if attempt < attempts:
                time.sleep(3 * attempt)
    raise RuntimeError(f"{opening_id} contrastive annotation failed: {'; '.join(errors)}")


def root_lesson_text(lessons: list[dict[str, Any]]) -> str:
    lines = [
        "## Contrastive Lessons",
        "",
        "Use these mistake-to-correction pairs only when the live situation matches.",
        "",
    ]
    for lesson in lessons:
        lines.extend(
            [
                f"### {lesson['lesson_id']} — {lesson['title']}",
                "",
                f"**When:** {lesson['when']}",
                "",
                f"**Mistake → correction:** {lesson['mistake']} → {lesson['correction']}",
                "",
                f"**Why:** {lesson['why']}",
                "",
                f"**Read for full checks:** `{lesson['target_node_id']}`",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n\n"


def node_lesson_text(lessons: list[dict[str, Any]]) -> str:
    lines = ["## Contrastive Mistake → Correction", ""]
    for lesson in lessons:
        lines.extend(
            [
                f"### {lesson['lesson_id']} — {lesson['title']}",
                "",
                f"**When this applies:** {lesson['when']}",
                "",
                f"**Mistake:** {lesson['mistake']}",
                "",
                f"**Correction:** {lesson['correction']}",
                "",
                f"**Why:** {lesson['why']}",
                "",
                f"**Recheck when:** {lesson['recheck']}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n\n"


def compile_one(repo_root: Path, opening_id: str, result: dict[str, Any]) -> None:
    base_root = repo_root / "SKILL_MINING_V2_READABLE" / BASE_METHOD
    output_root = repo_root / "SKILL_MINING_V2_READABLE" / OUTPUT_METHOD
    race = {"P": "protoss", "T": "terran", "Z": "zerg"}[opening_id[0]]
    matchup = opening_id[:3]
    src = base_root / race / matchup / opening_id
    dest = output_root / race / matchup / opening_id
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest)

    index_path = dest / "index.json"
    index = read_json(index_path)
    index["method"] = OUTPUT_METHOD
    write_json(index_path, index)

    lessons = result["annotation"]["lessons"]
    root_path = dest / "SKILL.md"
    root_text = root_path.read_text(encoding="utf-8")
    root_text = root_text.replace("- Method: Positive Only", "- Method: Contrastive Full V3")
    marker = "## Decision Nodes"
    if marker not in root_text:
        raise ValueError(f"root compile marker missing: {root_path}")
    write_text(root_path, root_text.replace(marker, root_lesson_text(lessons) + marker, 1))

    by_node: dict[str, list[dict[str, Any]]] = {}
    for lesson in lessons:
        by_node.setdefault(str(lesson["target_node_id"]), []).append(lesson)
    for node_id, node_lessons in by_node.items():
        node_path = dest / "nodes" / f"{node_id}.md"
        node_text = node_path.read_text(encoding="utf-8")
        node_marker = "## What This Does NOT Mean"
        if node_marker not in node_text:
            raise ValueError(f"node compile marker missing: {node_path}")
        write_text(
            node_path,
            node_text.replace(node_marker, node_lesson_text(node_lessons) + node_marker, 1),
        )

    provenance_dir = dest / "provenance"
    provenance_dir.mkdir(exist_ok=True)
    write_json(provenance_dir / "private_contrastive_synthesis.json", result)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--attempts", type=int, default=3)
    parser.add_argument("--openings", default="")
    parser.add_argument("--no-resume", action="store_true")
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()
    output_root = repo_root / "analysis" / "outputs_readable_skill_v1"
    stage1 = output_root / "01_method_ir"
    stage2 = output_root / "02_observation_projection"
    stage3 = output_root / "03_semantic_annotation"
    result_root = output_root / "08_full_contrastive_v3"
    all_ids = opening_ids(stage3)
    ids = list(all_ids)
    if args.openings:
        requested = {item.strip() for item in args.openings.split(",") if item.strip()}
        ids = [item for item in ids if item in requested]
        if set(ids) != requested:
            raise ValueError(f"unknown opening ids: {sorted(requested - set(ids))}")
    private_nodes = collect_private_nodes(stage1, stage2, stage3, all_ids)

    def work(opening_id: str) -> tuple[str, dict[str, Any]]:
        output_path = result_root / f"{opening_id}.json"
        public_projection = read_json(stage2 / BASE_METHOD / f"{opening_id}.json")
        public_semantic = read_json(stage3 / BASE_METHOD / f"{opening_id}.json")
        candidates, provenance = select_pairs(
            opening_id, public_projection, public_semantic, private_nodes
        )
        if output_path.exists() and not args.no_resume:
            cached = read_json(output_path)
            validate_annotation(cached.get("annotation") or {}, candidates)
            return opening_id, cached
        result = call_one(
            repo_root=repo_root,
            opening_id=opening_id,
            candidates=candidates,
            provenance=provenance,
            attempts=args.attempts,
        )
        write_json(output_path, result)
        return opening_id, result

    completed: dict[str, dict[str, Any]] = {}
    with ThreadPoolExecutor(max_workers=args.workers) as executor:
        futures = {executor.submit(work, opening_id): opening_id for opening_id in ids}
        for future in as_completed(futures):
            opening_id, result = future.result()
            completed[opening_id] = result
            print(f"[contrastive-v3] {opening_id}: {result['annotation_source']}", flush=True)
    for opening_id in ids:
        compile_one(repo_root, opening_id, completed[opening_id])
    summary = {
        "schema_version": 1,
        "method": OUTPUT_METHOD,
        "base_public_method": BASE_METHOD,
        "private_evidence_method": EVIDENCE_METHOD,
        "model_key": MODEL_KEY,
        "skills": len(ids),
        "lessons": sum(len(item["annotation"]["lessons"]) for item in completed.values()),
        "annotation_sources": sorted({item["annotation_source"] for item in completed.values()}),
        "reasoning_present": sum(bool(item["llm_metadata"]["reasoning_present"]) for item in completed.values()),
        "api_errors": sum(bool(item["llm_metadata"]["error"]) for item in completed.values()),
        "agent_visible_private_nodes": 0,
    }
    write_json(result_root / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
