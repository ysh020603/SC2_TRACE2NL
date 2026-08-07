"""Macro-only parser for player commands stored in replay.game.events."""

from __future__ import annotations

import traceback
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import sc2reader
from sc2reader.events.game import CommandEvent

from sc2_replay_miner.action_models import (
    ActionParsedReplay,
    MacroActionCategory,
    MacroActionRecord,
)
from sc2_replay_miner.event_utils import file_sha256, replay_id_from_sha, safe_float
from sc2_replay_miner.models import ParseErrorRecord
from sc2_replay_miner.parser import ReplayParser
from sc2_replay_miner.standard_actions import DEFAULT_DATABASE, StandardActionMapper
from sc2_replay_miner.taxonomy import Taxonomy, load_default_config

UPGRADE_PREFIXES = ("Research", "Upgrade", "Evolve")
TECH_MORPH_PREFIXES = ("UpgradeTo", "Morph")
IGNORED_MACRO_ABILITY_PREFIXES = ("Hallucinate",)


def _event_player_id(event: Any) -> int | None:
    """Resolve sc2reader game-event user ids to replay player ids."""
    player = getattr(event, "player", None)
    pid = getattr(player, "pid", None)
    if pid is None:
        return None
    try:
        return int(pid)
    except (TypeError, ValueError):
        return None


def _upgrade_target_name(ability_name: str) -> str:
    name = ability_name
    changed = True
    while changed:
        changed = False
        for prefix in UPGRADE_PREFIXES:
            if name.startswith(prefix) and len(name) > len(prefix):
                name = name[len(prefix) :]
                changed = True
                break
    return name or ability_name


