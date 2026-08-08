"""Stage 00 — experiment manifest."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from analysis.skill_mining_v2.common.io import (
    dir_content_hash,
    ensure_dir,
    file_sha256,
    git_commit,
    write_json,
)
from analysis.skill_mining_v2.config import (
    SNAPSHOT_TIMES,
    TAXONOMY_VERSION,
    PipelineConfig,
)


def run_stage00(cfg: PipelineConfig) -> dict[str, Any]:
    out_dir = ensure_dir(cfg.stage_dir(0, "00_manifest"))
    run_id = cfg.run_id or datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "_" + uuid4().hex[:8]
    cfg.run_id = run_id

    sc2_hash = ""
    if cfg.sc2_knowledge_path and cfg.sc2_knowledge_path.exists():
        sc2_hash = file_sha256(cfg.sc2_knowledge_path)[:32]
    dataset_hash = ""
    if cfg.action_root and cfg.action_root.exists():
        dataset_hash = dir_content_hash(cfg.action_root)

    manifest = {
        "run_id": run_id,
        "git_commit": git_commit(cfg.repo_root),
        "dataset_version": "action_json",
        "dataset_hash": dataset_hash,
        "sc2_knowledge_hash": sc2_hash,
        "taxonomy_version": TAXONOMY_VERSION,
        "random_seed": cfg.seed,
        "opening_window_candidates": list(cfg.opening_windows),
        "snapshot_times": list(SNAPSHOT_TIMES),
        "matchups": list(cfg.matchups),
        "limit": cfg.limit,
        "skip_llm": cfg.skip_llm,
        "llm_model_key": cfg.llm_model_key,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    write_json(out_dir / "run_manifest.json", manifest)
    print(f"[stage00] run_id={run_id} -> {out_dir / 'run_manifest.json'}", flush=True)
    return manifest
