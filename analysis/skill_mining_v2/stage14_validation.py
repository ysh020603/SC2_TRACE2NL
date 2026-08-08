"""Stage 14 — leakage / graph / grounding / annotation validation."""

from __future__ import annotations

import json
from typing import Any

import pandas as pd
import pyarrow.parquet as pq

from analysis.skill_mining_v2.common.io import ensure_dir, read_json, write_json
from analysis.skill_mining_v2.common.validation import (
    validate_annotation_text,
    validate_canonical_entities,
    validate_graph,
    validate_skill_grounding,
)
from analysis.skill_mining_v2.config import PipelineConfig


def run_stage14(cfg: PipelineConfig) -> dict[str, Any]:
    out_dir = ensure_dir(cfg.stage_dir(14, "14_validation"))
    entity_index = read_json(cfg.stage_dir(2, "02_semantics") / "entity_index.json")
    skill_index = read_json(cfg.stage_dir(12, "12_skills") / "skill_index.json")
    graph_index = read_json(cfg.stage_dir(9, "09_graphs") / "graph_index.json")

    reports = {}
    totals = {
        "skills": 0,
        "graph_errors": 0,
        "grounding_errors": 0,
        "canonical_errors": 0,
        "annotation_issues": 0,
        "data_leakage_errors": 0,
    }

    leakage_errors = []
    snapshots_path = cfg.stage_dir(5, "05_snapshots") / "snapshots.parquet"
    if snapshots_path.exists():
        available = set(pq.ParquetFile(snapshots_path).schema.names)
        snapshots = pd.read_parquet(
            snapshots_path,
            columns=[
                c
                for c in (
                    "t",
                    "own_t",
                    "opp_t",
                    "resp_t0",
                    "resp_t1",
                )
                if c in available
            ],
        )
        for col in ("own_t", "opp_t"):
            if col in snapshots and not (snapshots[col] == snapshots["t"]).all():
                leakage_errors.append(f"{col} does not equal snapshot t")
        if "resp_t0" in snapshots and not (snapshots["resp_t0"] == snapshots["t"]).all():
            leakage_errors.append("response start does not equal snapshot t")
        if "resp_t1" in snapshots and not (
            snapshots["resp_t1"] <= snapshots["t"] + 60
        ).all():
            leakage_errors.append("response contains actions after t+60")
    transitions_path = cfg.stage_dir(7, "07_transitions") / "transition_table.parquet"
    if transitions_path.exists():
        transitions = pd.read_parquet(transitions_path, columns=["t", "t_next"])
        if not (transitions["t_next"] > transitions["t"]).all():
            leakage_errors.append("transition table contains non-forward time edges")
    totals["data_leakage_errors"] = len(leakage_errors)

    for opening_id, rel in skill_index.items():
        root = cfg.repo_root / rel
        skill = read_json(root / "skill.json")
        graph = read_json(root / "strategy_graph.json")
        evidence = read_json(root / "evidence.json")
        annotation = read_json(root / "annotation.json")

        g_errs = validate_graph(graph)
        ground = validate_skill_grounding(skill, evidence=evidence, graph=graph)
        ground_errs = ground.get("issues") or []

        names: list[str] = []
        for rule in skill.get("preferred_rules") or []:
            names.extend(rule.get("canonical_actions") or [])
        for step in skill.get("default_evolution") or []:
            names.extend(step.get("canonical_actions") or [])
        canon = validate_canonical_entities(names, entity_index)
        canon_errs = canon.get("unknown_entities") or []

        ann_issues = validate_annotation_text(json.dumps(annotation, ensure_ascii=False))

        leakage_ok = True
        for e in graph.get("edges") or []:
            if e.get("source_time") is not None and e.get("target_time") is not None:
                if float(e["target_time"]) <= float(e["source_time"]):
                    leakage_ok = False
                    g_errs.append("temporal_non_increasing")

        report = {
            "skill_id": opening_id,
            "graph_errors": g_errs,
            "grounding_errors": ground_errs,
            "canonical_errors": canon_errs,
            "annotation_issues": ann_issues,
            "temporal_dag_ok": leakage_ok,
            "data_leakage_errors": leakage_errors,
            "ok": (
                (not g_errs)
                and (not ground_errs)
                and (not leakage_errors)
                and leakage_ok
                and ground.get("valid", False)
            ),
        }
        write_json(root / "validation_report.json", report)
        write_json(out_dir / f"validation_{opening_id}.json", report)
        reports[opening_id] = report
        totals["skills"] += 1
        totals["graph_errors"] += len(g_errs)
        totals["grounding_errors"] += len(ground_errs)
        totals["canonical_errors"] += len(canon_errs)
        totals["annotation_issues"] += len(ann_issues)

    for opening_id, ginfo in graph_index.items():
        graph = read_json(cfg.output_root / ginfo["pruned"])
        reports.setdefault(opening_id, {})["pruned_graph_errors"] = validate_graph(graph)

    summary = {
        "totals": totals,
        "n_ok": sum(1 for r in reports.values() if r.get("ok")),
        "run_id": cfg.run_id,
    }
    write_json(out_dir / "validation_summary.json", summary)
    write_json(out_dir / "validation_reports.json", reports)

    lines = [
        "# Validation Summary",
        "",
        f"- Skills checked: {totals['skills']}",
        f"- OK: {summary['n_ok']}",
        f"- Graph errors: {totals['graph_errors']}",
        f"- Grounding errors: {totals['grounding_errors']}",
        f"- Canonical entity errors: {totals['canonical_errors']}",
        f"- Annotation issues: {totals['annotation_issues']}",
        f"- Data leakage errors: {totals['data_leakage_errors']}",
        "",
    ]
    (out_dir / "validation_report.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"[stage14] ok={summary['n_ok']}/{totals['skills']}", flush=True)
    return summary
