from __future__ import annotations

from collections import Counter

from .common.io import read_json, write_json
from .config import PipelineConfig


def run(cfg: PipelineConfig) -> dict:
    compiled = read_json(cfg.stage_dir(4) / "index.json")
    validation = read_json(cfg.stage_dir(5) / "validation_summary.json")
    annotation_index = read_json(cfg.stage_dir(3) / "index.json")
    methods = {}
    for method, openings in compiled.items():
        sources = Counter()
        reasoning_present = api_errors = 0
        for opening_id, rel in annotation_index[method].items():
            semantic = read_json(cfg.output_root / rel)
            sources[semantic.get("annotation_source", "unknown")] += 1
            reasoning_present += bool((semantic.get("llm_metadata") or {}).get("reasoning_present"))
            api_errors += bool((semantic.get("llm_metadata") or {}).get("error"))
        methods[method] = {
            "count": len(openings), "nodes": sum(item.get("nodes", 0) for item in openings.values()),
            "annotation_sources": dict(sources), "reasoning_present": reasoning_present,
            "api_errors": api_errors, "validation_failures": sum(not report["valid"] for report in validation["reports"][method].values()),
            "openings": openings,
        }
    catalog = {
        "schema_version": 1, "skill_root": str(cfg.skill_root), "validation_passed": validation["valid"],
        "methods": methods,
        "total_skills": sum(len(openings) for openings in compiled.values()),
    }
    write_json(cfg.stage_dir(6) / "catalog.json", catalog)
    write_json(cfg.skill_root / "catalog.json", catalog)
    return catalog
