"""Build Full-v4 by adding experiment-grounded execution guardrails to Full-v3.

Full-v3 retains the strategic graph and contrastive lessons.  Full-v4 adds a
small universal macro safety contract plus three matchup-specific rules
annotated by DeepSeek Flash in non-reasoning mode.  Evaluation outcomes and
record provenance remain private; published rules refer only to live state.
"""

from __future__ import annotations

import argparse
import glob
import hashlib
import json
import re
import shutil
import statistics
import sys
import time
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any


BASE_METHOD = "full_contrastive_graph_v3"
OUTPUT_METHOD = "full_failure_aware_graph_v4"
MODEL_KEY = "DeepSeek-V4-flash"
RULE_COUNT = 3
FORBIDDEN_PUBLIC_TERMS = (
    "experiment",
    "evaluation",
    "failure rate",
    "failed game",
    "losing game",
    "replay",
    "run index",
    "training sample",
    "win rate",
)
WORKERS = {"SCV", "PROBE", "DRONE"}
BASES = {
    "COMMANDCENTER", "ORBITALCOMMAND", "PLANETARYFORTRESS",
    "NEXUS", "HATCHERY", "LAIR", "HIVE",
}
PRODUCTION = {
    "BARRACKS", "FACTORY", "STARPORT", "GATEWAY", "WARPGATE",
    "ROBOTICSFACILITY", "STARGATE", "HATCHERY", "LAIR", "HIVE",
}
SUPPLY = {"SUPPLYDEPOT", "PYLON", "OVERLORD", "OVERSEER"}

SYSTEM = """You write compact StarCraft II macro execution rules for a live-observation agent.
Private telemetry describes recurring macro breakdowns. Convert it into exactly three matchup-aware
rules that prevent those breakdowns while preserving the supplied opening identity. Use only cues
visible in the current observation: time, resources, income, supply, workers, army, completed and
pending structures, active queues, enemy intelligence, combat analysis, and threat flags. Rules may
use conditional numeric safety thresholds, but must not prescribe a fixed build order. Do not mention
experiments, outcomes, replays, runs, samples, statistics, or private evidence. Do not control combat
movement or attack timing. Prefer executable macro corrections: prerequisites first, concise queues,
resource conversion, production scaling, worker saturation, supply precision, counters, detection,
and recovery. Return strict JSON only; never include reasoning or chain of thought."""

SYSTEM += """
The three rules have fixed roles and order: R01 is an opening-preserving production/tempo rule;
R02 is an enemy-composition response grounded in Enemy Intelligence; R03 is a recovery override
for low army, high bank, severe predicted disadvantage, or threatened owned zones. Do not repeat
the universal supply rule. Never make a correction conditional on having no threat; danger makes
army conversion more urgent. Use 'next decision cycle' for rechecks because the macro interval is
60 game seconds. Never recommend optional expansion while army supply is below 15, production is
idle/insufficient, or predicted advantage is OverwhelmingDisadvantage. Never recommend multiple
supply providers in one decision."""


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True),
        encoding="utf-8",
    )
    temporary.replace(path)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text.rstrip() + "\n", encoding="utf-8")
    temporary.replace(path)


def json_object(text: str) -> dict[str, Any]:
    try:
        value = json.loads(text)
    except Exception:
        match = re.search(r"\{[\s\S]*\}", text or "")
        value = json.loads(match.group()) if match else {}
    return value if isinstance(value, dict) else {}


def opening_paths(base_root: Path) -> dict[str, Path]:
    return {
        path.parent.name: path.parent
        for path in base_root.glob("*/*/*/SKILL.md")
    }


def completed_count(observation: dict[str, Any], names: set[str]) -> float:
    completed = (observation.get("own_forces") or {}).get("completed") or {}
    return sum(float(count) for name, count in completed.items() if name.upper() in names)


def closest(items: list[dict[str, Any]], target: float) -> dict[str, Any] | None:
    eligible = [item for item in items if float(item.get("game_time") or 0) <= target + 35]
    return min(eligible, key=lambda item: abs(float(item["game_time"]) - target)) if eligible else None


