from analysis.readable_skill_v1.common.method_policy import policy


def test_flat_has_no_graph():
    assert policy("ablation_flat_adaptive")["graph"] is False
