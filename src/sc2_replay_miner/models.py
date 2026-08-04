"""Pydantic models for parsed SC2 replay records."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, Field

PARSER_VERSION = "0.1.0"

MacroCategory = Literal[
    "building_start",
    "building_complete",
    "unit_born",
    "unit_started",
    "tech_morph",
    "upgrade_complete",
    "unit_died",
    "unknown_macro",
]

BoType = Literal["core_6m", "strategy_8m", "all_macro"]


class ReplayRecord(BaseModel):
    replay_id: str
    source_file: str
    file_sha256: str
    file_size: int
    release_string: str | None = None
    base_build: int | None = None
    map_name: str | None = None
    game_length_seconds: float | None = None
    played_at: str | None = None
    game_type: str | None = None
    real_type: str | None = None
    region: str | None = None
    parse_status: str = "ok"
    parse_error: str | None = None
    parser_version: str = PARSER_VERSION


class PlayerRecord(BaseModel):
    replay_id: str
    player_id: int
    player_name: str | None = None
    player_uid: int | None = None
    team_id: int | None = None
    pick_race: str | None = None
    play_race: str | None = None
    result: str | None = None
    mmr: int | None = None
    mmr_available: bool = False
    is_human: bool | None = None
    is_observer: bool | None = None


class MacroEventRecord(BaseModel):
    replay_id: str
    player_id: int
    frame: int
    second: float
    event_type: str
    category: str
    raw_name: str
    canonical_name: str
    unit_key: str | None = None
    x: float | None = None
    y: float | None = None
    is_initial: bool = False
    is_completed: bool | None = None
    completion_second: float | None = None
    occurrence_index: int | None = None
    termination_reason: str | None = None


class BuildOrderRecord(BaseModel):
    replay_id: str
    player_id: int
    bo_type: BoType
    bo_index: int
    frame: int
    second: float
    category: str
    canonical_name: str
    occurrence_index: int | None = None
    x: float | None = None
    y: float | None = None


class ParseErrorRecord(BaseModel):
    source_file: str
    file_sha256: str | None = None
    stage: str
    exception_type: str
    message: str
    traceback: str
    timestamp: str
    error_class: str = "unexpected_exception"


class ParsedReplay(BaseModel):
    replay: ReplayRecord
    players: list[PlayerRecord] = Field(default_factory=list)
    macro_events: list[MacroEventRecord] = Field(default_factory=list)
    build_orders: list[BuildOrderRecord] = Field(default_factory=list)
    initial_state: dict[int, dict[str, int]] = Field(default_factory=dict)
    unknown_names: list[str] = Field(default_factory=list)
    tracker_event_counts: dict[str, int] = Field(default_factory=dict)
    extras: dict[str, Any] = Field(default_factory=dict)
