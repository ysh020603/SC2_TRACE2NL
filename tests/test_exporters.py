from __future__ import annotations

from pathlib import Path

import pytest

from sc2_replay_miner.exporters import build_full_match_json, write_full_match_json
from sc2_replay_miner.parser import ReplayParser

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = PROJECT_ROOT / "configs"
REPLAY_DIRS = (
    PROJECT_ROOT / "data" / "replays" / "sc2reader_official",
    PROJECT_ROOT / "data" / "replays" / "human_tournament",
)


def _one_replay() -> Path | None:
    for folder in REPLAY_DIRS:
        files = sorted(folder.glob("*.SC2Replay"))
        if files:
            return files[0]
    return None


@pytest.mark.skipif(_one_replay() is None, reason="no test replays available")
def test_full_match_json_has_timeline_and_winner(tmp_path: Path):
    replay = _one_replay()
    assert replay is not None
    parsed = ReplayParser(config_dir=CONFIG_DIR).parse(replay)
    payload = build_full_match_json(parsed)

    assert payload["replay_id"]
    assert payload["map_name"]
    assert payload["duration_clock"]
    assert len(payload["players"]) >= 2
    assert "timeline" in payload
    assert isinstance(payload["timeline"], list)
    assert len(payload["timeline"]) > 0

    first = payload["timeline"][0]
    assert "time" in first
    assert "second" in first
    assert "name" in first
    assert "event" in first
    assert "player_id" in first

    for player in payload["players"]:
        assert "race" in player
        assert "result" in player
        assert "build_order" in player
        assert isinstance(player["build_order"], list)

    winners = [p for p in payload["players"] if p.get("is_winner")]
    assert "winners" in payload
    if len(winners) == 1:
        assert payload["winner"] is not None
        assert payload["winner"]["player_id"] == winners[0]["player_id"]
    elif len(winners) > 1:
        # e.g. 2v2: multiple winners, no single winner field
        assert payload["winner"] is None
        assert len(payload["winners"]) == len(winners)

    out = write_full_match_json(parsed, tmp_path / "full_match.json")
    assert out.exists()
    assert out.stat().st_size > 100
