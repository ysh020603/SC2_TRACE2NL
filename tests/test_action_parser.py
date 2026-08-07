from __future__ import annotations

from pathlib import Path

import pytest

from sc2_replay_miner.action_exporters import build_action_match_json
from sc2_replay_miner.action_parser import MacroActionParser
from sc2_replay_miner.standard_actions import StandardActionMapper

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = PROJECT_ROOT / "configs"
RAW_MATCHUPS = PROJECT_ROOT / "raw_data" / "by_matchup"
ALLOWED_CATEGORIES = {
    "production",
    "construction",
    "tech_morph",
    "upgrade_research",
}
MICRO_ABILITIES = {
    "Attack",
    "RightClick",
    "Move",
    "Patrol",
    "HoldPosition",
    "Stop",
}


def _raw_sample() -> Path | None:
    for matchup in ("PvP", "PvT", "PvZ", "TvT", "TvZ", "ZvZ"):
        files = sorted((RAW_MATCHUPS / matchup).glob("*.SC2Replay"))
        if files:
            return files[0]
    return None


@pytest.mark.skipif(_raw_sample() is None, reason="no raw Blizzard replays available")
def test_action_parser_keeps_only_macro_commands():
    replay = _raw_sample()
    assert replay is not None
    parsed = MacroActionParser(config_dir=CONFIG_DIR).parse(replay)

    assert parsed.macro_actions
    assert {action.category for action in parsed.macro_actions} <= ALLOWED_CATEGORIES
    assert not {action.ability_name for action in parsed.macro_actions} & MICRO_ABILITIES
    assert parsed.data_quality["parse_mode"] == "game_events_macro_actions"
    assert parsed.data_quality["micro_actions_included"] is False
    assert parsed.data_quality["positions_included"] is False
    assert all(action.source == "game_events" for action in parsed.macro_actions)
    assert all(action.observed_completed is False for action in parsed.macro_actions)
    assert not any(
        action.ability_name.startswith("Hallucinate")
        for action in parsed.macro_actions
    )
    assert all(action.standard_action_name for action in parsed.macro_actions)


@pytest.mark.skipif(_raw_sample() is None, reason="no raw Blizzard replays available")
def test_action_json_is_compatible_and_has_no_positions():
    replay = _raw_sample()
    assert replay is not None
    parsed = MacroActionParser(config_dir=CONFIG_DIR).parse(replay)
    payload = build_action_match_json(parsed)

    assert payload["timeline"]
    assert payload["players"]
    assert payload["macro_action_count"] == len(payload["timeline"])
    assert payload["tracker_event_counts"] == {}
    assert payload["data_quality"]["semantics"] == "player_command_intent"

    forbidden = {"x", "y", "location", "target_x", "target_y", "target_unit"}
    for action in payload["timeline"]:
        assert not forbidden & action.keys()
        assert action["action"] == "ordered"
        assert action["standard_action_name"]
    for player in payload["players"]:
        assert isinstance(player["build_order"], list)
        assert player["statistics"]["source"] == "game_events_command_intent"
        for action in player["build_order"]:
            assert not forbidden & action.keys()


def test_standard_action_mapper_uses_structured_database_names():
    mapper = StandardActionMapper()
    cases = [
        (
            "BuildSupplyDepot",
            "SupplyDepot",
            "construction",
            "TERRANBUILD_SUPPLYDEPOT",
        ),
        ("TrainSCV", "SCV", "production", "COMMANDCENTERTRAIN_SCV"),
        (
            "WarpInStalker",
            "Stalker",
            "production",
            "WARPGATETRAIN_STALKER",
        ),
        (
            "ResearchStimpack",
            "Stimpack",
            "upgrade_research",
            "BARRACKSTECHLABRESEARCH_STIMPACK",
        ),
        (
            "UpgradeGroundWeapons1",
            "GroundWeapons1",
            "upgrade_research",
            "FORGERESEARCH_PROTOSSGROUNDWEAPONSLEVEL1",
        ),
        (
            "EvolveMetabolicBoost",
            "MetabolicBoost",
            "upgrade_research",
            "RESEARCH_ZERGLINGMETABOLICBOOST",
        ),
        (
            "UpgradeStructureArmor",
            "StructureArmor",
            "upgrade_research",
            "RESEARCH_TERRANSTRUCTUREARMORUPGRADE",
        ),
    ]
    for ability, target, category, expected in cases:
        match = mapper.resolve(ability, target, category)  # type: ignore[arg-type]
        assert match.name == expected

    missing = mapper.resolve(
        "EvolvePathogenGlands",
        "PathogenGlands",
        "upgrade_research",
    )
    assert missing.name is None
    assert missing.status == "unmapped"
