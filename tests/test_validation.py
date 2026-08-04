from __future__ import annotations

from sc2_replay_miner.models import (
    BuildOrderRecord,
    MacroEventRecord,
    ParsedReplay,
    PlayerRecord,
    ReplayRecord,
)
from sc2_replay_miner.validation import validate_parsed


def test_validate_detects_non_monotonic_macro():
    parsed = ParsedReplay(
        replay=ReplayRecord(
            replay_id="x",
            source_file="a.SC2Replay",
            file_sha256="0" * 64,
            file_size=1,
        ),
        players=[
            PlayerRecord(replay_id="x", player_id=1, mmr=None, mmr_available=False),
            PlayerRecord(replay_id="x", player_id=2, mmr=None, mmr_available=False),
        ],
        macro_events=[
            MacroEventRecord(
                replay_id="x",
                player_id=1,
                frame=200,
                second=20,
                event_type="UnitInitEvent",
                category="building_start",
                raw_name="Barracks",
                canonical_name="Barracks",
            ),
            MacroEventRecord(
                replay_id="x",
                player_id=1,
                frame=100,
                second=10,
                event_type="UnitInitEvent",
                category="building_start",
                raw_name="SupplyDepot",
                canonical_name="SupplyDepot",
            ),
        ],
        build_orders=[
            BuildOrderRecord(
                replay_id="x",
                player_id=1,
                bo_type="core_6m",
                bo_index=0,
                frame=200,
                second=20,
                category="building_start",
                canonical_name="Barracks",
            ),
            BuildOrderRecord(
                replay_id="x",
                player_id=1,
                bo_type="core_6m",
                bo_index=1,
                frame=100,
                second=10,
                category="building_start",
                canonical_name="SupplyDepot",
            ),
        ],
    )
    errors = validate_parsed(parsed)
    assert any("not monotonic" in e for e in errors)


def test_mmr_null_is_allowed():
    parsed = ParsedReplay(
        replay=ReplayRecord(
            replay_id="x",
            source_file="a.SC2Replay",
            file_sha256="0" * 64,
            file_size=1,
        ),
        players=[
            PlayerRecord(replay_id="x", player_id=1, mmr=None, mmr_available=False),
        ],
    )
    assert validate_parsed(parsed) == []