def record_signal(row: dict[str, Any]) -> dict[str, Any]:
    record_dir = Path(row["record_dir"])
    match = read_json(record_dir / "match.json")
    interactions = [
        item for item in match.get("interactions", [])
        if isinstance(item, dict) and isinstance(item.get("observation_structured"), dict)
    ]
    checkpoints: dict[str, Any] = {}
    for target in (240, 300, 360):
        item = closest(interactions, target)
        if item is None:
            continue
        observation = item["observation_structured"]
        economy = observation.get("economy") or {}
        checkpoints[str(target)] = {
            "time": round(float(item.get("game_time") or 0), 1),
            "workers": int(economy.get("supply_workers") or 0),
            "army_supply": int(economy.get("supply_army") or 0),
            "bank": int((economy.get("minerals") or 0) + (economy.get("vespene") or 0)),
            "bases": completed_count(observation, BASES),
            "production": completed_count(observation, PRODUCTION),
            "supply_providers": completed_count(observation, SUPPLY),
        }
    human_paths = list(record_dir.glob("*.human_skill.json"))
    max_supply_entries = 0
    if human_paths:
        decisions = read_json(human_paths[0]).get("decisions") or []
        max_supply_entries = max(
            [
                sum(
                    str(name).upper() in SUPPLY
                    for name in ((decision.get("decision") or {}).get("ordered_names") or [])
                )
                for decision in decisions if isinstance(decision, dict)
            ] or [0]
        )
    return {
        "result": row["result"],
        "duration": round(float(row["duration"]), 1),
        "consume_per_min": round(float(row["rur_consume_per_min"]), 1),
        "average_bank": round(float(row["rur_float_avg_bank"]), 1),
        "apu": round(float(row["apu_ratio"]), 3),
        "decision_errors": int(row["decision_errors"]),
        "checkpoints": checkpoints,
        "max_supply_entries_in_one_queue": max_supply_entries,
    }


def aggregate_private_evidence(rows: list[dict[str, Any]]) -> dict[str, Any]:
    if not rows:
        return {"direct_matches": 0}
    signals = [record_signal(row) for row in rows]
    by_result = Counter(signal["result"] for signal in signals)
    defeats = [signal for signal in signals if signal["result"] == "Defeat"]
    checkpoint_summary: dict[str, Any] = {}
    for target in ("240", "300", "360"):
        values = [signal["checkpoints"][target] for signal in defeats if target in signal["checkpoints"]]
        if values:
            checkpoint_summary[target] = {
                key: round(statistics.mean(float(item[key]) for item in values), 1)
                for key in (
                    "workers", "army_supply", "bank", "bases", "production", "supply_providers"
                )
            }
    return {
        "direct_matches": len(signals),
        "outcome_counts_private": dict(by_result),
        "defeat_macro_average": {
            "consume_per_min": round(statistics.mean(item["consume_per_min"] for item in defeats), 1),
            "average_bank": round(statistics.mean(item["average_bank"] for item in defeats), 1),
            "apu": round(statistics.mean(item["apu"] for item in defeats), 3),
        } if defeats else {},
        "defeat_checkpoints": checkpoint_summary,
        "defeats_with_three_or_more_supply_entries": sum(
            item["max_supply_entries_in_one_queue"] >= 3 for item in defeats
        ),
        "decision_error_total": sum(item["decision_errors"] for item in signals),
    }


def validate_annotation(payload: dict[str, Any]) -> None:
    rules = payload.get("rules")
    if not isinstance(rules, list) or len(rules) != RULE_COUNT:
        raise ValueError(f"expected exactly {RULE_COUNT} rules")
    required = {"rule_id", "title", "when", "correction", "check"}
    for index, rule in enumerate(rules, 1):
        if not isinstance(rule, dict) or set(rule) != required:
            raise ValueError(f"unexpected rule fields at {index}: {sorted(rule) if isinstance(rule, dict) else rule}")
        if rule.get("rule_id") != f"R{index:02d}":
            raise ValueError(f"rule order mismatch at {index}")
        for field in required - {"rule_id"}:
            value = str(rule.get(field) or "").strip()
            if not value or len(value.split()) > 95:
                raise ValueError(f"invalid {field} at rule {index}")
        public_blob = json.dumps(rule, ensure_ascii=False).lower()
        if any(term in public_blob for term in FORBIDDEN_PUBLIC_TERMS):
            raise ValueError(f"private provenance leaked at rule {index}")
        forbidden_contract = (
            "no immediate threat",
            "multiple supply providers",
            "every 15 seconds",
            "every 30 seconds",
            "every 45 seconds",
        )
        if any(term in public_blob for term in forbidden_contract):
            raise ValueError(f"rule contradicts the v4 execution contract at {index}")
        if index == 2 and not any(
            term in public_blob
            for term in ("enemy intelligence", "enemy", "opponent", "observed")
        ):
            raise ValueError("R02 must be grounded in observed enemy composition")
        if index == 3 and not any(
            term in public_blob
            for term in ("army supply", "bank", "predicted", "threat", "disadvantage")
        ):
            raise ValueError("R03 must be a live-state recovery override")


