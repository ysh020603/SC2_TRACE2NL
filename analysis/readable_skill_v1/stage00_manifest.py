from __future__ import annotations

from . import PIPELINE_VERSION
from .common.io import write_json
import subprocess

from .common.provenance import git_commit, now, sha256
from .config import LLM_MODEL_KEY, PipelineConfig


def run(cfg: PipelineConfig) -> dict:
    inputs = [
        cfg.input_root / "04_openings" / "opening_catalog.json",
        cfg.input_root / "06_states" / "state_catalog.json",
        cfg.input_root / "07_transitions" / "response_clusters.json",
        cfg.input_root / "09_graphs" / "graph_index.json",
    ]
    manifest = {
        "pipeline_version": PIPELINE_VERSION,
        "created_at": now(),
        "repo_commit": git_commit(cfg.repo_root),
        "input_root": str(cfg.input_root),
        "output_root": str(cfg.output_root),
        "skill_root": str(cfg.skill_root),
        "methods": list(cfg.methods),
        "openings": list(cfg.openings),
        "annotation_model_key": LLM_MODEL_KEY,
        "annotation_reasoning": False,
        "inputs": {str(path.relative_to(cfg.repo_root)): sha256(path) for path in inputs},
    }
    write_json(cfg.stage_dir(0) / "run_manifest.json", manifest)
    def branch(path):
        try:
            return subprocess.check_output(["git", "-C", str(path), "branch", "--show-current"], text=True).strip()
        except Exception:
            return "unknown"
    baseline = cfg.repo_root / "SC2-Agent-knowlegde"
    new_agent = cfg.repo_root / "SC2-Agent-human-skill"
    write_json(cfg.repo_root / "READABLE_SKILL_BASELINE_MANIFEST.json", {
        "baseline_repo": str(baseline), "baseline_branch": branch(baseline), "baseline_commit": git_commit(baseline),
        "skill_mining_repo_commit": git_commit(cfg.repo_root), "new_agent_repo": str(new_agent),
        "new_agent_branch": branch(new_agent), "created_at": now(), "readable_pipeline_version": PIPELINE_VERSION,
    })
    return manifest
