"""Validation helpers and summary report generation."""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

import pandas as pd

from sc2_replay_miner.models import ParsedReplay


def assert_monotonic_frames(frames: list[int], label: str) -> list[str]:
    errors: list[str] = []
    prev = None
    for frame in frames:
        if prev is not None and frame < prev:
            errors.append(f"{label} frames not monotonic: {prev} -> {frame}")
            break
        prev = frame
    return errors


def validate_parsed(parsed: ParsedReplay) -> list[str]:
    errors: list[str] = []
    player_ids = [p.player_id for p in parsed.players if not p.is_observer]
    if len(player_ids) != len(set(player_ids)):
        errors.append("duplicate player_id")

    for pid in sorted({e.player_id for e in parsed.macro_events}):
        frames = [e.frame for e in parsed.macro_events if e.player_id == pid]
        errors.extend(assert_monotonic_frames(frames, f"macro pid={pid}"))

    for bo_type in ("core_6m", "strategy_8m", "all_macro"):
        for pid in sorted({b.player_id for b in parsed.build_orders}):
            frames = [
                b.frame
                for b in parsed.build_orders
                if b.player_id == pid and b.bo_type == bo_type
            ]
            errors.extend(assert_monotonic_frames(frames, f"{bo_type} pid={pid}"))

    for player in parsed.players:
        if player.mmr is None and player.mmr_available:
            errors.append(f"player {player.player_id} mmr_available true but mmr null")
        if player.mmr is not None and not player.mmr_available:
            errors.append(f"player {player.player_id} has mmr but mmr_available false")

    # Initial workers should not appear in core/strategy BO
    for bo in parsed.build_orders:
        if (
            bo.bo_type in {"core_6m", "strategy_8m"}
            and bo.canonical_name in {"SCV", "Probe", "Drone", "Larva"}
            and bo.category == "unit_born"
            and (bo.occurrence_index or 0) <= 12
            and bo.second <= 2
        ):
            errors.append(f"initial worker leaked into {bo.bo_type}: {bo.canonical_name}")

    return errors


def build_summary_report(
    parsed_list: list[ParsedReplay],
    errors: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    errors = errors or []
    total_files = len(parsed_list) + len(errors)
    success = [p for p in parsed_list if p.replay.parse_status == "ok"]
    players = [p for parsed in success for p in parsed.players if not p.is_observer]
    mmr_available = sum(1 for p in players if p.mmr is not None)
    one_vs_one = 0
    versions: Counter[str] = Counter()
    maps: Counter[str] = Counter()
    matchups: Counter[str] = Counter()
    event_type_counts: Counter[str] = Counter()
    nonempty_core = 0
    unknown: set[str] = set()

    for parsed in success:
        versions[str(parsed.replay.release_string)] += 1
        maps[str(parsed.replay.map_name)] += 1
        active = [p for p in parsed.players if not p.is_observer]
        if len(active) == 2:
            one_vs_one += 1
            races = "".join(sorted((p.play_race or "?")[0] for p in active))
            matchups[races] += 1
        for name, count in parsed.tracker_event_counts.items():
            event_type_counts[name] += count
        unknown.update(parsed.unknown_names)
        core = [b for b in parsed.build_orders if b.bo_type == "core_6m"]
        for pid in {b.player_id for b in core}:
            if any(b.player_id == pid for b in core):
                nonempty_core += 1

    error_type_counts = Counter(e.get("error_class") or e.get("exception_type") for e in errors)
    parse_success_rate = (len(success) / total_files) if total_files else 0.0
    mmr_coverage = (mmr_available / len(players)) if players else 0.0

    return {
        "total_files": total_files,
        "parsed_successfully": len(success),
        "parse_success_rate": parse_success_rate,
        "one_vs_one_count": one_vs_one,
        "mmr_available_players": mmr_available,
        "mmr_coverage": mmr_coverage,
        "players_with_nonempty_core_bo": nonempty_core,
        "unknown_unit_names": sorted(unknown),
        "versions": dict(versions),
        "maps": dict(maps),
        "matchups": dict(matchups),
        "event_type_counts": dict(event_type_counts),
        "error_type_counts": dict(error_type_counts),
    }


def load_parse_errors(path: str | Path) -> list[dict[str, Any]]:
    path = Path(path)
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        rows.append(json.loads(line))
    return rows


def read_parquet_tables(processed_dir: str | Path) -> dict[str, pd.DataFrame]:
    processed_dir = Path(processed_dir)
    tables = {}
    for name in ("replays", "players", "macro_events", "build_orders"):
        path = processed_dir / f"{name}.parquet"
        tables[name] = pd.read_parquet(path) if path.exists() else pd.DataFrame()
    return tables
