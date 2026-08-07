"""JSON exporters for macro commands derived from replay.game.events."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from sc2_replay_miner.action_models import ActionParsedReplay, MacroActionRecord
from sc2_replay_miner.event_utils import format_clock
from sc2_replay_miner.models import PlayerRecord


def _action_item(
    action: MacroActionRecord,
    player: PlayerRecord | None,
    *,
    include_player: bool,
) -> dict[str, Any]:
    item: dict[str, Any] = {
        "time": format_clock(action.second),
        "second": action.second,
        "frame": action.frame,
        "event": action.category,
        "action": "ordered",
        "name": action.target_name,
        "ability": action.ability_name,
        "standard_action_name": action.standard_action_name,
        "standard_result_name": action.standard_result_name,
        "standard_result_type": action.standard_result_type,
        "standard_mapping_status": action.standard_mapping_status,
        "standard_mapping_confidence": action.standard_mapping_confidence,
        "occurrence_index": action.occurrence_index,
        "queued": action.queued,
        "build_time_seconds": action.build_time_seconds,
        "estimated_completion_second": action.estimated_completion_second,
        "estimated_completion_time": (
            format_clock(action.estimated_completion_second)
            if action.estimated_completion_second is not None
            else None
        ),
        "source": action.source,
        "observed_completed": action.observed_completed,
        "text": (
            f"{format_clock(action.second)} {action.target_name}"
            f" #{action.occurrence_index} ordered"
        ),
    }
    if include_player:
        item.update(
            {
                "player_id": action.player_id,
                "player_name": player.player_name if player else None,
                "race": player.play_race if player else None,
            }
        )
    return item


def _compatible_statistics(category_counts: dict[str, dict[str, int]]) -> dict[str, Any]:
    return {
        "units": dict(category_counts.get("production", {})),
        "buildings": {
            **category_counts.get("construction", {}),
            **category_counts.get("tech_morph", {}),
        },
        "upgrades": dict(category_counts.get("upgrade_research", {})),
        "source": "game_events_command_intent",
        "counts_mean": "commands_ordered_not_confirmed_outputs",
    }


def build_action_match_json(parsed: ActionParsedReplay) -> dict[str, Any]:
    """Build a full-match-compatible JSON containing macro command intents only."""
    players = [player for player in parsed.players if not player.is_observer]
    player_by_id = {player.player_id: player for player in players}
    winners = [player for player in players if (player.result or "").lower() == "win"]
    winner = winners[0] if len(winners) == 1 else None

    timeline = [
        _action_item(action, player_by_id.get(action.player_id), include_player=True)
        for action in parsed.macro_actions
    ]
    actions_by_player: dict[int, list[MacroActionRecord]] = {
        player.player_id: [] for player in players
    }
    for action in parsed.macro_actions:
        actions_by_player.setdefault(action.player_id, []).append(action)

    player_blocks: list[dict[str, Any]] = []
    for player in sorted(players, key=lambda item: item.player_id):
        actions = [
            _action_item(action, player, include_player=False)
            for action in actions_by_player.get(player.player_id, [])
        ]
        player_blocks.append(
            {
                "player_id": player.player_id,
                "name": player.player_name,
                "race": player.play_race,
                "pick_race": player.pick_race,
                "result": player.result,
                "mmr": player.mmr,
                "mmr_available": player.mmr_available,
                "team_id": player.team_id,
                "is_winner": (player.result or "").lower() == "win",
                "initial_state": {},
                "statistics": _compatible_statistics(
                    parsed.action_counts.get(player.player_id, {})
                ),
                "build_order": actions,
            }
        )

    matchup = "".join(sorted((player.play_race or "?")[0] for player in players))
    winners_payload = [
        {
            "player_id": player.player_id,
            "name": player.player_name,
            "race": player.play_race,
            "mmr": player.mmr,
            "team_id": player.team_id,
        }
        for player in winners
    ]

    return {
        "replay_id": parsed.replay.replay_id,
        "source_file": parsed.replay.source_file,
        "map_name": parsed.replay.map_name,
        "version": parsed.replay.release_string,
        "base_build": parsed.replay.base_build,
        "duration_seconds": parsed.replay.game_length_seconds,
        "duration_clock": format_clock(parsed.replay.game_length_seconds or 0),
        "game_type": parsed.replay.game_type,
        "real_type": parsed.replay.real_type,
        "region": parsed.replay.region,
        "played_at": parsed.replay.played_at,
        "matchup": matchup or None,
        "winner": (
            {
                "player_id": winner.player_id,
                "name": winner.player_name,
                "race": winner.play_race,
                "mmr": winner.mmr,
                "team_id": winner.team_id,
            }
            if winner
            else None
        ),
        "winners": winners_payload,
        "players": player_blocks,
        "timeline": timeline,
        "macro_action_count": len(parsed.macro_actions),
        "game_event_counts": parsed.game_event_counts,
        "unknown_targets": parsed.unknown_targets,
        "unmapped_abilities": parsed.unmapped_abilities,
        "tracker_event_counts": {},
        "data_quality": parsed.data_quality,
        "parser_version": parsed.replay.parser_version,
    }


def write_action_match_json(
    parsed: ActionParsedReplay,
    output_path: str | Path,
) -> Path:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    payload = build_action_match_json(parsed)
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return output_path
