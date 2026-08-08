"""Shared I/O helpers for the analysis pipeline."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Iterator

import pandas as pd

from analysis.pipeline.taxonomy import normalize_race

MATCHUPS = ("PvP", "PvT", "PvZ", "TvT", "TvZ", "ZvZ")
HORIZONS = (210, 300, 420)
PRIMARY_HORIZON = 300


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def iter_action_json(action_root: Path) -> Iterator[tuple[str, Path, dict[str, Any]]]:
    for matchup in MATCHUPS:
        d = action_root / matchup
        if not d.is_dir():
            continue
        for path in sorted(d.glob("*.json")):
            name = path.name
            if (
                name.startswith("summary")
                or name.endswith("_summary.json")
                or name in {"full_parse_summary.json", "parse_errors.jsonl"}
            ):
                continue
            data = json.loads(path.read_text(encoding="utf-8"))
            yield matchup, path, data


def player_views(data: dict[str, Any], matchup_dir: str) -> list[dict[str, Any]]:
    players = list(data.get("players") or [])
    views: list[dict[str, Any]] = []
    for p in players:
        opp = next((x for x in players if x.get("player_id") != p.get("player_id")), None)
        race = normalize_race(p.get("race")) or p.get("race")
        opp_race = None if opp is None else (normalize_race(opp.get("race")) or opp.get("race"))
        mmr = p.get("mmr") if p.get("mmr_available", True) else None
        opp_mmr = None
        if opp is not None and opp.get("mmr_available", True):
            opp_mmr = opp.get("mmr")
        try:
            mmr_f = float(mmr) if mmr is not None else None
        except (TypeError, ValueError):
            mmr_f = None
        try:
            opp_mmr_f = float(opp_mmr) if opp_mmr is not None else None
        except (TypeError, ValueError):
            opp_mmr_f = None
        views.append(
            {
                "replay_id": data.get("replay_id"),
                "player_id": p.get("player_id"),
                "race": race,
                "race_raw": p.get("race"),
                "opponent_race": opp_race,
                "result": p.get("result"),
                "mmr": mmr_f,
                "opponent_mmr": opp_mmr_f,
                "mmr_diff": None
                if mmr_f is None or opp_mmr_f is None
                else mmr_f - opp_mmr_f,
                "matchup_dir": matchup_dir,
                "matchup": data.get("matchup"),
                "map_name": data.get("map_name"),
                "version": data.get("version"),
                "base_build": data.get("base_build"),
                "region": data.get("region"),
                "played_at": data.get("played_at"),
                "duration_real_seconds": data.get("duration_seconds"),
                "build_order": list(p.get("build_order") or []),
            }
        )
    return views


def ensure_dir(path: Path) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_json(path: Path, obj: Any) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def load_player_table(tables_dir: Path) -> pd.DataFrame:
    return pd.read_parquet(tables_dir / "player_games.parquet")


def load_replay_table(tables_dir: Path) -> pd.DataFrame:
    return pd.read_parquet(tables_dir / "replays.parquet")