def normalize_annotation(payload: dict[str, Any]) -> dict[str, Any]:
    """Normalize harmless sub-cycle recheck wording to the 60-second agent cycle."""

    for rule in payload.get("rules") or []:
        if not isinstance(rule, dict):
            continue
        for field in ("when", "correction", "check"):
            value = str(rule.get(field) or "")
            value = re.sub(
                r"(?i)\s+(?:and|if|when)\s+(?:there\s+is\s+)?no\s+immediate\s+threat",
                "",
                value,
            )
            value = re.sub(
                r"(?i)(?:recheck\s+)?every\s+(?:15|30|45)\s+seconds\s*:?",
                "At the next decision cycle:",
                value,
            )
            rule[field] = value
    return payload


def call_one(
    *,
    repo_root: Path,
    opening_id: str,
    root_excerpt: str,
    evidence: dict[str, Any],
    attempts: int,
) -> dict[str, Any]:
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))
    from API_Tools.llm_caller import call_openai_detailed, load_agent_pool

    config_path = repo_root / "API_config" / "config.json"
    model_config = (
        load_agent_pool(config_path=str(config_path), force_reload=True).get("llm_agents_pool") or {}
    ).get(MODEL_KEY)
    if not isinstance(model_config, dict) or model_config.get("is_reasoning") is not False:
        raise RuntimeError(f"{MODEL_KEY} must set is_reasoning=false")
    contract = {
        "rules": [
            {"rule_id": f"R{index:02d}", "title": "", "when": "", "correction": "", "check": ""}
            for index in range(1, RULE_COUNT + 1)
        ]
    }
    user = json.dumps(
        {
            "opening_id": opening_id,
            "existing_skill_excerpt": root_excerpt[:9000],
            "private_macro_telemetry": evidence,
            "universal_contract_already_published": [
                "Use a short executable queue and satisfy prerequisites before dependents.",
                "Add supply just in time; do not repeat providers already completed, pending, or queued.",
                "Convert a large bank into production and army before optional expansion or technology.",
                "Use 5- and 6-minute army/production checkpoints and override greed under threat.",
                "Keep workers flowing toward saturation without letting worker queues crowd out defense.",
            ],
            "task": (
                "Return three non-overlapping matchup-specific macro rules that complement the universal contract. "
                "R01 must preserve the opening while enforcing production tempo; R02 must respond to observed enemy "
                "composition; R03 must recover from low army/high bank/severe disadvantage. Prioritize the strongest "
                "recurring breakdowns and recheck only at the next macro decision cycle."
            ),
            "required_output": contract,
        },
        ensure_ascii=False,
    )
    errors: list[str] = []
    for attempt in range(1, attempts + 1):
        result = call_openai_detailed(
            messages=[{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}],
            model_key=MODEL_KEY,
            config_path=str(config_path),
            is_reasoning=False,
            temperature=0.1,
            max_tokens=3500,
            response_format={"type": "json_object"},
            timeout=360,
        )
        try:
            if result.get("is_reasoning") is not False or result.get("reasoning"):
                raise ValueError("non-reasoning contract violated")
            if result.get("error"):
                raise ValueError(str(result["error"]))
            parsed = normalize_annotation(json_object(str(result.get("content") or "")))
            validate_annotation(parsed)
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
                    "usage": result.get("usage") or result.get("token_usage") or {},
                    "error": "",
                    "attempt": attempt,
                },
                "private_failure_evidence": {
                    "agent_visible": False,
                    "digest": hashlib.sha256(
                        json.dumps(evidence, ensure_ascii=False, sort_keys=True).encode("utf-8")
                    ).hexdigest(),
                    "summary": evidence,
                },
            }
        except Exception as exc:
            errors.append(f"attempt {attempt}: {exc}")
            if attempt < attempts:
                time.sleep(3 * attempt)
    raise RuntimeError(f"{opening_id} v4 annotation failed: {'; '.join(errors)}")


