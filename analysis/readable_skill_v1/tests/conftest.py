from __future__ import annotations

import json
from pathlib import Path

import pytest


@pytest.fixture
def minimal_skill(tmp_path: Path):
    def build(method="full_signed_graph", node_type="positive", text="Enemy Intelligence appears ground oriented.", children=None):
        skill = tmp_path / method / "protoss" / "PvP" / "PvP_O01"
        (skill / "nodes").mkdir(parents=True, exist_ok=True)
        (skill / "SKILL.md").write_text(f"# Test\n\n## Decision Nodes\n\n[{node_type.upper()}] N001\n\n{text}\n", encoding="utf-8")
        (skill / "nodes" / "N001.md").write_text(f"# N001\n\n## Node Type\n\n{node_type.upper()}\n\n{text}\n", encoding="utf-8")
        (skill / "index.json").write_text(json.dumps({"skill_id":"PvP_O01","method":method,"root":"SKILL.md","nodes":{"N001":{"path":"nodes/N001.md","type":node_type,"title":"Test","summary":text,"trigger_summary":text,"children":children or []}}}), encoding="utf-8")
        return skill
    return build
