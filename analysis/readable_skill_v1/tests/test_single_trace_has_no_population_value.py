from analysis.readable_skill_v1.common.method_policy import policy


def test_single_trace_boundary():
    p = policy("ablation_single_trace")
    assert not p["population"] and not p["value"] and not p["opponent"]