def universal_guardrails(opening_id: str) -> str:
    race = {"P": "Protoss", "T": "Terran", "Z": "Zerg"}[opening_id[0]]
    race_note = {
        "P": "Scale Gateways or other unit-producing tech only after power, prerequisites, and production capacity are executable.",
        "T": "Scale Barracks/Factory/Starport capacity before ordering add-ons or units that lack a completed parent structure.",
        "Z": "Treat Hatchery/Lair/Hive count, larvae, Overlords, and worker/army larva competition as the production-capacity check.",
    }[opening_id[0]]
    lines = [
        "## V4 Failure-Aware Execution Guardrails",
        "",
        "Apply these checks before following any strategic direction or matchup-specific lesson.",
        "",
        "### G01 — Keep the queue executable",
        "",
        "- Rebuild the ordered queue from the live Completed, Under Construction, Active Queues, resources, supply, and prerequisites.",
        "- Put prerequisite structures before dependent add-ons, technology, upgrades, or units; omit actions whose parent will still be unavailable.",
        "- Prefer a short queue that can begin now. Do not let repeated workers, supply providers, or future tech hide the immediate army-production action.",
        "",
        "### G02 — Supply is just-in-time, not a spending plan",
        "",
        "- Count completed, pending, and already queued supply together. Add one provider when free supply is at or below 4, or two only when several active production queues will consume the space immediately.",
        "- Never add three or more supply providers in one decision. If supply is already comfortable, spend on workers, production, combat units, or required technology instead.",
        "",
        "### G03 — Convert the bank into fighting capacity",
        "",
        "- If the combined mineral and gas bank is at least 750 while production is idle or army supply is low, prioritize currently executable production structures and combat units before optional expansion or technology.",
        "- Around 05:00, aim for at least two usable unit-production sources and roughly 10 army supply. Around 06:00, if army supply is below 15, pause optional greed and restore continuous army production.",
        "- When predicted army advantage is OverwhelmingDisadvantage or an owned zone is threatened, army, counters, detection, and production take priority over expansion and nonessential technology until the live comparison improves.",
        "",
        "### G04 — Balance workers against survival",
        "",
        "- Keep worker production moving toward current base saturation, but do not queue many workers ahead of a missing production facility or urgent defensive units.",
        "- Recheck worker count, ideal workers, income, army supply, production queues, and threat flags every cycle; replace the old queue when the bottleneck changes.",
        "",
        f"### G05 — {race} production interpretation",
        "",
        f"- {race_note}",
        "",
    ]
    return "\n".join(lines)


def matchup_rules(rules: list[dict[str, Any]]) -> str:
    lines = ["## V4 Matchup-Specific Corrections", ""]
    for rule in rules:
        lines.extend([
            f"### {rule['rule_id']} — {rule['title']}",
            "",
            f"**When:** {rule['when']}",
            "",
            f"**Correction:** {rule['correction']}",
            "",
            f"**Recheck:** {rule['check']}",
            "",
        ])
    return "\n".join(lines)


def node_checks(opening_id: str) -> str:
    race_line = {
        "P": "Verify powered production and prerequisites before adding tech or combat-unit entries.",
        "T": "Verify completed parent production structures before add-ons and dependent units.",
        "Z": "Verify larvae, Overlords, bases, and worker-versus-army larva allocation.",
    }[opening_id[0]]
    return "\n".join([
        "## V4 Execution Recheck",
        "",
        "Before acting on this node:",
        "",
        "- Keep the queue short, executable, and prerequisite-ordered.",
        "- Count completed, pending, and queued supply; never repeat three supply providers in one decision.",
        "- At bank ≥750 or army supply <10 near 05:00, convert resources into production and combat units before optional greed.",
        "- At army supply <15 near 06:00 or under OverwhelmingDisadvantage, override economy/tech with army, counters, detection, and production.",
        f"- {race_line}",
        "",
    ])


