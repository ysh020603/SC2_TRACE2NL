import json
from pathlib import Path

import pytest

from analysis.readable_skill_v1.build_trajectory_fusion_full_v5 import (
    OUTPUT_METHOD,
    compile_one,
    validate_annotation,
)


def policies():
    return [
        {
            "phase": "early_game",
            "title": "Preserve flexible ground development",
            "applies_when": "The opening is still developing and Enemy Intelligence is incomplete.",
            "target": "Maintain flexible production and economy while preparing an observable ground response.",
            "veto": "Avoid optional technology that prevents currently executable defense.",
            "live_check": "Recheck production queues, army posture, supply, resources, and new enemy cues.",
            "routing_summary": "Preserve flexibility and resolve the immediate live bottleneck.",
        }
    ]


def test_validate_rejects_phase_identity_change():
    payload = {"phase_policies": policies()}
    validate_annotation(payload, ["early_game"])
    with pytest.raises(ValueError):
        validate_annotation(payload, ["midgame"])


def test_compile_adds_phase_metadata_and_removes_duplicate_root_nodes(tmp_path: Path):
    base = tmp_path / "base/protoss/PvZ/PvZ_O02"
    (base / "nodes").mkdir(parents=True)
    (base / "SKILL.md").write_text(
        "# Example\n\n- Method: Contrastive Full V3\n\n## Contrastive Lessons\n\nKeep.\n\n## Decision Nodes\n\nDuplicate.\n",
        encoding="utf-8",
    )
    (base / "nodes/N001.md").write_text(
        "# N001\n\n## Recommended Strategic Direction\n\nKeep.\n\n## What This Does NOT Mean\n\nNo sequence.\n",
        encoding="utf-8",
    )
    (base / "index.json").write_text(json.dumps({
        "skill_id": "PvZ_O02", "opening_name": "Example", "method": "full_contrastive_graph_v3", "root": "SKILL.md",
        "nodes": {"N001": {"path": "nodes/N001.md", "type": "default", "title": "One", "summary": "s", "trigger_summary": "t", "children": []}},
    }), encoding="utf-8")
    result = {"annotation": {"phase_policies": policies()}}
    output = tmp_path / "out"
    compile_one(base, output, "PvZ_O02", result, {"N001": "early_game"})
    compiled = output / "protoss/PvZ/PvZ_O02"
    index = json.loads((compiled / "index.json").read_text(encoding="utf-8"))
    root = (compiled / "SKILL.md").read_text(encoding="utf-8")
    node = (compiled / "nodes/N001.md").read_text(encoding="utf-8")
    assert index["method"] == OUTPUT_METHOD
    assert index["nodes"]["N001"]["phase"] == "early_game"
    assert index["nodes"]["N001"]["policy_summary"]
    assert "Trajectory-Fusion Full V5" in root
    assert "## Decision Nodes" not in root
    assert "## Runtime-Routed Decision Nodes" in root
    assert "## V5 Phase-Conditioned Trajectory Policy" in node
