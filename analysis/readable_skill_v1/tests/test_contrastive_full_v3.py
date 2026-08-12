import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[3]
SKILLS = ROOT / "SKILL_MINING_V2_READABLE"
OUTPUTS = ROOT / "analysis" / "outputs_readable_skill_v1" / "08_full_contrastive_v3"
BASE_METHOD = "ablation_positive_only"
METHOD = "full_contrastive_graph_v3"
FORBIDDEN = (
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


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def skill_dirs(method: str):
    return sorted(path.parent for path in (SKILLS / method).glob("*/*/*/index.json"))


def test_contrastive_v3_preserves_positive_graph_and_publishes_lessons():
    base = {path.name: path for path in skill_dirs(BASE_METHOD)}
    contrastive = {path.name: path for path in skill_dirs(METHOD)}
    assert len(base) == 57
    assert contrastive.keys() == base.keys()
    for opening_id, directory in contrastive.items():
        base_index = load(base[opening_id] / "index.json")
        index = load(directory / "index.json")
        assert index["method"] == METHOD
        assert set(node["type"] for node in index["nodes"].values()) <= {"positive", "default"}
        comparable = dict(index)
        comparable["method"] = BASE_METHOD
        assert comparable == base_index
        root = (directory / "SKILL.md").read_text(encoding="utf-8")
        assert "- Method: Contrastive Full V3" in root
        assert root.count("## Contrastive Lessons") == 1
        assert "**Mistake → correction:**" in root
        assert not any(term in root.lower() for term in FORBIDDEN)


def test_contrastive_v3_annotations_are_deepseek_non_reasoning_and_private():
    payloads = [load(path) for path in OUTPUTS.glob("*.json") if path.name != "summary.json"]
    assert len(payloads) == 57
    assert {item["annotation_source"] for item in payloads} == {"llm"}
    assert {item["llm_metadata"]["model_key"] for item in payloads} == {"DeepSeek-V4-flash"}
    assert all(item["llm_metadata"]["is_reasoning"] is False for item in payloads)
    assert not any(item["llm_metadata"]["reasoning_present"] for item in payloads)
    assert not any(item["llm_metadata"]["error"] for item in payloads)
    assert not any(item["private_pairing_provenance"]["agent_visible"] for item in payloads)
    assert all(len(item["annotation"]["lessons"]) == 3 for item in payloads)
