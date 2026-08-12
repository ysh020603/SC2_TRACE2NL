from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from analysis.readable_skill_v1.common.knowledge_grounding import KnowledgeStore


def _canonical(store: KnowledgeStore, values) -> list[str]:
    result = []
    for value in values or []:
        name = store.canonical(str(value))
        if name and name not in result:
            result.append(name)
    return result


def _combat_units(store: KnowledgeStore, values) -> list[str]:
    names = _canonical(store, values)
    result = []
    for name in names:
        item = store.entities.get(name) or {}
        if store.entity_types.get(name) != "Unit" or item.get("is_structure") or item.get("is_worker"):
            continue
        if name in {"MULE", "Larva", "Egg", "Cocoon"}:
            continue
        result.append(name)
    return result


def _properties(store: KnowledgeStore, names: list[str]) -> set[str]:
    props = set()
    for name in names:
        item = store.entities.get(name) or {}
        props.update(str(x) for x in item.get("attributes") or [])
        props.add("Air" if item.get("is_flying") else "Ground")
        for weapon in item.get("weapons") or []:
            target = weapon.get("target_type")
            if target:
                props.add(f"Attacks{target}")
    return props


def _counter_pairs(store: KnowledgeStore, subjects: list[str], objects: list[str]) -> list[tuple[str, str, str]]:
    object_set = set(objects)
    pairs = []
    for subject in subjects:
        for relation in store.by_subject.get(subject, []):
            if relation.get("relation") != "counters" or relation.get("object_name") not in object_set:
                continue
            usable, _ = store.relation_is_usable(relation)
            if usable:
                pairs.append((subject, str(relation.get("object_name")), str(relation.get("relation_id"))))
    return pairs


def analyze_match(store: KnowledgeStore, row: dict[str, Any]) -> dict[str, Any]:
    record_dir = Path(row["record_dir"])
    match = json.loads((record_dir / "match.json").read_text(encoding="utf-8"))
    signals: dict[str, list[dict[str, Any]]] = defaultdict(list)
    previous_enemy_props: set[str] = set()
    previous_plan: tuple[str, ...] | None = None
    previous_pressure = False

    for interaction in match.get("interactions") or []:
        if not interaction.get("observation_structured"):
            continue
        obs = interaction["observation_structured"]
        economy = obs.get("economy") or {}
        time = float(obs.get("time") or interaction.get("game_time") or 0)
        bank = float(economy.get("minerals") or 0) + float(economy.get("vespene") or 0)
        army_supply = float(economy.get("supply_army") or 0)
        supply_left = float(economy.get("supply_left") or 0)
        pressure = (time >= 300 and bank >= 750 and army_supply < 15) or (
            time >= 600 and bank >= 1500 and army_supply < 30
        )
        if pressure:
            signals["resource_to_army_conversion_failure"].append(
                {"time": round(time, 1), "bank": round(bank, 1), "army_supply": army_supply}
            )

        rounds = interaction.get("agent_rounds") or []
        for agent_round in rounds:
            if agent_round.get("type") != "invalid":
                continue
            error = str(agent_round.get("error") or "")
            if "supply block" in error.lower() or "supply" in error.lower() and "rejected" in error.lower():
                signals["supply_planning_repair"].append({"time": round(time, 1), "error": error[:240]})
            if any(term in error.lower() for term in ("prerequisite", "unavailable", "cannot execute", "not executable")):
                signals["prerequisite_or_execution_repair"].append({"time": round(time, 1), "error": error[:240]})

        own_forces = obs.get("own_forces") or {}
        completed = list((own_forces.get("completed") or {}).keys())
        planned = list(((interaction.get("decision") or {}).get("accepted_ordered_names") or []))
        own_units = _combat_units(store, completed + planned)
        enemy_names = _combat_units(store, list(((obs.get("enemy") or {}).get("composition") or {}).keys()))
        if own_units and enemy_names:
            own_advantage = _counter_pairs(store, own_units, enemy_names)
            enemy_advantage = _counter_pairs(store, enemy_names, own_units)
            if enemy_advantage and not own_advantage:
                signals["knowledge_visible_composition_mismatch"].append({
                    "time": round(time, 1), "own_units": own_units[:12], "enemy_units": enemy_names[:12],
                    "enemy_counter_evidence": enemy_advantage[:8],
                })

        enemy_props = _properties(store, enemy_names)
        new_props = enemy_props - previous_enemy_props
        if previous_enemy_props and new_props and not interaction.get("skill_reads_this_cycle"):
            signals["routing_not_rechecked_after_new_enemy_property"].append({
                "time": round(time, 1), "new_properties": sorted(new_props), "enemy_units": enemy_names[:12]
            })
        previous_enemy_props |= enemy_props

        plan = tuple(_combat_units(store, planned))
        if pressure and previous_pressure and plan and plan == previous_plan:
            signals["feedback_not_changing_repeated_failed_posture"].append({
                "time": round(time, 1), "repeated_combat_plan": list(plan), "bank": round(bank, 1),
                "army_supply": army_supply,
            })
        previous_plan, previous_pressure = plan, pressure

        if supply_left <= 0 and bank >= 300:
            signals["live_supply_block_with_bank"].append({
                "time": round(time, 1), "bank": round(bank, 1), "army_supply": army_supply
            })

    thresholds = {
        "resource_to_army_conversion_failure": 2,
        "supply_planning_repair": 2,
        "prerequisite_or_execution_repair": 1,
        "knowledge_visible_composition_mismatch": 2,
        "routing_not_rechecked_after_new_enemy_property": 2,
        "feedback_not_changing_repeated_failed_posture": 1,
        "live_supply_block_with_bank": 2,
    }
    present = sorted(name for name, evidence in signals.items() if len(evidence) >= thresholds[name])
    if int(row.get("decision_errors") or 0) > 0 or int(row.get("api_errors") or 0) > 0 or row.get("watchdog_recovery"):
        present.append("runtime_or_api_instability")
    return {
        "run_index": row.get("run_index"), "skill_id": row.get("skill_id"), "result": row.get("result"),
        "duration": row.get("duration"), "avg_bank": row.get("rur_float_avg_bank"),
        "army_utilization": row.get("apu_ratio"), "present_signals": sorted(set(present)),
        "evidence_counts": {name: len(items) for name, items in signals.items()},
        "evidence": {name: items[:5] for name, items in signals.items()},
    }


