"""Phase 2: opening window extraction (plan.md §4 / §21)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from analysis.pipeline.io_utils import (
    HORIZONS,
    ensure_dir,
    iter_action_json,
    player_views,
)
from analysis.pipeline.taxonomy import build_key_sequence, macro_category, result_name


def _events_to_horizon(events: list[dict[str, Any]], horizon: int) -> list[dict[str, Any]]:
    out = []
    for ev in events:
        sec = ev.get("second")
        if not isinstance(sec, (int, float)):
            continue
        if float(sec) <= horizon:
            out.append(ev)
    return out


def run_phase02(action_root: Path, out_dir: Path) -> dict[str, Any]:
    ensure_dir(out_dir)
    event_rows: list[dict[str, Any]] = []
    seq_path = out_dir / "opening_sequences.jsonl"

    n_players = 0
    with seq_path.open("w", encoding="utf-8") as fout:
        for matchup_dir, _path, data in iter_action_json(action_root):
            for view in player_views(data, matchup_dir):
                n_players += 1
                bo = view["build_order"]
                max_sec = 0.0
                for ev in bo:
                    sec = ev.get("second")
                    if isinstance(sec, (int, float)):
                        max_sec = max(max_sec, float(sec))

                duration = view.get("duration_real_seconds")
                try:
                    duration_f = float(duration) if duration is not None else None
                except (TypeError, ValueError):
                    duration_f = None

                # game-time observation proxy
                observed_game = max_sec
                if observed_game <= 0 and duration_f and duration_f > 0:
                    # fallback: no BO; treat as observed only to 0
                    observed_game = 0.0

                seq_record: dict[str, Any] = {
                    "replay_id": view["replay_id"],
                    "player_id": view["player_id"],
                    "race": view["race"],
                    "opponent_race": view["opponent_race"],
                    "matchup_dir": matchup_dir,
                    "result": view["result"],
                    "max_build_order_second": max_sec if max_sec > 0 else None,
                    "duration_real_seconds": duration_f,
                    "horizons": {},
                }

                for h in HORIZONS:
                    observed = observed_game >= h
                    early_terminated = not observed
                    clipped = _events_to_horizon(bo, h)
                    key_seq = build_key_sequence(clipped)
                    cats = {}
                    for ev in clipped:
                        cat = macro_category(ev)
                        cats[cat] = cats.get(cat, 0) + 1

                    seq_record["horizons"][str(h)] = {
                        "opening_observed_to": observed,
                        "early_terminated": early_terminated,
                        "n_events": len(clipped),
                        "key_sequence": [x["token"] for x in key_seq],
                        "key_sequence_timed": key_seq,
                        "category_counts": cats,
                    }

                    for i, ev in enumerate(clipped):
                        event_rows.append(
                            {
                                "replay_id": view["replay_id"],
                                "player_id": view["player_id"],
                                "race": view["race"],
                                "opponent_race": view["opponent_race"],
                                "matchup_dir": matchup_dir,
                                "horizon": h,
                                "opening_observed_to": observed,
                                "early_terminated": early_terminated,
                                "event_index": i,
                                "second": ev.get("second"),
                                "frame": ev.get("frame"),
                                "event": ev.get("event"),
                                "name": result_name(ev),
                                "ability": ev.get("ability"),
                                "standard_action_name": ev.get("standard_action_name"),
                                "standard_result_name": ev.get("standard_result_name"),
                                "standard_mapping_confidence": ev.get(
                                    "standard_mapping_confidence"
                                ),
                                "macro_category": macro_category(ev),
                                "occurrence_index": ev.get("occurrence_index"),
                            }
                        )

                fout.write(json.dumps(seq_record, ensure_ascii=False) + "\n")

    events_df = pd.DataFrame(event_rows)
    events_df.to_parquet(out_dir / "opening_events.parquet", index=False)

    summary = {
        "player_rows": n_players,
        "opening_event_rows": int(len(events_df)),
        "horizons": list(HORIZONS),
        "outputs": [
            str(out_dir / "opening_events.parquet"),
            str(out_dir / "opening_sequences.jsonl"),
        ],
    }
    (out_dir / "phase02_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return summary
