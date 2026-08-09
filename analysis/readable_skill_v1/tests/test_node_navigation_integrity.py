from analysis.readable_skill_v1.common.validation import validate_skill


def test_missing_child_fails(minimal_skill, tmp_path):
    skill = minimal_skill(children=["N999"])
    entity = tmp_path / "entities.json"
    entity.write_text('{"units":{},"upgrades":{}}')
    assert any("missing child" in error for error in validate_skill(skill, "full_signed_graph", entity))