def analyze_report(report_path: Path, store: KnowledgeStore) -> dict[str, Any]:
    report = json.loads(report_path.read_text(encoding="utf-8"))
    matches = [analyze_match(store, row) for row in report.get("rows") or [] if row.get("valid_artifact")]
    by_result: dict[str, Counter] = defaultdict(Counter)
    totals = Counter()
    for match in matches:
        result = str(match["result"])
        totals[result] += 1
        by_result[result].update(match["present_signals"])
    prevalence = {}
    all_signals = sorted({signal for match in matches for signal in match["present_signals"]})
    for signal in all_signals:
        prevalence[signal] = {
            result: {
                "matches": by_result[result][signal],
                "total": totals[result],
                "rate": round(by_result[result][signal] / totals[result], 4) if totals[result] else 0,
            }
            for result in sorted(totals)
        }
    defeat_rank = sorted(
        all_signals,
        key=lambda signal: (
            prevalence[signal].get("Defeat", {}).get("rate", 0)
            - prevalence[signal].get("Victory", {}).get("rate", 0),
            prevalence[signal].get("Defeat", {}).get("matches", 0),
        ),
        reverse=True,
    )
    return {
        "source_report": str(report_path), "matches": len(matches), "result_totals": dict(totals),
        "prevalence_by_outcome": prevalence, "defeat_enrichment_order": defeat_rank,
        "match_diagnostics": matches,
        "interpretation_boundary": "These are process-level diagnostic signals, not proven causal labels.",
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--knowledge-root", type=Path, required=True)
    parser.add_argument("--report", type=Path, action="append", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    store = KnowledgeStore.load(args.knowledge_root)
    payload = {path.stem: analyze_report(path, store) for path in args.report}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({name: {"totals": data["result_totals"], "rank": data["defeat_enrichment_order"]} for name, data in payload.items()}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
