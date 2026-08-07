#!/usr/bin/env python3
"""Run plan.md Phase 2–8 sequentially on data/action_json.

Phase 1 audit is assumed already available under analysis/outputs/00_audit
(or re-run with --with-phase1).
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent  # analysis/
REPO = ROOT.parent  # repo root
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from analysis.pipeline.io_utils import PRIMARY_HORIZON, ensure_dir  # noqa: E402
from analysis.pipeline.phase02_openings import run_phase02  # noqa: E402
from analysis.pipeline.phase03_features import run_phase03  # noqa: E402
from analysis.pipeline.phase04_clusters import run_phase04  # noqa: E402
from analysis.pipeline.phase05_catalog import run_phase05  # noqa: E402
from analysis.pipeline.phase06_matchups import run_phase06  # noqa: E402
from analysis.pipeline.phase07_robustness import run_phase07  # noqa: E402
from analysis.pipeline.phase08_report import run_phase08  # noqa: E402


def _log(msg: str) -> None:
    print(msg, flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--action-json-root",
        type=Path,
        default=REPO / "data" / "action_json",
    )
    parser.add_argument(
        "--out-root",
        type=Path,
        default=ROOT / "outputs",
    )
    parser.add_argument(
        "--with-phase1",
        action="store_true",
        help="Re-run Phase 1 audit before Phase 2.",
    )
    parser.add_argument(
        "--start-phase",
        type=int,
        default=2,
        help="Start from this phase number (2–8).",
    )
    args = parser.parse_args()

    out = ensure_dir(args.out_root)
    summaries: dict[str, object] = {}
    t0 = time.time()

    if args.with_phase1 or args.start_phase <= 1:
        _log("=== Phase 1: data audit ===")
        from analysis.phase1_audit.run_audit import main as audit_main

        # run_audit uses argparse on sys.argv; call via subprocess-like argv override
        old = sys.argv
        try:
            sys.argv = [
                "run_audit.py",
                "--action-json-root",
                str(args.action_json_root),
                "--out-root",
                str(out),
            ]
            audit_main()
        finally:
            sys.argv = old
        summaries["phase1"] = "ok"

    if args.start_phase <= 2:
        _log("=== Phase 2: openings ===")
        summaries["phase2"] = run_phase02(args.action_json_root, out / "02_openings")
        _log(json.dumps(summaries["phase2"], ensure_ascii=False))

    if args.start_phase <= 3:
        _log("=== Phase 3: features ===")
        summaries["phase3"] = run_phase03(
            out / "02_openings" / "opening_sequences.jsonl",
            out / "03_features",
            args.action_json_root,
        )
        _log(json.dumps(summaries["phase3"], ensure_ascii=False))

    if args.start_phase <= 4:
        _log("=== Phase 4: clustering ===")
        summaries["phase4"] = run_phase04(
            out / "03_features" / f"features_{PRIMARY_HORIZON}.parquet",
            out / "04_clusters",
        )
        _log(json.dumps(summaries["phase4"], ensure_ascii=False))

    if args.start_phase <= 5:
        _log("=== Phase 5: catalog ===")
        summaries["phase5"] = run_phase05(
            out / "03_features" / f"features_{PRIMARY_HORIZON}.parquet",
            out / "04_clusters",
            out / "05_catalog",
        )
        _log(json.dumps(summaries["phase5"], ensure_ascii=False))

    if args.start_phase <= 6:
        _log("=== Phase 6: matchups ===")
        summaries["phase6"] = run_phase06(out / "04_clusters", out / "06_matchups")
        _log(json.dumps(summaries["phase6"], ensure_ascii=False))

    if args.start_phase <= 7:
        _log("=== Phase 7: robustness ===")
        summaries["phase7"] = run_phase07(
            out / "03_features",
            out / "04_clusters",
            out / "06_matchups",
            out / "07_robustness",
        )
        _log(json.dumps(summaries["phase7"], ensure_ascii=False))

    if args.start_phase <= 8:
        _log("=== Phase 8: final report ===")
        summaries["phase8"] = run_phase08(out)
        _log(json.dumps(summaries["phase8"], ensure_ascii=False))

    elapsed = time.time() - t0
    (out / "pipeline_run_summary.json").write_text(
        json.dumps({"elapsed_seconds": elapsed, "summaries": summaries}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    _log(f"DONE in {elapsed:.1f}s -> {out}")


if __name__ == "__main__":
    main()
