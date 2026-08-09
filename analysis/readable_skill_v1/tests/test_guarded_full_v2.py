import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SKILLS = ROOT / "SKILL_MINING_V2_READABLE"
OUTPUTS = ROOT / "analysis" / "outputs_readable_skill_v1" / "07_full_guarded_v2"
BASE_METHOD = "ablation_positive_only"
METHOD = "full_guarded_graph_v2"
FORBIDDEN_GUARDRAIL_WORDS = (
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


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def skill_dirs(method: str):
    return sorted(path.parent for path in (SKILLS / method).glob("*/*/*/index.json"))


def test_guarded_full_v2_preserves_positive_public_graph_and_hides_counterevidence():
    base = {path.name: path for path in skill_dirs(BASE_METHOD)}
    guarded = {path.name: path for path in skill_dirs(METHOD)}
    assert len(base) == 57
    assert guarded.keys() == base.keys()
    for opening_id, directory in guarded.items():
        base_index = load(base[opening_id] / "index.json")
        index = load(directory / "index.json")
        assert index["method"] == METHOD
        assert set(node["type"] for node in index["nodes"].values()) <= {"positive", "default"}
        comparable = dict(index)
        comparable["method"] = BASE_METHOD
        assert comparable == base_index
        root = (directory / "SKILL.md").read_text(encoding="utf-8")
        assert "[NEGATIVE]" not in root
        assert "- Method: Guarded Full V2" in root
        for node_id, node in index["nodes"].items():
            text = (directory / node["path"]).read_text(encoding="utf-8")
            assert text.count("## Conditional Safety Guardrail") == 1
            guard = text.split("## Conditional Safety Guardrail", 1)[1].split(
                "## What This Does NOT Mean", 1
            )[0].lower()
            assert not any(
                re.search(rf"\b{re.escape(word)}\b", guard)
                for word in FORBIDDEN_GUARDRAIL_WORDS
            )


def test_guarded_full_v2_annotations_are_all_deepseek_non_reasoning_llm():
    payloads = [load(path) for path in OUTPUTS.glob("*.json") if path.name != "summary.json"]
    assert len(payloads) == 57
    assert {item["annotation_source"] for item in payloads} == {"llm"}
    assert {item["llm_metadata"]["model_key"] for item in payloads} == {"DeepSeek-V4-flash"}
    assert all(item["llm_metadata"]["is_reasoning"] is False for item in payloads)
    assert not any(item["llm_metadata"]["reasoning_present"] for item in payloads)
    assert not any(item["llm_metadata"]["error"] for item in payloads)
    assert not any(item["private_evidence_provenance"]["agent_visible"] for item in payloads)
