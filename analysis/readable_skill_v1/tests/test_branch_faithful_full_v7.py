from analysis.readable_skill_v1.build_branch_faithful_full_v7 import use_v4


def test_v7_branch_and_contract_selection_boundary():
    assert use_v4("PvP_O01")
    assert use_v4("TvZ_O05")
    assert not use_v4("PvT_O03")
    assert not use_v4("ZvT_O04")