class MacroActionParser:
    """Extract production/build/research commands while excluding micro actions."""

    def __init__(
        self,
        config_dir: str | Path | None = None,
        config: dict[str, Any] | None = None,
        action_database: str | Path = DEFAULT_DATABASE,
    ) -> None:
        if config_dir is None:
            config_dir = Path(__file__).resolve().parents[2] / "configs"
        self.config_dir = Path(config_dir)
        self.config = config if config is not None else load_default_config(self.config_dir)
        self.taxonomy = Taxonomy(self.config_dir)
        self.action_mapper = StandardActionMapper(action_database)
        # Reuse the existing metadata/player builders without changing tracker parsing.
        self._metadata_parser = ReplayParser(config_dir=self.config_dir, config=self.config)

    def parse(self, replay_path: str | Path) -> ActionParsedReplay:
        replay_path = Path(replay_path)
        sha = file_sha256(replay_path)
        rid = replay_id_from_sha(sha)
        replay = sc2reader.load_replay(str(replay_path), load_level=4, load_map=False)

        replay_record = self._metadata_parser._build_replay_record(
            replay,
            replay_path,
            sha,
            rid,
            replay_path.stat().st_size,
        )
        players = self._metadata_parser._build_players(replay, rid)
        valid_player_ids = {p.player_id for p in players if not p.is_observer}
        game_events = list(getattr(replay, "game_events", []) or [])
        actions = self._extract_actions(game_events, rid, valid_player_ids)

        counts: dict[int, dict[str, dict[str, int]]] = defaultdict(
            lambda: {
                "production": Counter(),
                "construction": Counter(),
                "tech_morph": Counter(),
                "upgrade_research": Counter(),
            }
        )
        for action in actions:
            counts[action.player_id][action.category][action.target_name] += 1

        plain_counts = {
            pid: {category: dict(values) for category, values in categories.items()}
            for pid, categories in counts.items()
        }
        event_counts = Counter(type(event).__name__ for event in game_events)
        tracker_available = bool(getattr(replay, "tracker_events", []) or [])
        action_player_ids = {action.player_id for action in actions}
        empty_action_player_ids = sorted(valid_player_ids - action_player_ids)
        duration = replay_record.game_length_seconds
        unmapped_abilities = sorted(
            {
                action.ability_name
                for action in actions
                if action.standard_action_name is None
            }
        )
        mapped_count = sum(
            action.standard_action_name is not None for action in actions
        )

        return ActionParsedReplay(
            replay=replay_record,
            players=players,
            macro_actions=actions,
            action_counts=plain_counts,
            unknown_targets=sorted(self.taxonomy.unknown_names),
            unmapped_abilities=unmapped_abilities,
            game_event_counts=dict(event_counts),
            data_quality={
                "parse_mode": "game_events_macro_actions",
                "source": "replay.game.events",
                "tracker_available": tracker_available,
                "semantics": "player_command_intent",
                "positions_included": False,
                "micro_actions_included": False,
                "completion_is_observed": False,
                "estimated_completion_uses_balance_build_time": True,
                "short_game_under_60_seconds": duration is not None and duration < 60,
                "players_without_macro_actions": empty_action_player_ids,
                "standard_action_database": str(
                    self.action_mapper.database_path.resolve()
                ),
                "standard_action_mapped": mapped_count,
                "standard_action_unmapped": len(actions) - mapped_count,
                "unavailable": [
                    "confirmed_unit_birth",
                    "confirmed_building_completion",
                    "confirmed_upgrade_completion",
                    "unit_death",
                    "resource_state",
                    "supply_state",
                    "reliable_command_cancellation_linkage",
                ],
            },
        )

    def parse_safe(
        self, replay_path: str | Path
    ) -> tuple[ActionParsedReplay | None, ParseErrorRecord | None]:
        replay_path = Path(replay_path)
        sha = None
        try:
            sha = file_sha256(replay_path)
            return self.parse(replay_path), None
        except Exception as exc:
            return None, ParseErrorRecord(
                source_file=str(replay_path),
                file_sha256=sha,
                stage="load_game_events",
                exception_type=type(exc).__name__,
                message=str(exc),
                traceback=traceback.format_exc(),
                timestamp=datetime.now(timezone.utc).isoformat(),
                error_class="game_events_parse_error",
            )

    def _extract_actions(
        self,
        game_events: list[Any],
        rid: str,
        valid_player_ids: set[int],
    ) -> list[MacroActionRecord]:
        occurrence: Counter[tuple[int, str, str]] = Counter()
        actions: list[MacroActionRecord] = []

        for event in game_events:
            if not isinstance(event, CommandEvent):
                continue
            pid = _event_player_id(event)
            if pid is None or pid not in valid_player_ids:
                continue

            ability_name = str(getattr(event, "ability_name", "") or "")
            if ability_name.startswith(IGNORED_MACRO_ABILITY_PREFIXES):
                continue
            ability = getattr(event, "ability", None)
            category: MacroActionCategory | None = None
            target_name: str | None = None
            build_time: float | None = None

            if getattr(event, "has_ability", False) and getattr(
                ability, "is_build", False
            ):
                build_unit = getattr(ability, "build_unit", None)
                target_name = getattr(build_unit, "name", None)
                if not target_name or self.taxonomy.is_ignored(target_name):
                    continue
                target_name = self.taxonomy.canonical_name(str(target_name))
                build_time = safe_float(getattr(ability, "build_time", None))
                if self.taxonomy.is_building(target_name):
                    category = (
                        "tech_morph"
                        if ability_name.startswith(TECH_MORPH_PREFIXES)
                        and not ability_name.startswith("Build")
                        else "construction"
                    )
                else:
                    category = "production"
            elif ability_name.startswith(UPGRADE_PREFIXES):
                category = "upgrade_research"
                target_name = _upgrade_target_name(ability_name)

            if category is None or target_name is None:
                continue

            frame = int(getattr(event, "frame", 0) or 0)
            second = float(getattr(event, "second", 0) or 0)
            occurrence[(pid, category, target_name)] += 1
            flag = getattr(event, "flag", None)
            queued = bool(flag.get("queued")) if isinstance(flag, dict) else False
            estimated_completion = (
                second + build_time if build_time is not None and build_time > 0 else None
            )
            standard = self.action_mapper.resolve(
                ability_name,
                target_name,
                category,
            )

            actions.append(
                MacroActionRecord(
                    replay_id=rid,
                    player_id=pid,
                    frame=frame,
                    second=second,
                    category=category,
                    ability_name=ability_name,
                    target_name=target_name,
                    standard_action_name=standard.name,
                    standard_result_name=standard.result_name,
                    standard_result_type=standard.result_type,
                    standard_mapping_status=standard.status,
                    standard_mapping_confidence=standard.confidence,
                    occurrence_index=occurrence[(pid, category, target_name)],
                    queued=queued,
                    build_time_seconds=build_time,
                    estimated_completion_second=estimated_completion,
                )
            )

        actions.sort(key=lambda action: (action.frame, action.player_id, action.occurrence_index))
        return actions
