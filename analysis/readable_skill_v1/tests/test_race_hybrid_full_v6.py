from analysis.readable_skill_v1.build_race_hybrid_full_v6 import use_v4


def test_v6_uses_v4_only_for_terran_and_protoss_mirror():
    assert use_v4("TvP_O02")
    assert use_v4("TvT_O03")
    assert use_v4("TvZ_O01")
    assert use_v4("PvP_O01")
    assert not use_v4("PvT_O03")
    assert not use_v4("PvZ_O02")
    assert not use_v4("ZvZ_O04")
