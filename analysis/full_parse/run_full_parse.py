#!/usr/bin/env python3
"""Resume-capable full-corpus macro-action parse into data/action_json.

Skips replays whose absolute source_file is already present in existing JSON.
Updates analysis/full_parse/state/status.json for the watchdog.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import traceback
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[2]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

MATCHUPS = ("PvP", "PvT", "PvZ", "TvT", "TvZ", "ZvZ")
DEFAULT_DB = REPO / "data_sc2_260701" / "data_base_sc2_260701.json"
DEFAULT_CONFIG = REPO / "configs"


def _write_status(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


def _load_done_sources(json_dir: Path) -> set[str]:
    done: set[str] = set()
    if not json_dir.is_dir():
        return done
    for p in json_dir.glob("*.json"):
        if p.name in {"summary.json", "parse_errors.jsonl"} or p.name.startswith("summary"):
            continue
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        src = data.get("source_file")
        if src:
            try:
                done.add(str(Path(src).resolve()))
            except Exception:
                done.add(str(src))
    return done


def _list_replays(directory: Path) -> list[Path]:
    files = sorted({*directory.glob("*.SC2Replay"), *directory.glob("*.sc2replay")})
    return [p for p in files if p.is_file()]


def _parse_one(args: tuple[str, str, str, str]) -> dict[str, Any]:
    replay_path, config_dir, action_database, json_out = args
    try:
        from sc2_replay_miner.action_exporters import write_action_match_json
        from sc2_replay_miner.action_parser import MacroActionParser

        parser = MacroActionParser(
            config_dir=Path(config_dir),
            action_database=Path(action_database),
        )
        parsed, err = parser.parse_safe(Path(replay_path))
        if err is not None:
            return {
                "ok": False,
                "source_file": replay_path,
                "error": err.model_dump(),
            }
        assert parsed is not None
        out = Path(json_out) / f"{parsed.replay.replay_id}.json"
        write_action_match_json(parsed, out)
        return {
            "ok": True,
            "source_file": replay_path,
            "replay_id": parsed.replay.replay_id,
            "macro_actions": len(parsed.macro_actions),
            "mapped": sum(1 for a in parsed.macro_actions if a.standard_action_name),
            "unmapped": sum(1 for a in parsed.macro_actions if a.standard_action_name is None),
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "ok": False,
            "source_file": replay_path,
            "error": {
                "exception_type": type(exc).__name__,
                "message": str(exc),
                "traceback": traceback.format_exc(limit=5),
            },
        }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--raw-root", type=Path, default=REPO / "raw_data" / "by_matchup")
    ap.add_argument("--json-root", type=Path, default=REPO / "data" / "action_json")
    ap.add_argument("--state-dir", type=Path, default=REPO / "analysis" / "full_parse" / "state")
    ap.add_argument("--log-dir", type=Path, default=REPO / "analysis" / "full_parse" / "logs")
    ap.add_argument("--workers", type=int, default=48)
    ap.add_argument("--batch-size", type=int, default=2000)
    ap.add_argument(
        "--matchups",
        nargs="*",
        default=list(MATCHUPS),
        help="Subset of matchups to parse",
    )
    args = ap.parse_args()

    args.state_dir.mkdir(parents=True, exist_ok=True)
    args.log_dir.mkdir(parents=True, exist_ok=True)
    status_path = args.state_dir / "status.json"
    pid_path = args.state_dir / "parse.pid"
    pid_path.write_text(str(os.getpid()), encoding="utf-8")

    started = time.time()
    grand = {
        "phase": "running",
        "pid": os.getpid(),
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "workers": args.workers,
        "batch_size": args.batch_size,
        "matchups": {},
        "totals": {
            "raw": 0,
            "already_done": 0,
            "todo": 0,
            "success": 0,
            "failed": 0,
            "skipped_existing": 0,
        },
        "last_update": None,
        "error": None,
        "finished_at": None,
    }

    try:
        for mu in args.matchups:
            raw_dir = args.raw_root / mu
            json_dir = args.json_root / mu
            json_dir.mkdir(parents=True, exist_ok=True)
            err_path = json_dir / "parse_errors.jsonl"
            log_path = args.log_dir / f"{mu}.log"

            files = _list_replays(raw_dir)
            done = _load_done_sources(json_dir)
            pending = [p for p in files if str(p.resolve()) not in done]

            mu_state = {
                "raw": len(files),
                "already_done": len(files) - len(pending),
                "todo": len(pending),
                "success": 0,
                "failed": 0,
                "status": "running" if pending else "done",
            }
            grand["matchups"][mu] = mu_state
            grand["totals"]["raw"] += len(files)
            grand["totals"]["already_done"] += mu_state["already_done"]
            grand["totals"]["todo"] += len(pending)
            grand["totals"]["skipped_existing"] += mu_state["already_done"]
            grand["last_update"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
            _write_status(status_path, grand)

            with log_path.open("a", encoding="utf-8") as log:
                log.write(
                    f"\n=== start {time.strftime('%Y-%m-%d %H:%M:%S')} "
                    f"raw={len(files)} pending={len(pending)} workers={args.workers}\n"
                )
                if not pending:
                    log.write("nothing pending\n")
                    mu_state["status"] = "done"
                    _write_status(status_path, grand)
                    continue

                for batch_start in range(0, len(pending), args.batch_size):
                    batch = pending[batch_start : batch_start + args.batch_size]
                    tasks = [
                        (
                            str(p),
                            str(DEFAULT_CONFIG),
                            str(DEFAULT_DB),
                            str(json_dir),
                        )
                        for p in batch
                    ]
                    with ProcessPoolExecutor(max_workers=args.workers) as pool:
                        futures = [pool.submit(_parse_one, t) for t in tasks]
                        for fut in as_completed(futures):
                            result = fut.result()
                            if result.get("ok"):
                                mu_state["success"] += 1
                                grand["totals"]["success"] += 1
                            else:
                                mu_state["failed"] += 1
                                grand["totals"]["failed"] += 1
                                with err_path.open("a", encoding="utf-8") as ef:
                                    ef.write(json.dumps(result, ensure_ascii=False) + "\n")
                                log.write(
                                    f"FAIL {result.get('source_file')}: "
                                    f"{(result.get('error') or {}).get('exception_type')} "
                                    f"{(result.get('error') or {}).get('message')}\n"
                                )

                    done_in_mu = mu_state["success"] + mu_state["failed"]
                    rate = done_in_mu / max(1, mu_state["todo"])
                    elapsed = time.time() - started
                    eta = None
                    finished_all = grand["totals"]["success"] + grand["totals"]["failed"]
                    if finished_all > 0 and grand["totals"]["todo"] > finished_all:
                        eta = elapsed / finished_all * (grand["totals"]["todo"] - finished_all)
                    grand["last_update"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
                    grand["elapsed_seconds"] = round(elapsed, 1)
                    grand["eta_seconds"] = None if eta is None else round(eta, 1)
                    _write_status(status_path, grand)
                    msg = (
                        f"{mu} batch {batch_start // args.batch_size + 1}: "
                        f"success={mu_state['success']} failed={mu_state['failed']} "
                        f"progress={rate:.1%} elapsed={elapsed:.0f}s eta={eta}\n"
                    )
                    log.write(msg)
                    print(msg, flush=True)

                mu_state["status"] = "done"
                # summary for this matchup
                summary = {
                    "input_directory": str(raw_dir.resolve()),
                    "total_raw": len(files),
                    "skipped_existing": mu_state["already_done"],
                    "attempted": mu_state["todo"],
                    "success": mu_state["success"],
                    "failed": mu_state["failed"],
                    "success_rate": (
                        mu_state["success"] / mu_state["todo"] if mu_state["todo"] else 1.0
                    ),
                    "workers": args.workers,
                }
                (json_dir / "full_parse_summary.json").write_text(
                    json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
                )
                _write_status(status_path, grand)

        grand["phase"] = "completed"
        grand["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        grand["elapsed_seconds"] = round(time.time() - started, 1)
        grand["eta_seconds"] = 0
        _write_status(status_path, grand)
        print("FULL_PARSE_COMPLETED", json.dumps(grand["totals"]), flush=True)
    except Exception as exc:  # noqa: BLE001
        grand["phase"] = "failed"
        grand["error"] = f"{type(exc).__name__}: {exc}"
        grand["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        _write_status(status_path, grand)
        print("FULL_PARSE_FAILED", grand["error"], flush=True)
        raise
    finally:
        if pid_path.exists():
            pid_path.unlink(missing_ok=True)


if __name__ == "__main__":
    main()
