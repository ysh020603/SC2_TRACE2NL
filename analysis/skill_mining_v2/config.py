"""Global configuration for skill_mining_v2."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
from pathlib import Path
from typing import Sequence

# --- Repository paths (resolved from this file) ---
_CONFIG_DIR = Path(__file__).resolve().parent
REPO_ROOT = _CONFIG_DIR.parents[1]
ACTION_JSON_ROOT = REPO_ROOT / "data" / "action_json"
SC2_KB_PATH = REPO_ROOT / "data_sc2_260701" / "data_base_sc2_260701.json"
SC2_RELATIONS_PATH = REPO_ROOT / "data_sc2_260701" / "relations" / "entity_expanded_relations.json"
OUTPUT_ROOT = REPO_ROOT / "analysis" / "outputs_skill_v2"
SKILL_ROOT = REPO_ROOT / "SKILL_MINING_V2"

# --- Matchups ---
DIRECTIONAL_MATCHUPS: tuple[str, ...] = (
    "PvP",
    "PvT",
    "PvZ",
    "TvP",
    "TvT",
    "TvZ",
    "ZvP",
    "ZvT",
    "ZvZ",
)

SOURCE_MATCHUP_DIRS: tuple[str, ...] = ("PvP", "PvT", "PvZ", "TvT", "TvZ", "ZvZ")

# How on-disk directories map to directional matchups (reverse views included)
MATCHUP_DIR_TO_FILE_MATCHUPS: dict[str, tuple[str, ...]] = {
    "PvP": ("PvP",),
    "PvT": ("PvT", "TvP"),
    "PvZ": ("PvZ", "ZvP"),
    "TvT": ("TvT",),
    "TvZ": ("TvZ", "ZvZ"),
    "ZvZ": ("ZvZ",),
}

RACE_CODE = {"P": "Protoss", "T": "Terran", "Z": "Zerg"}
RACE_TO_CODE = {v: k for k, v in RACE_CODE.items()}

# --- Timing ---
OPENING_WINDOW_CANDIDATES: list[int] = [180, 210, 240, 270, 300, 330, 360]
OPENING_WINDOW_FAST: tuple[int, ...] = (180, 210, 240, 300, 360)
SNAPSHOT_TIMES: list[int] = [180, 240, 300, 360, 420, 480, 540, 600, 720]
RESPONSE_DELTA = 60

# --- Runtime defaults ---
RANDOM_SEED = 42
DEFAULT_LLM_MODEL_KEY = "DeepSeek-V4-flash"
TAXONOMY_VERSION = "skill_mining_v2_1.0"
FIGURE_DPI = 300
MACRO_EVENTS = frozenset({"production", "construction", "tech_morph", "upgrade_research"})

# --- Support / admission thresholds ---
OPENING_SUPPORT_DEFAULT = 300
OPENING_PREVALENCE_MIN = 0.01
OPENING_BOOTSTRAP_RETENTION_MIN = 0.70
LARGEST_CLUSTER_SPLIT_THRESHOLD = 0.60
STATE_CLUSTER_K_RANGE = (3, 10)
RESPONSE_CLUSTER_K_RANGE = (3, 12)

# --- Transition value thresholds ---
PREFERRED_LIFT = 0.03
HARMFUL_LIFT = -0.03
DEFAULT_LIFT_ABS = 0.015
PREFERRED_SUPPORT_DEFAULT = 300
PREFERRED_ESS_DEFAULT = 200

# --- Graph pruning ---
MAX_PREFERRED_EDGES = 2
MAX_DEFAULT_EDGES = 1
MAX_HARMFUL_EDGES = 2

# --- OpeningScore weights (α, β, γ, δ, η) ---
OPENING_SCORE_ALPHA = 1.0  # separability
OPENING_SCORE_BETA = 1.0  # stability
OPENING_SCORE_GAMMA = 0.8  # semantic distinctiveness
OPENING_SCORE_DELTA = 1.2  # largest-cluster penalty
OPENING_SCORE_ETA = 1.0  # opponent leakage

# Back-compat aliases
WINDOW_ALPHA = OPENING_SCORE_ALPHA
WINDOW_BETA = OPENING_SCORE_BETA
WINDOW_GAMMA = OPENING_SCORE_GAMMA
WINDOW_DELTA = OPENING_SCORE_DELTA
WINDOW_ETA = OPENING_SCORE_ETA
DEFAULT_SEED = RANDOM_SEED
LLM_MODEL_KEY = DEFAULT_LLM_MODEL_KEY


def adaptive_min_support(n: int, default: int = OPENING_SUPPORT_DEFAULT, frac: float = 0.01) -> int:
    """Scale support thresholds for pilot runs."""
    return max(20, min(default, max(20, int(n * frac))))


def adaptive_ess(n: int, default: int = PREFERRED_ESS_DEFAULT, frac: float = 0.008) -> int:
    return max(15, min(default, max(15, int(n * frac))))


def adaptive_lift_threshold(n: int, preferred: float = PREFERRED_LIFT, harmful: float = HARMFUL_LIFT) -> tuple[float, float]:
    """Widen lift thresholds when sample size is small."""
    if n >= 1000:
        return preferred, harmful
    scale = max(0.5, min(1.0, n / 1000.0))
    return preferred * scale, harmful * scale


def opening_score(
    separability: float,
    stability: float,
    semantic_distinctiveness: float,
    largest_cluster_ratio: float,
    opponent_leakage: float,
    *,
    alpha: float = OPENING_SCORE_ALPHA,
    beta: float = OPENING_SCORE_BETA,
    gamma: float = OPENING_SCORE_GAMMA,
    delta: float = OPENING_SCORE_DELTA,
    eta: float = OPENING_SCORE_ETA,
) -> float:
    """Composite OpeningScore(t) from window-selection metrics."""
    return (
        alpha * separability
        + beta * stability
        + gamma * semantic_distinctiveness
        - delta * largest_cluster_ratio
        - eta * opponent_leakage
    )


@dataclass
class PipelineConfig:
    """Runtime configuration assembled from CLI flags."""

    repo_root: Path = field(default_factory=lambda: REPO_ROOT)
    action_root: Path | None = None
    sc2_knowledge_path: Path | None = None
    sc2_relations_path: Path | None = None
    output_root: Path | None = None
    skill_root: Path | None = None
    seed: int = RANDOM_SEED
    matchups: Sequence[str] = field(default_factory=lambda: list(DIRECTIONAL_MATCHUPS))
    limit: int | None = None
    from_stage: int = 0
    to_stage: int = 14
    skip_llm: bool = False
    resume: bool = True
    full_windows: bool = False
    workers: int = 4
    llm_model_key: str = DEFAULT_LLM_MODEL_KEY
    run_id: str | None = None

    def __post_init__(self) -> None:
        root = Path(self.repo_root)
        self.repo_root = root
        if self.action_root is None:
            self.action_root = root / "data" / "action_json"
        if self.sc2_knowledge_path is None:
            self.sc2_knowledge_path = root / "data_sc2_260701" / "data_base_sc2_260701.json"
        if self.sc2_relations_path is None:
            self.sc2_relations_path = (
                root / "data_sc2_260701" / "relations" / "entity_expanded_relations.json"
            )
        if self.output_root is None:
            self.output_root = root / "analysis" / "outputs_skill_v2"
        if self.skill_root is None:
            self.skill_root = root / "SKILL_MINING_V2"

    @classmethod
    def from_args(cls, args: argparse.Namespace | None = None, **kwargs: object) -> PipelineConfig:
        """Build config from argparse namespace or keyword overrides."""
        if args is not None:
            kwargs.update(
                {
                    k: getattr(args, k)
                    for k in (
                        "repo_root",
                        "action_root",
                        "output_root",
                        "skill_root",
                        "seed",
                        "matchups",
                        "limit",
                        "from_stage",
                        "to_stage",
                        "skip_llm",
                        "resume",
                        "full_windows",
                        "workers",
                        "llm_model_key",
                        "run_id",
                    )
                    if hasattr(args, k) and getattr(args, k) is not None
                }
            )
        if "matchups" in kwargs and isinstance(kwargs["matchups"], str):
            kwargs["matchups"] = [m.strip() for m in kwargs["matchups"].split(",") if m.strip()]
        return cls(**kwargs)  # type: ignore[arg-type]

    @property
    def opening_windows(self) -> tuple[int, ...]:
        return tuple(OPENING_WINDOW_CANDIDATES) if self.full_windows else OPENING_WINDOW_FAST

    def stage_dir(self, stage: int, name: str = "") -> Path:
        mapping = {
            0: "00_manifest",
            1: "01_trajectories",
            2: "02_semantics",
            3: "03_opening_windows",
            4: "04_openings",
            5: "05_snapshots",
            6: "06_states",
            7: "07_transitions",
            8: "08_transition_value",
            9: "09_graphs",
            10: "10_annotation_packets",
            11: "11_annotations",
            12: "12_skills",
            13: "13_ablations",
            14: "14_validation",
        }
        return self.output_root / mapping.get(stage, name or f"stage_{stage:02d}")

    def figures_dir(self, sub: str = "") -> Path:
        base = self.output_root / "figures"
        return base / sub if sub else base
