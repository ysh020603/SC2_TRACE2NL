from __future__ import annotations

from .config import parse_args
from . import stage00_manifest, stage01_method_evidence_ir, stage02_observation_projection
from . import stage03_llm_semantic_annotation, stage04_hierarchy_compile, stage05_validation, stage06_catalog

STAGES = {
    0: stage00_manifest.run, 1: stage01_method_evidence_ir.run, 2: stage02_observation_projection.run,
    3: stage03_llm_semantic_annotation.run, 4: stage04_hierarchy_compile.run,
    5: stage05_validation.run, 6: stage06_catalog.run,
}


def main(argv: list[str] | None = None) -> int:
    cfg = parse_args(argv)
    cfg.output_root.mkdir(parents=True, exist_ok=True)
    cfg.skill_root.mkdir(parents=True, exist_ok=True)
    for stage in range(cfg.from_stage, cfg.to_stage + 1):
        print(f"[readable-skill-v1] stage {stage:02d}", flush=True)
        STAGES[stage](cfg)
    print(f"[readable-skill-v1] complete: {cfg.skill_root}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
