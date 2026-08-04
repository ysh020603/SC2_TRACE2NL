"""Export parsed records to Parquet / JSON / markdown."""

from __future__ import annotations

import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any

import pandas as pd

from sc2_replay_miner.event_utils import format_clock
from sc2_replay_miner.models import (
    BuildOrderRecord,
    MacroEventRecord,
    ParsedReplay,
    PlayerRecord,
    ReplayRecord,
)

TABLE_NAMES = ("replays", "players", "macro_events", "build_orders")

# Categories kept in the human-facing full-game BO timeline.
FULL_BO_CATEGORIES = {
    "building_start",
    "tech_morph",
    "upgrade_complete",
    "unit_born",
    "unit_started",
}


def _bo_action_label(category: str) -> str:
    return {
        "building_start": "started",
        "building_complete": "completed",
        "tech_morph": "morphed",
        "upgrade_complete": "completed",
        "unit_born": "born",
        "unit_started": "started",
        "unit_died": "died",
        "unknown_macro": "unknown",
    }.get(category, category)


def _timeline_item_from_bo(record: BuildOrderRecord, player: PlayerRecord | None) -> dict[str, Any]:
    item: dict[str, Any] = {
        "time": format_clock(record.second),
        "second": record.second,
        "frame": record.frame,
        "player_id": record.player_id,
        "player_name": player.player_name if player else None,
        "race": player.play_race if player else None,
        "event": record.category,
        "action": _bo_action_label(record.category),
        "name": record.canonical_name,
        "occurrence_index": record.occurrence_index,
        "x": record.x,
        "y": record.y,
        "text": (
            f"{format_clock(record.second)} "
            f"{record.canonical_name}"
            f"{f' #{record.occurrence_index}' if record.occurrence_index else ''} "
            f"{_bo_action_label(record.category)}"
        ).strip(),
    }
    return item


def build_full_match_json(parsed: ParsedReplay) -> dict[str, Any]:
    """One self-contained JSON object for a complete match."""
    players = [p for p in parsed.players if not p.is_observer]
    player_by_id = {p.player_id: p for p in players}
    winners = [p for p in players if (p.result or "").lower() == "win"]
    winner = winners[0] if len(winners) == 1 else None
    duration = parsed.replay.game_length_seconds

    stats = parsed.extras.get("player_statistics", {})

    full_bo_records = [
        b
        for b in parsed.build_orders
        if b.bo_type == "all_macro" and b.category in FULL_BO_CATEGORIES
    ]
    full_bo_records.sort(key=lambda b: (b.frame, b.player_id, b.bo_index))

    timeline = [
        _timeline_item_from_bo(record, player_by_id.get(record.player_id))
        for record in full_bo_records
    ]

    player_blocks: list[dict[str, Any]] = []
    for player in sorted(players, key=lambda p: p.player_id):
        by_type: dict[str, list[dict[str, Any]]] = {
            "full": [],
            "core_6m": [],
            "strategy_8m": [],
        }
        for record in parsed.build_orders:
            if record.player_id != player.player_id:
                continue
            item = _timeline_item_from_bo(record, player)
            # Drop player_* duplication inside per-player lists.
            item.pop("player_id", None)
            item.pop("player_name", None)
            item.pop("race", None)
            if record.bo_type == "all_macro" and record.category in FULL_BO_CATEGORIES:
                by_type["full"].append(item)
            elif record.bo_type == "core_6m":
                by_type["core_6m"].append(item)
            elif record.bo_type == "strategy_8m":
                by_type["strategy_8m"].append(item)

        for values in by_type.values():
            values.sort(key=lambda x: (x["frame"], x["second"], x["name"]))

        player_blocks.append(
            {
                "player_id": player.player_id,
                "name": player.player_name,
                "race": player.play_race,
                "pick_race": player.pick_race,
                "result": player.result,
                "mmr": player.mmr,
                "mmr_available": player.mmr_available,
                "team_id": player.team_id,
                "is_winner": (player.result or "").lower() == "win",
                "initial_state": parsed.initial_state.get(player.player_id, {}),
                "statistics": stats.get(player.player_id, {}),
                "build_order": by_type["full"],
                "build_order_core_6m": by_type["core_6m"],
                "build_order_strategy_8m": by_type["strategy_8m"],
            }
        )

    matchup = "".join(sorted((p.play_race or "?")[0] for p in players)) if players else None
    winners_payload = [
        {
            "player_id": p.player_id,
            "name": p.player_name,
            "race": p.play_race,
            "mmr": p.mmr,
            "team_id": p.team_id,
        }
        for p in winners
    ]

    return {
        "replay_id": parsed.replay.replay_id,
        "source_file": parsed.replay.source_file,
        "map_name": parsed.replay.map_name,
        "version": parsed.replay.release_string,
        "base_build": parsed.replay.base_build,
        "duration_seconds": duration,
        "duration_clock": format_clock(duration or 0),
        "game_type": parsed.replay.game_type,
        "real_type": parsed.replay.real_type,
        "region": parsed.replay.region,
        "played_at": parsed.replay.played_at,
        "matchup": matchup,
        "winner": (
            {
                "player_id": winner.player_id,
                "name": winner.player_name,
                "race": winner.play_race,
                "mmr": winner.mmr,
                "team_id": winner.team_id,
            }
            if winner
            else None
        ),
        "winners": winners_payload,
        "players": player_blocks,
        "timeline": timeline,
        "unknown_names": parsed.unknown_names,
        "tracker_event_counts": parsed.tracker_event_counts,
        "parser_version": parsed.replay.parser_version,
    }


