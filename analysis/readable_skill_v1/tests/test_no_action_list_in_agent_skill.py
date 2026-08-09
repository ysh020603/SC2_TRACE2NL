from analysis.readable_skill_v1.common.validation import validate_skill


def test_action_list_leakage_fails(minimal_skill, tmp_path):
    skill = minimal_skill(text="canonical_actions must not appear")
    entity = tmp_path / "entities.json"
    entity.write_text('{"units":{},"upgrades":{}}')
    assert any("leakage" in error for error in validate_skill(skill, "full_signed_graph", entity))
