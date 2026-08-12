from __future__ import annotations

import importlib.util
import json
from pathlib import Path

import pytest


MODULE_PATH = Path(__file__).resolve().parents[1] / "build_failure_aware_full_v4.py"
SPEC = importlib.util.spec_from_file_location("build_failure_aware_full_v4", MODULE_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(MODULE)
ROOT = Path(__file__).resolve().parents[3]
SKILLS = ROOT / "SKILL_MINING_V2_READABLE"
OUTPUTS = ROOT / "analysis" / "outputs_readable_skill_v1" / "09_full_failure_aware_v4"


def annotation():
    return {"rules": [
        {
            "rule_id": "R01",
            "title": "Production tempo",
            "when": "When the opening has a large bank and insufficient usable production.",
            "correction": "Add executable production and combat units before optional economy.",
            "check": "At the next decision cycle, recheck bank, active queues, and army supply.",
        },
        {
            "rule_id": "R02",
            "title": "Observed counter",
            "when": "When Enemy Intelligence shows a ground-heavy opponent composition.",
            "correction": "Prioritize available ground counters while maintaining production.",
            "check": "At the next decision cycle, recheck the observed enemy composition and own counters.",
        },
        {
            "rule_id": "R03",
            "title": "Army recovery",
            "when": "When army supply is low or predicted advantage is OverwhelmingDisadvantage.",
            "correction": "Convert the bank into production, combat units, counters, and detection.",
            "check": "At the next decision cycle, recheck army supply, bank, threats, and predicted advantage.",
        },
    ]}


def test_validate_annotation_requires_exact_contract():
    MODULE.validate_annotation(annotation())
    invalid = annotation()
    invalid["rules"][0]["when"] = "The failed game showed a weak army."
    with pytest.raises(ValueError, match="private provenance"):
        MODULE.validate_annotation(invalid)


def test_normalize_annotation_rewrites_subcycle_recheck():
    payload = annotation()
    payload["rules"][0]["check"] = "Recheck every 30 seconds: inspect the active queues."
    normalized = MODULE.normalize_annotation(payload)
    assert "next decision cycle" in normalized["rules"][0]["check"]
    MODULE.validate_annotation(normalized)


def test_normalize_annotation_removes_no_threat_gate():
    payload = annotation()
    payload["rules"][0]["when"] += " and there is no immediate threat"
    normalized = MODULE.normalize_annotation(payload)
    assert "no immediate threat" not in normalized["rules"][0]["when"].lower()
    MODULE.validate_annotation(normalized)


def test_compile_injects_guardrails_and_preserves_v3(tmp_path):
    base_root = tmp_path / "full_contrastive_graph_v3"
    source = base_root / "protoss" / "PvP" / "PvP_O01"
    (source / "nodes").mkdir(parents=True)
    (source / "index.json").write_text(
        json.dumps(
            {
                "skill_id": "PvP_O01",
                "method": "full_contrastive_graph_v3",
                "root": "SKILL.md",
                "nodes": {"N001": {"path": "nodes/N001.md", "type": "default", "children": []}},
            }
        ),
        encoding="utf-8",
    )
    (source / "SKILL.md").write_text(
        "# Skill\n- Method: Contrastive Full V3\n\n## Contrastive Lessons\n\nExisting V3 lesson.\n",
        encoding="utf-8",
    )
    (source / "nodes" / "N001.md").write_text(
        "# N001\n\n## What This Does NOT Mean\n\nKeep live-state priority.\n",
        encoding="utf-8",
    )
    result = {"annotation": annotation()}
    output_root = tmp_path / "full_failure_aware_graph_v4"
    MODULE.compile_one(source, output_root, "PvP_O01", result)
    destination = output_root / "protoss" / "PvP" / "PvP_O01"
    root = (destination / "SKILL.md").read_text(encoding="utf-8")
    node = (destination / "nodes" / "N001.md").read_text(encoding="utf-8")
    index = json.loads((destination / "index.json").read_text(encoding="utf-8"))
    assert "V4 Failure-Aware Execution Guardrails" in root
    assert "V4 Matchup-Specific Corrections" in root
    assert "Existing V3 lesson" in root
    assert "V4 Execution Recheck" in node
    assert index["method"] == "full_failure_aware_graph_v4"


def test_generated_v4_corpus_is_complete_and_private():
    base = {
        path.parent.name: path.parent
        for path in (SKILLS / MODULE.BASE_METHOD).glob("*/*/*/index.json")
    }
    generated = {
        path.parent.name: path.parent
        for path in (SKILLS / MODULE.OUTPUT_METHOD).glob("*/*/*/index.json")
    }
    assert len(base) == 57
    assert generated.keys() == base.keys()
    for opening_id, directory in generated.items():
        base_index = json.loads((base[opening_id] / "index.json").read_text(encoding="utf-8"))
        index = json.loads((directory / "index.json").read_text(encoding="utf-8"))
        comparable = dict(index)
        comparable["method"] = MODULE.BASE_METHOD
        assert comparable == base_index
        root = (directory / "SKILL.md").read_text(encoding="utf-8")
        assert "- Method: Failure-Aware Full V4" in root
        assert root.count("## V4 Failure-Aware Execution Guardrails") == 1
        assert root.count("## V4 Matchup-Specific Corrections") == 1
        assert root.count("## Contrastive Lessons") == 1
        assert not any(term in root.lower() for term in MODULE.FORBIDDEN_PUBLIC_TERMS)
        for node in (directory / "nodes").glob("*.md"):
            assert node.read_text(encoding="utf-8").count("## V4 Execution Recheck") == 1


def test_generated_annotations_are_flash_non_reasoning():
    payloads = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in OUTPUTS.glob("*.json")
        if path.name != "summary.json"
    ]
    assert len(payloads) == 57
    assert {item["annotation_source"] for item in payloads} == {"llm"}
    assert {item["llm_metadata"]["model_key"] for item in payloads} == {"DeepSeek-V4-flash"}
    assert all(item["llm_metadata"]["is_reasoning"] is False for item in payloads)
    assert not any(item["llm_metadata"]["reasoning_present"] for item in payloads)
    assert not any(item["llm_metadata"]["error"] for item in payloads)
    assert not any(item["private_failure_evidence"]["agent_visible"] for item in payloads)
    for item in payloads:
        MODULE.validate_annotation(item["annotation"])
