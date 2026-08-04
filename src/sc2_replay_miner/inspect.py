"""Inspect a single SC2Replay and print raw structure for calibration."""

from __future__ import annotations

from collections import Counter
from pprint import pprint
from typing import Any

import sc2reader
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from sc2_replay_miner.event_utils import event_type_name

console = Console()

MACRO_FOCUS = {
    "UnitBornEvent",
    "UnitInitEvent",
    "UnitDoneEvent",
    "UnitDiedEvent",
    "UnitTypeChangeEvent",
    "UpgradeCompleteEvent",
    "PlayerStatsEvent",
}


def _safe_vars(obj: Any) -> dict[str, Any]:
    try:
        return dict(vars(obj))
    except TypeError:
        return {"repr": repr(obj)}


def inspect_replay(replay_path: str, load_level: int = 3, max_events: int = 30) -> None:
    replay = sc2reader.load_replay(replay_path, load_level=load_level, load_map=False)

    console.print(
        Panel.fit(
            "\n".join(
                [
                    f"file: {replay_path}",
                    f"release_string: {getattr(replay, 'release_string', None)}",
                    f"base_build: {getattr(replay, 'base_build', None)}",
                    f"map_name: {getattr(replay, 'map_name', None)}",
                    f"game_length: {getattr(replay, 'game_length', None)}",
                    f"game_type: {getattr(replay, 'game_type', None)}",
                    f"real_type: {getattr(replay, 'real_type', None)}",
                    f"region: {getattr(replay, 'region', None)}",
                    f"frames: {getattr(replay, 'frames', None)}",
                ]
            ),
            title="Replay",
        )
    )

    console.print("\n[bold]Players[/bold]")
    for player in getattr(replay, "players", []) or []:
        console.print(f"\nPlayer pid={getattr(player, 'pid', None)}")
        pprint(_safe_vars(player))

    tracker_events = list(getattr(replay, "tracker_events", []) or [])
    counts = Counter(event_type_name(e) for e in tracker_events)
    table = Table(title="Tracker event counts")
    table.add_column("event")
    table.add_column("count", justify="right")
    for name, count in counts.most_common():
        table.add_row(name, str(count))
    console.print(table)

    console.print(f"\n[bold]First {max_events} macro-focused events[/bold]")
    shown = 0
    for event in tracker_events:
        name = event_type_name(event)
        if name not in MACRO_FOCUS:
            continue
        console.print(
            f"\n--- {name} frame={getattr(event, 'frame', None)} "
            f"second={getattr(event, 'second', None)} ---"
        )
        pprint(_safe_vars(event))
        unit = getattr(event, "unit", None)
        if unit is not None:
            console.print("unit:")
            pprint(_safe_vars(unit))
        shown += 1
        if shown >= max_events:
            break
