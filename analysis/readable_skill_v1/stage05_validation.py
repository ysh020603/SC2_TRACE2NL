from __future__ import annotations

from .common.io import read_json, write_json
from .common.validation import validate_skill
from .config import PipelineConfig


def run(cfg: PipelineConfig) -> dict:
    compiled = read_json(cfg.stage_dir(4) / "index.json")
    reports, failures = {}, []
    entity_path = cfg.input_root / "02_semantics" / "entity_index.json"
    for method, openings in compiled.items():
        for opening_id, item in openings.items():
            skill_dir = cfg.skill_root / item["path"]
            errors = validate_skill(skill_dir, method, entity_path)
            report = {"method": method, "opening_id": opening_id, "valid": not errors, "errors": errors}
            reports.setdefault(method, {})[opening_id] = report
            write_json(skill_dir / "provenance" / "validation_report.json", report)
            if errors:
                failures.append(f"{method}/{opening_id}: {errors}")
    summary = {"valid": not failures, "skills": sum(len(v) for v in reports.values()), "failures": failures, "reports": reports}
    write_json(cfg.stage_dir(5) / "validation_summary.json", summary)
    if failures:
        raise RuntimeError("Readable Skill validation failed:\n" + "\n".join(failures[:20]))
    return summary
