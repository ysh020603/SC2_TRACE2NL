"""Defensive helpers for reading sc2reader tracker events."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any


def file_sha256(path: str | Path, chunk_size: int = 1024 * 1024) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        while True:
            chunk = fh.read(chunk_size)
            if not chunk:
                break
            digest.update(chunk)
    return digest.hexdigest()


def replay_id_from_sha(sha256: str) -> str:
    return sha256[:24]


def safe_int(value: Any) -> int | None:
    if value is None:
        return None
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def safe_float(value: Any) -> float | None:
    if value is None:
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def length_to_seconds(length_obj: Any) -> float | None:
    if length_obj is None:
        return None
    seconds = getattr(length_obj, "seconds", None)
    if seconds is not None:
        return float(seconds)
    total = getattr(length_obj, "total_seconds", None)
    if callable(total):
        try:
            return float(total())
        except Exception:
            pass
    try:
        hours = int(getattr(length_obj, "hours", 0) or 0)
        mins = int(getattr(length_obj, "mins", getattr(length_obj, "min", 0)) or 0)
        secs = int(getattr(length_obj, "secs", 0) or 0)
        return float(hours * 3600 + mins * 60 + secs)
    except Exception:
        return None


def resolve_player_id(event: Any) -> int | None:
    """Resolve owning player id from heterogeneous tracker event fields."""
    candidates: list[Any] = []

    controller = getattr(event, "unit_controller", None)
    if controller is not None:
        candidates.append(getattr(controller, "pid", None))

    unit = getattr(event, "unit", None)
    owner = getattr(unit, "owner", None) if unit is not None else None
    if owner is not None:
        candidates.append(getattr(owner, "pid", None))

    player = getattr(event, "player", None)
    if player is not None:
        candidates.append(getattr(player, "pid", None))

    candidates.extend(
        [
            getattr(event, "pid", None),
            getattr(event, "control_pid", None),
            getattr(event, "upkeep_pid", None),
        ]
    )

    for candidate in candidates:
        pid = safe_int(candidate)
        if pid is not None and pid > 0:
            return pid
    return None


def event_type_name(event: Any) -> str:
    return getattr(event, "name", None) or type(event).__name__


def unit_raw_name(event: Any) -> str | None:
    unit_type_name = getattr(event, "unit_type_name", None)
    if unit_type_name:
        return str(unit_type_name)
    unit = getattr(event, "unit", None)
    if unit is not None:
        name = getattr(unit, "name", None)
        if name:
            return str(name)
    return None


def unit_key(event: Any) -> str | None:
    unit = getattr(event, "unit", None)
    if unit is None:
        unit_id = getattr(event, "unit_id", None)
        return str(unit_id) if unit_id is not None else None
    unit_id = getattr(unit, "id", None)
    if unit_id is not None:
        return str(unit_id)
    event_unit_id = getattr(event, "unit_id", None)
    return str(event_unit_id) if event_unit_id is not None else None


def event_location(event: Any) -> tuple[float | None, float | None]:
    x = safe_float(getattr(event, "x", None))
    y = safe_float(getattr(event, "y", None))
    if x is not None and y is not None:
        return x, y
    location = getattr(event, "location", None)
    if location is not None and len(location) >= 2:
        return safe_float(location[0]), safe_float(location[1])
    unit = getattr(event, "unit", None)
    if unit is not None:
        loc = getattr(unit, "location", None)
        if loc is not None and len(loc) >= 2:
            return safe_float(loc[0]), safe_float(loc[1])
    return None, None


def previous_unit_type(unit: Any, current_name: str | None) -> str | None:
    """Best-effort previous type from unit.type_history for morph events."""
    if unit is None:
        return None
    history = getattr(unit, "type_history", None)
    if not history:
        return None
    try:
        items = list(history.items())
    except Exception:
        return None
    if len(items) < 2:
        # When type_history only has the new type, try comparing with unit.name
        if current_name and getattr(unit, "name", None) and unit.name != current_name:
            return str(unit.name)
        return None
    # Prefer the type immediately before the latest entry.
    prev = items[-2][1]
    prev_name = getattr(prev, "name", None)
    if prev_name:
        return str(prev_name)
    return str(prev)


def format_clock(seconds: float) -> str:
    total = max(0, int(seconds))
    mins, secs = divmod(total, 60)
    return f"{mins:02d}:{secs:02d}"
