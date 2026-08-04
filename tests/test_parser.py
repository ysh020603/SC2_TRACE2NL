from __future__ import annotations

from pathlib import Path

import pytest

from sc2_replay_miner.parser import ReplayParser
from sc2_replay_miner.validation import validate_parsed

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = PROJECT_ROOT / "configs"
REPLAY_DIRS = (
    PROJECT_ROOT / "data" / "replays" / "sc2reader_official",
    PROJECT_ROOT / "data" / "replays" / "human_tournament",
)


def _sample_replays() -> list[Path]:
    for folder in REPLAY_DIRS:
        files = sorted(folder.glob("*.SC2Replay"))
        if files:
            return files
    return []


@pytest.mark.skipif(not _sample_replays(), reason="no test replays available")
def test_parse_one_replay_has_bilateral_data():
    replay = _sample_replays()[0]
    parsed = ReplayParser(config_dir=CONFIG_DIR).parse(replay)
    assert parsed.replay.parse_status == "ok"
    assert parsed.replay.release_string
    assert parsed.replay.map_name
    assert parsed.replay.game_length_seconds is not None
    humans = [p for p in parsed.players if not p.is_observer]
    assert len(humans) >= 2
    assert len({p.player_id for p in humans}) == len(humans)
    for player in humans:
        # MMR may be null for tournament replays
        if player.mmr is None:
            assert player.mmr_available is False
        else:
            assert player.mmr_available is True
    pids_with_macros = {e.player_id for e in parsed.macro_events}
    assert any(p.player_id in pids_with_macros for p in humans)
    assert not validate_parsed(parsed)


@pytest.mark.skipif(not _sample_replays(), reason="no test replays available")
def test_initial_workers_not_in_core_bo():
    replay = _sample_replays()[0]
    parsed = ReplayParser(config_dir=CONFIG_DIR).parse(replay)
    for bo in parsed.build_orders:
        if bo.bo_type != "core_6m":
            continue
        assert bo.canonical_name not in {"SCV", "Probe", "Drone"}
        assert bo.category in {"building_start", "tech_morph", "upgrade_complete"}


def test_parse_safe_on_missing_file(tmp_path: Path):
    missing = tmp_path / "nope.SC2Replay"
    parsed, err = ReplayParser(config_dir=CONFIG_DIR).parse_safe(missing)
    assert parsed is None
    assert err is not None
    assert err.exception_type
