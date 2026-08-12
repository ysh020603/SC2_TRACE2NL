from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from pathlib import Path

METHODS = (
    "full_signed_graph",
    "ablation_single_trace",
    "ablation_static_population",
    "ablation_flat_adaptive",
    "ablation_positive_only",
    "ablation_frequency_only",
)
LLM_MODEL_KEY = "DeepSeek-V4-flash"
FORBIDDEN_LLM_MODEL_KEYS = frozenset({"DeepSeek-V4-flash_think"})
RACE = {"P": "Protoss", "T": "Terran", "Z": "Zerg"}


@dataclass
class PipelineConfig:
    repo_root: Path = field(default_factory=lambda: Path(__file__).resolve().parents[2])
    input_root: Path | None = None
    output_root: Path | None = None
    skill_root: Path | None = None
    knowledge_root: Path | None = None
    failure_diagnostics: Path | None = None
    methods: tuple[str, ...] = METHODS
    openings: tuple[str, ...] = ()
    from_stage: int = 0
    to_stage: int = 6
    resume: bool = True
    skip_llm: bool = False
    max_nodes: int = 12
    llm_workers: int = 6
    llm_model_key: str = LLM_MODEL_KEY

    def __post_init__(self) -> None:
        self.repo_root = Path(self.repo_root).resolve()
        self.input_root = Path(self.input_root or self.repo_root / "analysis" / "outputs_skill_v2")
        self.output_root = Path(self.output_root or self.repo_root / "analysis" / "outputs_readable_skill_v1")
        self.skill_root = Path(self.skill_root or self.repo_root / "SKILL_MINING_V2_READABLE")
        self.knowledge_root = Path(self.knowledge_root or self.repo_root / "data_sc2_260701")
        self.failure_diagnostics = Path(self.failure_diagnostics).resolve() if self.failure_diagnostics else None
        self.methods = tuple(self.methods)
        self.openings = tuple(self.openings)
        unknown = set(self.methods) - set(METHODS)
        if unknown:
            raise ValueError(f"unknown methods: {sorted(unknown)}")
        if self.llm_model_key != LLM_MODEL_KEY or self.llm_model_key in FORBIDDEN_LLM_MODEL_KEYS:
            raise ValueError("Readable Skill language annotation is pinned to DeepSeek-V4-flash (non-reasoning)")

    def stage_dir(self, stage: int) -> Path:
        names = {0: "00_manifest", 1: "01_method_ir", 2: "02_observation_projection", 3: "03_semantic_annotation", 4: "04_compiled", 5: "05_validation", 6: "06_catalog"}
        return self.output_root / names[stage]


def parse_args(argv: list[str] | None = None) -> PipelineConfig:
    p = argparse.ArgumentParser(description="Compile V2 evidence into readable hierarchical skills")
    p.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    p.add_argument("--input-root", type=Path)
    p.add_argument("--output-root", type=Path)
    p.add_argument("--skill-root", type=Path)
    p.add_argument("--knowledge-root", type=Path)
    p.add_argument("--failure-diagnostics", type=Path)
    p.add_argument("--methods", default=",".join(METHODS))
    p.add_argument("--openings", default="", help="comma-separated opening ids")
    p.add_argument("--from-stage", type=int, default=0)
    p.add_argument("--to-stage", type=int, default=6)
    p.add_argument("--no-resume", dest="resume", action="store_false")
    p.add_argument("--skip-llm", action="store_true", help="testing only; compiled provenance marks deterministic fallback")
    p.add_argument("--max-nodes", type=int, default=12)
    p.add_argument("--llm-workers", type=int, default=6)
    p.add_argument("--llm-model-key", default=LLM_MODEL_KEY, choices=[LLM_MODEL_KEY])
    a = p.parse_args(argv)
    return PipelineConfig(
        repo_root=a.repo_root, input_root=a.input_root, output_root=a.output_root, skill_root=a.skill_root,
        knowledge_root=a.knowledge_root,
        failure_diagnostics=a.failure_diagnostics,
        methods=tuple(x for x in a.methods.split(",") if x), openings=tuple(x for x in a.openings.split(",") if x),
        from_stage=a.from_stage, to_stage=a.to_stage, resume=a.resume, skip_llm=a.skip_llm,
        max_nodes=a.max_nodes, llm_workers=a.llm_workers, llm_model_key=a.llm_model_key,
    )
