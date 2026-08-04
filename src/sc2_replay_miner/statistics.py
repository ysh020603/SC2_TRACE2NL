"""Aggregate unit/building/upgrade statistics from macro events."""

from __future__ import annotations

from collections import Counter, defaultdict

from sc2_replay_miner.models import MacroEventRecord, ParsedReplay


def summarize_player_macro(events: list[MacroEventRecord]) -> dict[int, dict[str, dict[str, int]]]:
    """Return per-player counters for units/buildings/upgrades."""
    out: dict[int, dict[str, dict[str, int]]] = defaultdict(
        lambda: {"units": Counter(), "buildings": Counter(), "upgrades": Counter()}
    )
    for event in events:
        if event.is_initial:
            continue
        bucket = out[event.player_id]
        if event.category in {"unit_born", "unit_started"}:
            bucket["units"][event.canonical_name] += 1
        elif event.category in {"building_start", "building_complete", "tech_morph"}:
            if event.category == "building_complete":
                continue
            bucket["buildings"][event.canonical_name] += 1
        elif event.category == "upgrade_complete":
            bucket["upgrades"][event.canonical_name] += 1
    # Convert counters to plain dicts
    return {
        pid: {
            "units": dict(vals["units"]),
            "buildings": dict(vals["buildings"]),
            "upgrades": dict(vals["upgrades"]),
        }
        for pid, vals in out.items()
    }


def attach_statistics(parsed: ParsedReplay) -> ParsedReplay:
    parsed.extras["player_statistics"] = summarize_player_macro(parsed.macro_events)
    return parsed
