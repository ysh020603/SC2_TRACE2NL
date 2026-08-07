"""Models for macro actions derived from replay.game.events."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

from sc2_replay_miner.models import PlayerRecord, ReplayRecord

MacroActionCategory = Literal[
    "production",
    "construction",
    "tech_morph",
    "upgrade_research",
]


class MacroActionRecord(BaseModel):
    """A player-issued macro command, not an observed state transition."""

    replay_id: str
    player_id: int
    frame: int
    second: float
    category: MacroActionCategory
    ability_name: str
    target_name: str
    standard_action_name: str | None = None
    standard_result_name: str | None = None
    standard_result_type: str | None = None
    standard_mapping_status: str = "unmapped"
    standard_mapping_confidence: float = 0.0
    occurrence_index: int
    queued: bool = False
    build_time_seconds: float | None = None
    estimated_completion_second: float | None = None
    source: Literal["game_events"] = "game_events"
    observed_completed: Literal[False] = False


class ActionParsedReplay(BaseModel):
    """Replay metadata plus macro-only player command events."""

    replay: ReplayRecord
    players: list[PlayerRecord] = Field(default_factory=list)
    macro_actions: list[MacroActionRecord] = Field(default_factory=list)
    action_counts: dict[int, dict[str, dict[str, int]]] = Field(default_factory=dict)
    unknown_targets: list[str] = Field(default_factory=list)
    unmapped_abilities: list[str] = Field(default_factory=list)
    game_event_counts: dict[str, int] = Field(default_factory=dict)
    data_quality: dict[str, Any] = Field(default_factory=dict)