def compile_one(base_dir: Path, output_root: Path, opening_id: str, result: dict[str, Any]) -> None:
    destination = output_root / base_dir.relative_to(base_dir.parents[2])
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(base_dir, destination)

    index_path = destination / "index.json"
    index = read_json(index_path)
    index["method"] = OUTPUT_METHOD
    write_json(index_path, index)

    root_path = destination / "SKILL.md"
    root_text = root_path.read_text(encoding="utf-8")
    root_text = root_text.replace("- Method: Contrastive Full V3", "- Method: Failure-Aware Full V4")
    marker = "## Contrastive Lessons"
    if marker not in root_text:
        raise ValueError(f"root compile marker missing: {root_path}")
    insertion = universal_guardrails(opening_id) + "\n" + matchup_rules(result["annotation"]["rules"])
    write_text(root_path, root_text.replace(marker, insertion + "\n" + marker, 1))

    for node_path in sorted((destination / "nodes").glob("*.md")):
        node_text = node_path.read_text(encoding="utf-8")
        marker = "## What This Does NOT Mean"
        if marker not in node_text:
            raise ValueError(f"node compile marker missing: {node_path}")
        write_text(node_path, node_text.replace(marker, node_checks(opening_id) + "\n" + marker, 1))

    provenance = destination / "provenance"
    provenance.mkdir(exist_ok=True)
    write_json(provenance / "failure_aware_synthesis.json", result)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--report", type=Path, default=None)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--attempts", type=int, default=3)
    parser.add_argument("--openings", default="")
    parser.add_argument("--no-resume", action="store_true")
    args = parser.parse_args()

    repo_root = args.repo_root.resolve()
    base_root = repo_root / "SKILL_MINING_V2_READABLE" / BASE_METHOD
    output_root = repo_root / "SKILL_MINING_V2_READABLE" / OUTPUT_METHOD
    result_root = repo_root / "analysis" / "outputs_readable_skill_v1" / "09_full_failure_aware_v4"
    report_path = args.report or (
        repo_root / "SC2-Agent-human-skill" / "game_records" / "_human_skill_ablation"
        / "human_skill_deepseek_flash_nothinking_30x8_fullv3_eval_20260811" / "analysis_all8_60.json"
    )
    report = read_json(report_path)
    v3_rows = [row for row in report.get("rows", []) if row.get("method") == "full_v3"]
    rows_by_skill: dict[str, list[dict[str, Any]]] = defaultdict(list)
    rows_by_race: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in v3_rows:
        rows_by_skill[str(row["skill_id"])].append(row)
        rows_by_race[str(row["skill_id"])[0]].append(row)

    base_dirs = opening_paths(base_root)
    ids = sorted(base_dirs)
    if args.openings:
        requested = {item.strip() for item in args.openings.split(",") if item.strip()}
        ids = [item for item in ids if item in requested]
        if set(ids) != requested:
            raise ValueError(f"unknown opening ids: {sorted(requested - set(ids))}")

    evidence_cache: dict[str, dict[str, Any]] = {}
    race_cache = {race: aggregate_private_evidence(rows) for race, rows in rows_by_race.items()}

    def work(opening_id: str) -> tuple[str, dict[str, Any]]:
        direct = aggregate_private_evidence(rows_by_skill.get(opening_id, []))
        evidence = {
            "opening": direct,
            "bot_race": race_cache.get(opening_id[0], {"direct_matches": 0}),
            "scope_note_private": (
                "opening-specific plus race evidence" if direct["direct_matches"]
                else "no direct opening matches; generalize only the same bot race evidence"
            ),
        }
        evidence_cache[opening_id] = evidence
        output_path = result_root / f"{opening_id}.json"
        if output_path.exists() and not args.no_resume:
            cached = read_json(output_path)
            validate_annotation(cached.get("annotation") or {})
            return opening_id, cached
        root_excerpt = (base_dirs[opening_id] / "SKILL.md").read_text(encoding="utf-8")
        result = call_one(
            repo_root=repo_root,
            opening_id=opening_id,
            root_excerpt=root_excerpt,
            evidence=evidence,
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
            print(f"[failure-aware-v4] {opening_id}: {result['annotation_source']}", flush=True)

    for opening_id in ids:
        compile_one(base_dirs[opening_id], output_root, opening_id, completed[opening_id])

    summary = {
        "schema_version": 1,
        "method": OUTPUT_METHOD,
        "base_method": BASE_METHOD,
        "model_key": MODEL_KEY,
        "skills": len(ids),
        "rules": sum(len(item["annotation"]["rules"]) for item in completed.values()),
        "directly_evaluated_skills": sum(bool(rows_by_skill.get(opening_id)) for opening_id in ids),
        "annotation_sources": sorted({item["annotation_source"] for item in completed.values()}),
        "reasoning_present": sum(bool(item["llm_metadata"]["reasoning_present"]) for item in completed.values()),
        "api_errors": sum(bool(item["llm_metadata"]["error"]) for item in completed.values()),
        "agent_visible_private_evidence": 0,
    }
    write_json(result_root / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
