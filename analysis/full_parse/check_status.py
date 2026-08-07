#!/usr/bin/env python3
"""Print full-parse watchdog snapshot."""

from __future__ import annotations

import json
import os
from pathlib import Path

STATE = Path(__file__).resolve().parent / "state"
STATUS = STATE / "status.json"
PID = STATE / "parse.pid"
REPO = Path(__file__).resolve().parents[2]
MATCHUPS = ("PvP", "PvT", "PvZ", "TvT", "TvZ", "ZvZ")


def pid_alive(pid: int) -> bool:
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def count_json(d: Path) -> int:
    if not d.is_dir():
        return 0
    return sum(
        1
        for p in d.glob("*.json")
        if p.name not in {"summary.json", "full_parse_summary.json"}
        and not p.name.startswith("summary")
    )


def main() -> None:
    status = {}
    if STATUS.exists():
        status = json.loads(STATUS.read_text(encoding="utf-8"))
    alive = False
    pid = None
    if PID.exists():
        try:
            pid = int(PID.read_text().strip())
            alive = pid_alive(pid)
        except Exception:
            pid = None
    counts = {
        mu: count_json(REPO / "data" / "action_json" / mu) for mu in MATCHUPS
    }
    snap = {
        "status_file": status,
        "parse_pid": pid,
        "parse_alive": alive,
        "action_json_counts": counts,
        "action_json_total": sum(counts.values()),
    }
    print(json.dumps(snap, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
