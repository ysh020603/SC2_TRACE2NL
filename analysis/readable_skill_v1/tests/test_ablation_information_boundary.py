from analysis.readable_skill_v1.common.method_policy import policy


def test_six_method_boundaries_are_distinct():
    assert policy("full_signed_graph")["graph"]
    assert not policy("ablation_flat_adaptive")["graph"]
    assert not policy("ablation_single_trace")["population"]
    assert not policy("ablation_static_population")["opponent"]
    assert "harmful" not in policy("ablation_positive_only")["labels"]
    assert not policy("ablation_frequency_only")["value"]
