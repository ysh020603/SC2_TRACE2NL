from analysis.readable_skill_v1.common.obs_vocabulary import combat_cues


def test_combat_cues_are_grounded():
    vocab = {"Stalker":{"race":"Protoss","attributes":[],"section":"units"}, "Pylon":{"race":"Protoss","attributes":["Structure"],"section":"units"}}
    assert combat_cues(["Stalker", "ImaginaryUnit", "Pylon"], vocab, "Protoss") == ["Stalker"]
