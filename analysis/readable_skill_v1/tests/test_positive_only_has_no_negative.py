from analysis.readable_skill_v1.common.method_policy import allowed_badges


def test_positive_only_badges():
    assert allowed_badges("ablation_positive_only") == {"POSITIVE", "DEFAULT"}