def write_full_match_json(parsed: ParsedReplay, output_path: str | Path) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = build_full_match_json(parsed)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return output_path


def write_full_matches(
    parsed_list: list[ParsedReplay],
    output_dir: str | Path,
) -> tuple[Path, list[Path]]:
    """Write one JSON per match plus a combined full_matches.json array.

    Per-match files are written directly into ``output_dir`` as ``<replay_id>.json``.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    combined: list[dict[str, Any]] = []
    written: list[Path] = []
    for parsed in parsed_list:
        payload = build_full_match_json(parsed)
        combined.append(payload)
        path = output_dir / f"{parsed.replay.replay_id}.json"
        path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        written.append(path)

    combined_path = output_dir / "full_matches.json"
    combined_path.write_text(json.dumps(combined, ensure_ascii=False, indent=2), encoding="utf-8")
    return combined_path, written


def _records_to_frame(records: Iterable[Any]) -> pd.DataFrame:
    rows = [r.model_dump() if hasattr(r, "model_dump") else dict(r) for r in records]
    if not rows:
        return pd.DataFrame()
    return pd.DataFrame(rows)


def parsed_to_tables(parsed_list: list[ParsedReplay]) -> dict[str, pd.DataFrame]:
    replays: list[ReplayRecord] = []
    players: list[PlayerRecord] = []
    macros: list[MacroEventRecord] = []
    bos: list[BuildOrderRecord] = []
    for parsed in parsed_list:
        replays.append(parsed.replay)
        players.extend(parsed.players)
        macros.extend(parsed.macro_events)
        bos.extend(parsed.build_orders)
    return {
        "replays": _records_to_frame(replays),
        "players": _records_to_frame(players),
        "macro_events": _records_to_frame(macros),
        "build_orders": _records_to_frame(bos),
    }


def write_parquet_tables(
    tables: dict[str, pd.DataFrame],
    output_dir: str | Path,
    compression: str = "zstd",
) -> dict[str, Path]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    written: dict[str, Path] = {}
    for name in TABLE_NAMES:
        df = tables.get(name, pd.DataFrame())
        path = output_dir / f"{name}.parquet"
        df.to_parquet(path, index=False, compression=compression)
        written[name] = path
    return written


def write_json_preview(parsed: ParsedReplay, output_path: str | Path) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "replay": parsed.replay.model_dump(),
        "players": [p.model_dump() for p in parsed.players],
        "initial_state": parsed.initial_state,
        "tracker_event_counts": parsed.tracker_event_counts,
        "unknown_names": parsed.unknown_names,
        "macro_events_preview": [e.model_dump() for e in parsed.macro_events[:100]],
        "build_orders_preview": {
            bo_type: [
                b.model_dump()
                for b in parsed.build_orders
                if b.bo_type == bo_type
            ][:80]
            for bo_type in ("core_6m", "strategy_8m", "all_macro")
        },
        "player_statistics": parsed.extras.get("player_statistics", {}),
    }
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return output_path


def append_jsonl(path: str | Path, record: dict[str, Any]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(record, ensure_ascii=False) + "\n")


def write_summary_report(report: dict[str, Any], output_path: str | Path) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return output_path


def write_unknown_names(names: Iterable[str], output_path: str | Path) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = sorted(set(names))
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    return output_path
