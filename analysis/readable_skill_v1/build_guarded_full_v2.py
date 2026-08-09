"""Build a guarded Full-v2 skill from Positive Only plus private failure evidence.

The public root/index remain structurally identical to Positive Only.  Failure
evidence is supplied only to the annotation call, and is compiled into a short
conditional guardrail inside each node detail.  The agent never sees the
failure nodes or their labels.
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
OUTPUT_METHOD = "full_guarded_graph_v2"
MODEL_KEY = "DeepSeek-V4-flash"
FORBIDDEN_PUBLIC_TERMS = (
    "negative",
    "failure",
    "failed",
    "losing",
    "loss",
    "worse",
    "historical",
    "trajectory",
    "sample",
    "replay",
)

SYSTEM = """You compile compact safety guardrails for a StarCraft II macro skill.
The public skill is based on successful/default adaptive situations. Separate
private evidence describes broad directions that correlated with poor outcomes.
Use that private evidence only to improve conditional safety checks. Never expose
its nodes, labels, provenance, outcomes, samples, trajectories, or source wording.
Do not produce a build order, action sequence, exact unseen count, causal claim,
or chain of thought. The current live observation always has priority. Return
strict JSON only."""


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


def opening_ids(stage3: Path) -> list[str]:
    return sorted(path.stem for path in (stage3 / BASE_METHOD).glob("*.json"))


def evidence_record(opening_id: str, node: dict[str, Any]) -> dict[str, str]:
    return {
        "source_opening": opening_id,
        "source_node": str(node.get("node_id") or ""),
        "situation": " ".join(
            part for part in (
                str(node.get("trigger_summary") or ""),
                str(node.get("own_situation") or ""),
                str(node.get("opponent_situation") or ""),
            ) if part
        ),
        "unsafe_direction": str(node.get("avoid_direction") or ""),
        "recheck": str(node.get("exit_or_recheck_condition") or ""),
    }


def collect_private_evidence(stage3: Path, ids: list[str]) -> dict[str, list[dict[str, str]]]:
    result: dict[str, list[dict[str, str]]] = {}
    for opening_id in ids:
        semantic = read_json(stage3 / EVIDENCE_METHOD / f"{opening_id}.json")
        nodes = semantic.get("annotation", {}).get("nodes", [])
        result[opening_id] = [
            evidence_record(opening_id, node)
            for node in nodes
            if isinstance(node, dict) and node.get("node_type") == "negative"
        ]
    return result


def select_evidence(opening_id: str, evidence: dict[str, list[dict[str, str]]]) -> list[dict[str, str]]:
    own = list(evidence.get(opening_id) or [])
    if own:
        return own
    matchup = opening_id[:3]
    same_matchup = [item for key, values in evidence.items() if key[:3] == matchup for item in values]
    if same_matchup:
        return same_matchup
    same_race = [item for key, values in evidence.items() if key[:1] == opening_id[:1] for item in values]
    return same_race or [item for values in evidence.values() for item in values]


def validate_annotation(payload: dict[str, Any], node_ids: list[str]) -> None:
    raw_nodes = payload.get("nodes")
    if not isinstance(raw_nodes, list):
        raise ValueError("guardrail response nodes must be a list")
    actual = [str(item.get("node_id") or "") for item in raw_nodes if isinstance(item, dict)]
    if actual != node_ids:
        raise ValueError(f"guardrail node identity/order mismatch: expected={node_ids}, actual={actual}")
    for item in raw_nodes:
        if set(item) != {"node_id", "guardrail", "recheck_condition"}:
            raise ValueError(f"unexpected guardrail fields for {item.get('node_id')}: {sorted(item)}")
        for field in ("guardrail", "recheck_condition"):
            value = str(item.get(field) or "").strip()
            if not value or len(value.split()) > 75:
                raise ValueError(f"invalid {field} for {item.get('node_id')}")
            lower = value.lower()
            if any(re.search(rf"\b{re.escape(term)}\b", lower) for term in FORBIDDEN_PUBLIC_TERMS):
                raise ValueError(f"private evidence leaked into {item.get('node_id')}: {value}")


def call_one(
    *,
    repo_root: Path,
    opening_id: str,
    positive: dict[str, Any],
    private_evidence: list[dict[str, str]],
    attempts: int,
) -> dict[str, Any]:
    from API_Tools.llm_caller import call_openai_detailed, load_agent_pool

    api_config = repo_root / "API_config" / "config.json"
    model_cfg = (load_agent_pool(config_path=str(api_config), force_reload=True).get("llm_agents_pool") or {}).get(MODEL_KEY)
    if not isinstance(model_cfg, dict) or model_cfg.get("is_reasoning") is not False:
        raise RuntimeError(f"{MODEL_KEY} must exist and set is_reasoning=false")
    public_nodes = []
    for node in positive.get("annotation", {}).get("nodes", []):
        public_nodes.append({
            "node_id": node["node_id"],
            "node_type": node["node_type"],
            "trigger_summary": node["trigger_summary"],
            "own_situation": node["own_situation"],
            "opponent_situation": node["opponent_situation"],
            "decision_direction": node["decision_direction"],
            "existing_recheck": node["exit_or_recheck_condition"],
        })
    node_ids = [node["node_id"] for node in public_nodes]
    contract = {
        "nodes": [
            {"node_id": node_id, "guardrail": "", "recheck_condition": ""}
            for node_id in node_ids
        ]
    }
    user = json.dumps({
        "opening_id": opening_id,
        "task": (
            "For every public node, preserve its direction and write one concise conditional safety guardrail. "
            "Phrase the guardrail only as live-observation checks and safer adaptation: what must be verified before "
            "deepening the direction, and what safer priority to use when the condition is not met. Do not mention "
            "private evidence, outcome signs, removed nodes, history, or replay provenance."
        ),
        "public_positive_or_default_nodes": public_nodes,
        "private_evidence_not_for_publication": private_evidence,
        "required_output": contract,
    }, ensure_ascii=False)
    errors: list[str] = []
    for attempt in range(1, attempts + 1):
        result = call_openai_detailed(
            messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}],
            model_key=MODEL_KEY,
            config_path=str(api_config),
            is_reasoning=False,
            temperature=0.15,
            max_tokens=6500,
            response_format={"type": "json_object"},
            timeout=360,
        )
        try:
            if result.get("is_reasoning") is not False or result.get("reasoning"):
                raise ValueError("non-reasoning contract violated")
            if result.get("error"):
                raise ValueError(str(result["error"]))
            parsed = json_object(str(result.get("content") or ""))
            validate_annotation(parsed, node_ids)
            evidence_ids = [f"{item['source_opening']}:{item['source_node']}" for item in private_evidence]
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
                "private_evidence_provenance": {
                    "source_method": EVIDENCE_METHOD,
                    "source_ids": evidence_ids,
                    "source_digest": hashlib.sha256(
                        json.dumps(private_evidence, ensure_ascii=False, sort_keys=True).encode("utf-8")
                    ).hexdigest(),
                    "agent_visible": False,
                },
            }
        except Exception as exc:
            errors.append(f"attempt {attempt}: {exc}")
            if attempt < attempts:
                time.sleep(3 * attempt)
    raise RuntimeError(f"{opening_id} guardrail annotation failed: {'; '.join(errors)}")


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

    root_path = dest / "SKILL.md"
    root_text = root_path.read_text(encoding="utf-8")
    root_text = root_text.replace("- Method: Positive Only", "- Method: Guarded Full V2")
    write_text(root_path, root_text)

    for item in result["annotation"]["nodes"]:
        node_path = dest / "nodes" / f"{item['node_id']}.md"
        node_text = node_path.read_text(encoding="utf-8")
        marker = "## What This Does NOT Mean"
        if marker not in node_text:
            raise ValueError(f"node compile marker missing: {node_path}")
        guard = (
            "## Conditional Safety Guardrail\n\n"
            f"{item['guardrail']}\n\n"
            "**Recheck when:**  \n"
            f"{item['recheck_condition']}\n\n"
        )
        write_text(node_path, node_text.replace(marker, guard + marker, 1))

    provenance = dest / "provenance"
    provenance.mkdir(exist_ok=True)
    write_json(provenance / "private_failure_synthesis.json", result)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--attempts", type=int, default=3)
    parser.add_argument("--openings", default="")
    parser.add_argument("--no-resume", action="store_true")
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()
    stage3 = repo_root / "analysis" / "outputs_readable_skill_v1" / "03_semantic_annotation"
    result_root = repo_root / "analysis" / "outputs_readable_skill_v1" / "07_full_guarded_v2"
    ids = opening_ids(stage3)
    if args.openings:
        requested = {item.strip() for item in args.openings.split(",") if item.strip()}
        ids = [item for item in ids if item in requested]
        if set(ids) != requested:
            raise ValueError(f"unknown opening ids: {sorted(requested - set(ids))}")
    evidence = collect_private_evidence(stage3, opening_ids(stage3))

    def work(opening_id: str) -> tuple[str, dict[str, Any]]:
        output_path = result_root / f"{opening_id}.json"
        if output_path.exists() and not args.no_resume:
            cached = read_json(output_path)
            positive = read_json(stage3 / BASE_METHOD / f"{opening_id}.json")
            expected = [node["node_id"] for node in positive["annotation"]["nodes"]]
            validate_annotation(cached.get("annotation") or {}, expected)
            return opening_id, cached
        positive = read_json(stage3 / BASE_METHOD / f"{opening_id}.json")
        result = call_one(
            repo_root=repo_root,
            opening_id=opening_id,
            positive=positive,
            private_evidence=select_evidence(opening_id, evidence),
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
            print(f"[guarded-v2] {opening_id}: {result['annotation_source']}", flush=True)
    for opening_id in ids:
        compile_one(repo_root, opening_id, completed[opening_id])
    summary = {
        "schema_version": 1,
        "method": OUTPUT_METHOD,
        "base_public_method": BASE_METHOD,
        "private_evidence_method": EVIDENCE_METHOD,
        "model_key": MODEL_KEY,
        "skills": len(ids),
        "nodes": sum(len(item["annotation"]["nodes"]) for item in completed.values()),
        "annotation_sources": sorted({item["annotation_source"] for item in completed.values()}),
        "reasoning_present": sum(bool(item["llm_metadata"]["reasoning_present"]) for item in completed.values()),
        "api_errors": sum(bool(item["llm_metadata"]["error"]) for item in completed.values()),
        "agent_visible_failure_nodes": 0,
    }
    write_json(result_root / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
