#!/usr/bin/env python3
"""SC2 Human Trace → Adaptive Skill Mining pipeline entrypoint.

Examples:
  # TvP pilot without LLM
  python analysis/skill_mining_v2/run_pipeline.py --matchup TvP --limit 2000 --skip-llm

  # Stages 3-8 only
  python analysis/skill_mining_v2/run_pipeline.py --from-stage 3 --to-stage 8

  # Full run with DeepSeek-V4-flash (nothinking)
  python analysis/skill_mining_v2/run_pipeline.py
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

# Ensure repo root on sys.path
REPO_ROOT = Path(__file__).resolve().parents[2]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from analysis.skill_mining_v2.config import DIRECTIONAL_MATCHUPS, LLM_MODEL_KEY, PipelineConfig
from analysis.skill_mining_v2.stage00_manifest import run_stage00
from analysis.skill_mining_v2.stage01_trajectories import run_stage01
from analysis.skill_mining_v2.stage02_semantics import run_stage02
from analysis.skill_mining_v2.stage03_opening_windows import run_stage03
from analysis.skill_mining_v2.stage04_opening_discovery import run_stage04
from analysis.skill_mining_v2.stage05_state_snapshots import run_stage05
from analysis.skill_mining_v2.stage06_state_discovery import run_stage06
from analysis.skill_mining_v2.stage07_transition_mining import run_stage07
from analysis.skill_mining_v2.stage08_transition_value import run_stage08
from analysis.skill_mining_v2.stage09_graph_builder import run_stage09
from analysis.skill_mining_v2.stage10_annotation_packets import run_stage10
from analysis.skill_mining_v2.stage11_llm_annotation import run_stage11
from analysis.skill_mining_v2.stage12_skill_compile import run_stage12
from analysis.skill_mining_v2.stage13_ablation_generation import run_stage13
from analysis.skill_mining_v2.stage14_validation import run_stage14


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Adaptive Skill Mining v2 pipeline")
    p.add_argument("--from-stage", type=int, default=0)
    p.add_argument("--to-stage", type=int, default=14)
    p.add_argument(
        "--matchup",
        action="append",
        default=None,
        help="Directional matchup (repeatable), e.g. TvP. Default: all 9.",
    )
    p.add_argument("--limit", type=int, default=None, help="Max trajectories per matchup")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--skip-llm", action="store_true", help="Skip LLM calls; use heuristic names")
    p.add_argument("--no-resume", action="store_true", help="Do not reuse existing stage outputs")
    p.add_argument(
        "--fresh",
        action="store_true",
        help="Archive existing V2 outputs, then start a clean stage-0 run",
    )
    p.add_argument("--full-windows", action="store_true", help="Use all opening window candidates")
    p.add_argument("--llm-model-key", default=LLM_MODEL_KEY, help="API_config llm_agents_pool key")
    p.add_argument("--run-id", default=None)
    p.add_argument("--workers", type=int, default=4)
    return p.parse_args()


def _run_signature(cfg: PipelineConfig) -> dict:
    return {
        "matchups": sorted(cfg.matchups),
        "limit": cfg.limit,
        "random_seed": cfg.seed,
        "opening_window_candidates": list(cfg.opening_windows),
        "skip_llm": cfg.skip_llm,
        "llm_model_key": cfg.llm_model_key,
    }


def _prepare_run(cfg: PipelineConfig, *, fresh: bool) -> None:
    manifest_path = cfg.stage_dir(0, "00_manifest") / "run_manifest.json"
    if fresh:
        if cfg.from_stage != 0:
            raise ValueError("--fresh requires --from-stage 0")
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        archive_root = cfg.repo_root / "archive" / "v2_runs" / stamp
        moved = False
        for source, name in (
            (cfg.output_root, "outputs_skill_v2"),
            (cfg.skill_root, "SKILL_MINING_V2"),
        ):
            source.mkdir(parents=True, exist_ok=True)
            for child in list(source.iterdir()):
                if child.name in {"README.md", ".gitkeep"}:
                    continue
                destination = archive_root / name / child.name
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(child), str(destination))
                moved = True
        if moved:
            print(f"[pipeline] archived previous V2 run -> {archive_root}", flush=True)
        cfg.resume = False
        return

    if not manifest_path.exists():
        if cfg.from_stage > 0:
            raise RuntimeError(
                f"Cannot start at stage {cfg.from_stage}: missing {manifest_path}. "
                "Start from stage 0."
            )
        return

    previous = json.loads(manifest_path.read_text(encoding="utf-8"))
    cfg.run_id = previous.get("run_id")
    expected = _run_signature(cfg)
    actual = {
        "matchups": sorted(previous.get("matchups") or []),
        "limit": previous.get("limit"),
        "random_seed": previous.get("random_seed"),
        "opening_window_candidates": previous.get("opening_window_candidates"),
        "skip_llm": previous.get("skip_llm"),
        "llm_model_key": previous.get("llm_model_key"),
    }
    if cfg.resume and expected != actual:
        raise RuntimeError(
            "Existing V2 outputs were produced with a different run configuration. "
            f"existing={actual}, requested={expected}. Use --fresh to archive them "
            "and start clean; do not mix pilot and full-run artifacts."
        )


def main() -> int:
    args = parse_args()
    matchups = args.matchup or list(DIRECTIONAL_MATCHUPS)
    cfg = PipelineConfig(
        repo_root=REPO_ROOT,
        seed=args.seed,
        matchups=matchups,
        limit=args.limit,
        from_stage=args.from_stage,
        to_stage=args.to_stage,
        skip_llm=args.skip_llm,
        resume=not args.no_resume,
        full_windows=args.full_windows,
        workers=args.workers,
        llm_model_key=args.llm_model_key,
        run_id=args.run_id,
    )
    cfg.output_root.mkdir(parents=True, exist_ok=True)
    cfg.skill_root.mkdir(parents=True, exist_ok=True)
    _prepare_run(cfg, fresh=args.fresh)

    print(
        f"[pipeline] matchups={list(cfg.matchups)} limit={cfg.limit} "
        f"stages={cfg.from_stage}-{cfg.to_stage} skip_llm={cfg.skip_llm} "
        f"llm={cfg.llm_model_key}",
        flush=True,
    )

    traj = None
    snaps = None
    states = None
    transitions = None
    edges = None

    t0 = time.time()
    for stage in range(cfg.from_stage, cfg.to_stage + 1):
        st = time.time()
        print(f"\n===== STAGE {stage:02d} =====", flush=True)
        if stage == 0:
            run_stage00(cfg)
        elif stage == 1:
            traj = run_stage01(cfg)
        elif stage == 2:
            run_stage02(cfg)
        elif stage == 3:
            run_stage03(cfg, traj=traj)
        elif stage == 4:
            run_stage04(cfg, traj=traj)
        elif stage == 5:
            snaps = run_stage05(cfg, traj=traj)
        elif stage == 6:
            out = run_stage06(cfg, snapshots=snaps)
            states = out.get("assignments")
        elif stage == 7:
            out = run_stage07(cfg, states=states)
            transitions = out.get("transitions")
        elif stage == 8:
            out = run_stage08(cfg, transitions=transitions)
            edges = out.get("edges")
        elif stage == 9:
            run_stage09(cfg, edges=edges)
        elif stage == 10:
            run_stage10(cfg)
        elif stage == 11:
            run_stage11(cfg)
        elif stage == 12:
            run_stage12(cfg)
        elif stage == 13:
            run_stage13(cfg)
        elif stage == 14:
            run_stage14(cfg)
        else:
            raise ValueError(f"unknown stage {stage}")
        print(f"[pipeline] stage {stage:02d} done in {time.time() - st:.1f}s", flush=True)

    print(f"\n[pipeline] complete in {time.time() - t0:.1f}s run_id={cfg.run_id}", flush=True)
    print(f"[pipeline] outputs: {cfg.output_root}", flush=True)
    print(f"[pipeline] skills:  {cfg.skill_root}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
