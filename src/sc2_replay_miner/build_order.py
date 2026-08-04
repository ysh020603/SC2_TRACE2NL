"""Build three BO views from macro events."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

from sc2_replay_miner.models import BuildOrderRecord, MacroEventRecord
from sc2_replay_miner.taxonomy import Taxonomy


def _bo_item(
    event: MacroEventRecord,
    bo_type: str,
    bo_index: int,
) -> BuildOrderRecord:
    return BuildOrderRecord(
        replay_id=event.replay_id,
        player_id=event.player_id,
        bo_type=bo_type,  # type: ignore[arg-type]
        bo_index=bo_index,
        frame=event.frame,
        second=event.second,
        category=event.category,
        canonical_name=event.canonical_name,
        occurrence_index=event.occurrence_index,
        x=event.x,
        y=event.y,
    )


def build_all_macro_bo(events: list[MacroEventRecord]) -> list[BuildOrderRecord]:
    """Whole-game macro timeline used as the source for other BO definitions."""
    ordered = sorted(
        [e for e in events if not e.is_initial],
        key=lambda e: (e.player_id, e.frame, e.event_type, e.canonical_name),
    )
    out: list[BuildOrderRecord] = []
    per_player_index: dict[int, int] = defaultdict(int)
    for event in ordered:
        # Skip pure death markers in display-oriented all_macro? Keep them for completeness.
        idx = per_player_index[event.player_id]
        out.append(_bo_item(event, "all_macro", idx))
        per_player_index[event.player_id] = idx + 1
    return out


def build_core_6m(
    events: list[MacroEventRecord],
    max_seconds: float = 360.0,
) -> list[BuildOrderRecord]:
    """Buildings starts, tech morphs, upgrades in the first N seconds (no workers/basic spam)."""
    allowed = {"building_start", "tech_morph", "upgrade_complete"}
    selected = [
        e
        for e in events
        if (not e.is_initial)
        and e.category in allowed
        and e.second <= max_seconds
    ]
    selected.sort(key=lambda e: (e.player_id, e.frame, e.canonical_name))
    out: list[BuildOrderRecord] = []
    per_player_index: dict[int, int] = defaultdict(int)
    for event in selected:
        idx = per_player_index[event.player_id]
        out.append(_bo_item(event, "core_6m", idx))
        per_player_index[event.player_id] = idx + 1
    return out


def build_strategy_8m(
    events: list[MacroEventRecord],
    taxonomy: Taxonomy,
    max_seconds: float = 480.0,
    key_unit_max: int = 2,
    basic_unit_max: int = 1,
    core_max_seconds: float = 360.0,
) -> list[BuildOrderRecord]:
    """core_6m plus first key/basic unit births within strategy window."""
    core = build_core_6m(events, max_seconds=core_max_seconds)
    # Keep core items that fall in strategy window; core already capped at 6m.
    selected: list[MacroEventRecord] = []
    # Re-materialize core as macro-like selection via events lookup
    core_keys = {
        (c.player_id, c.frame, c.category, c.canonical_name, c.occurrence_index)
        for c in core
    }
    for event in events:
        key = (
            event.player_id,
            event.frame,
            event.category,
            event.canonical_name,
            event.occurrence_index,
        )
        if key in core_keys:
            selected.append(event)

    unit_counts: dict[tuple[int, str], int] = defaultdict(int)
    for event in sorted(events, key=lambda e: (e.player_id, e.frame)):
        if event.is_initial or event.second > max_seconds:
            continue
        if event.category != "unit_born":
            continue
        name = event.canonical_name
        if taxonomy.is_worker(name) or taxonomy.is_ignored(name):
            continue
        key = (event.player_id, name)
        seen = unit_counts[key]
        limit = None
        if taxonomy.is_key_unit(name):
            limit = key_unit_max
        elif taxonomy.is_basic_army(name):
            limit = basic_unit_max
        else:
            # First appearance of other army units also useful.
            limit = 1
        if seen < limit:
            selected.append(event)
            unit_counts[key] = seen + 1

    # Deduplicate while preserving chronological order
    uniq: list[MacroEventRecord] = []
    seen_ids: set[tuple[Any, ...]] = set()
    for event in sorted(selected, key=lambda e: (e.player_id, e.frame, e.category)):
        ident = (
            event.player_id,
            event.frame,
            event.category,
            event.canonical_name,
            event.occurrence_index,
            event.unit_key,
        )
        if ident in seen_ids:
            continue
        seen_ids.add(ident)
        uniq.append(event)

    out: list[BuildOrderRecord] = []
    per_player_index: dict[int, int] = defaultdict(int)
    for event in uniq:
        idx = per_player_index[event.player_id]
        out.append(_bo_item(event, "strategy_8m", idx))
        per_player_index[event.player_id] = idx + 1
    return out


def generate_build_orders(
    events: list[MacroEventRecord],
    taxonomy: Taxonomy,
    config: dict[str, Any] | None = None,
) -> list[BuildOrderRecord]:
    bo_cfg = (config or {}).get("build_order", {})
    core_max = float(bo_cfg.get("core_max_seconds", 360))
    strategy_max = float(bo_cfg.get("strategy_max_seconds", 480))
    key_max = int(bo_cfg.get("key_unit_max_occurrences", 2))
    basic_max = int(bo_cfg.get("basic_unit_max_occurrences", 1))

    records: list[BuildOrderRecord] = []
    records.extend(build_core_6m(events, max_seconds=core_max))
    records.extend(
        build_strategy_8m(
            events,
            taxonomy=taxonomy,
            max_seconds=strategy_max,
            key_unit_max=key_max,
            basic_unit_max=basic_max,
            core_max_seconds=core_max,
        )
    )
    records.extend(build_all_macro_bo(events))
    return records
