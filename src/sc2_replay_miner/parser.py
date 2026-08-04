"""Core SC2Replay macro-event parser using sc2reader load_level=3."""

from __future__ import annotations

import traceback
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import sc2reader

from sc2_replay_miner.build_order import generate_build_orders
from sc2_replay_miner.event_utils import (
    event_location,
    event_type_name,
    file_sha256,
    length_to_seconds,
    previous_unit_type,
    replay_id_from_sha,
    resolve_player_id,
    unit_key,
    unit_raw_name,
)
from sc2_replay_miner.models import (
    PARSER_VERSION,
    MacroEventRecord,
    ParsedReplay,
    ParseErrorRecord,
    PlayerRecord,
    ReplayRecord,
)
from sc2_replay_miner.statistics import attach_statistics
from sc2_replay_miner.taxonomy import Taxonomy, load_default_config

MACRO_EVENT_TYPES = {
    "UnitInitEvent",
    "UnitDoneEvent",
    "UnitBornEvent",
    "UnitDiedEvent",
    "UnitTypeChangeEvent",
    "UpgradeCompleteEvent",
}

IGNORED_UPGRADES = {
    "GameHeartActive",
    "SprayTerran",
    "SprayZerg",
    "SprayProtoss",
    "RewardDanceMule",
    "RewardDanceOverlord",
    "RewardDanceViking",
}


def classify_error(exc: BaseException, stage: str) -> str:
    msg = str(exc).lower()
    name = type(exc).__name__
    if "cache_handles" in msg or (name == "IndexError" and stage == "load_replay"):
        return "corrupt_mpq"
    if "unsupported" in msg or "version" in msg:
        return "unsupported_version"
    if "tracker" in msg:
        return "missing_tracker_events"
    if "mpq" in msg or "archive" in msg:
        return "corrupt_mpq"
    return "unexpected_exception"


def default_project_paths() -> tuple[Path, Path]:
    """Return (project_root, config_dir) relative to this package."""
    project_root = Path(__file__).resolve().parents[2]
    return project_root, project_root / "configs"


class ReplayParser:
    def __init__(
        self,
        config_dir: str | Path | None = None,
        config: dict[str, Any] | None = None,
    ):
        _, default_config_dir = default_project_paths()
        self.config_dir = Path(config_dir) if config_dir else default_config_dir
        self.config = config or load_default_config(self.config_dir)
        self.taxonomy = Taxonomy(self.config_dir)
        parser_cfg = self.config.get("parser", {})
        self.load_level = int(parser_cfg.get("load_level", 3))
        self.load_map = bool(parser_cfg.get("load_map", False))
        bo_cfg = self.config.get("build_order", {})
        self.initial_state_max_seconds = float(bo_cfg.get("initial_state_max_seconds", 2))

    def parse(self, replay_path: str | Path) -> ParsedReplay:
        replay_path = Path(replay_path)
        sha = file_sha256(replay_path)
        rid = replay_id_from_sha(sha)
        file_size = replay_path.stat().st_size

        replay = sc2reader.load_replay(
            str(replay_path),
            load_level=self.load_level,
            load_map=self.load_map,
        )

        replay_record = self._build_replay_record(replay, replay_path, sha, rid, file_size)
        players = self._build_players(replay, rid)
        valid_player_ids = {p.player_id for p in players if not p.is_observer}

        tracker_events = list(getattr(replay, "tracker_events", []) or [])
        counts = Counter(event_type_name(e) for e in tracker_events)

        macros, initial_state = self._extract_macro_events(
            tracker_events,
            rid,
            valid_player_ids,
        )
        build_orders = generate_build_orders(macros, self.taxonomy, self.config)

        parsed = ParsedReplay(
            replay=replay_record,
            players=players,
            macro_events=macros,
            build_orders=build_orders,
            initial_state=initial_state,
            unknown_names=sorted(self.taxonomy.unknown_names),
            tracker_event_counts=dict(counts),
        )
        return attach_statistics(parsed)

    def parse_safe(
        self, replay_path: str | Path
    ) -> tuple[ParsedReplay | None, ParseErrorRecord | None]:
        replay_path = Path(replay_path)
        sha = None
        try:
            sha = file_sha256(replay_path)
        except Exception:
            sha = None
        try:
            return self.parse(replay_path), None
        except Exception as exc:
            stage = "load_replay"
            err = ParseErrorRecord(
                source_file=str(replay_path),
                file_sha256=sha,
                stage=stage,
                exception_type=type(exc).__name__,
                message=str(exc),
                traceback=traceback.format_exc(),
                timestamp=datetime.now(timezone.utc).isoformat(),
                error_class=classify_error(exc, stage),
            )
            return None, err

    def _build_replay_record(
        self,
        replay: Any,
        replay_path: Path,
        sha: str,
        rid: str,
        file_size: int,
    ) -> ReplayRecord:
        played_at = None
        unix = getattr(replay, "unix_timestamp", None)
        if unix:
            try:
                played_at = datetime.fromtimestamp(int(unix), tz=timezone.utc).isoformat()
            except Exception:
                played_at = str(unix)

        region = getattr(replay, "region", None)
        if region is not None:
            region = str(region)

        return ReplayRecord(
            replay_id=rid,
            source_file=str(replay_path.resolve()),
            file_sha256=sha,
            file_size=file_size,
            release_string=getattr(replay, "release_string", None),
            base_build=getattr(replay, "base_build", None),
            map_name=getattr(replay, "map_name", None),
            game_length_seconds=length_to_seconds(getattr(replay, "game_length", None)),
            played_at=played_at,
            game_type=getattr(replay, "game_type", None),
            real_type=getattr(replay, "real_type", None),
            region=region,
            parse_status="ok",
            parse_error=None,
            parser_version=PARSER_VERSION,
        )

    def _build_players(self, replay: Any, rid: str) -> list[PlayerRecord]:
        records: list[PlayerRecord] = []
        for player in getattr(replay, "players", []) or []:
            mmr = getattr(player, "mmr", None)
            if mmr is not None:
                try:
                    mmr = int(mmr)
                except (TypeError, ValueError):
                    mmr = None
            records.append(
                PlayerRecord(
                    replay_id=rid,
                    player_id=int(player.pid),
                    player_name=getattr(player, "name", None),
                    player_uid=getattr(player, "uid", None),
                    team_id=getattr(player, "team_id", None),
                    pick_race=getattr(player, "pick_race", None),
                    play_race=getattr(player, "play_race", None),
                    result=getattr(player, "result", None),
                    mmr=mmr,
                    mmr_available=mmr is not None,
                    is_human=getattr(player, "is_human", None),
                    is_observer=bool(getattr(player, "is_observer", False)),
                )
            )
        return records

    def _extract_macro_events(
        self,
        tracker_events: list[Any],
        rid: str,
        valid_player_ids: set[int],
    ) -> tuple[list[MacroEventRecord], dict[int, dict[str, int]]]:
        pending_init: dict[str, MacroEventRecord] = {}
        occurrence: dict[tuple[int, str, str], int] = defaultdict(int)
        initial_state: dict[int, dict[str, int]] = defaultdict(lambda: defaultdict(int))
        macros: list[MacroEventRecord] = []

        for event in tracker_events:
            etype = event_type_name(event)
            if etype not in MACRO_EVENT_TYPES:
                continue

            pid = resolve_player_id(event)
            if pid is None or pid not in valid_player_ids:
                continue

            second = float(getattr(event, "second", 0) or 0)
            frame = int(getattr(event, "frame", 0) or 0)
            is_initial = second <= self.initial_state_max_seconds
            x, y = event_location(event)
            ukey = unit_key(event)

            if etype == "UnitInitEvent":
                raw = unit_raw_name(event) or "Unknown"
                if self.taxonomy.is_ignored(raw):
                    continue
                kind = self.taxonomy.classify(raw)
                if kind == "building":
                    category = "building_start"
                elif kind in {"worker", "basic_army", "key_unit", "unknown"}:
                    category = "unit_started"
                else:
                    category = "unknown_macro"
                occurrence[(pid, category, raw)] += 1
                rec = MacroEventRecord(
                    replay_id=rid,
                    player_id=pid,
                    frame=frame,
                    second=second,
                    event_type=etype,
                    category=category,
                    raw_name=raw,
                    canonical_name=self.taxonomy.canonical_name(raw),
                    unit_key=ukey,
                    x=x,
                    y=y,
                    is_initial=is_initial,
                    is_completed=False,
                    completion_second=None,
                    occurrence_index=occurrence[(pid, category, raw)],
                    termination_reason=None,
                )
                if is_initial:
                    initial_state[pid][raw] += 1
                else:
                    macros.append(rec)
                    if ukey:
                        pending_init[ukey] = rec

            elif etype == "UnitDoneEvent":
                raw = unit_raw_name(event) or "Unknown"
                if ukey and ukey in pending_init:
                    started = pending_init.pop(ukey)
                    started.is_completed = True
                    started.completion_second = second
                # Record completion as separate macro fact (not used as BO building action).
                if self.taxonomy.is_ignored(raw):
                    continue
                if is_initial:
                    continue
                if self.taxonomy.is_building(raw) or self.taxonomy.classify(raw) == "unknown":
                    category = "building_complete"
                else:
                    category = "unit_born"
                occurrence[(pid, category, raw)] += 1
                macros.append(
                    MacroEventRecord(
                        replay_id=rid,
                        player_id=pid,
                        frame=frame,
                        second=second,
                        event_type=etype,
                        category=category,
                        raw_name=raw,
                        canonical_name=self.taxonomy.canonical_name(raw),
                        unit_key=ukey,
                        x=x,
                        y=y,
                        is_initial=False,
                        is_completed=True,
                        completion_second=second,
                        occurrence_index=occurrence[(pid, category, raw)],
                    )
                )

            elif etype == "UnitBornEvent":
                raw = unit_raw_name(event) or "Unknown"
                if self.taxonomy.is_ignored(raw):
                    continue
                if is_initial:
                    initial_state[pid][raw] += 1
                    continue
                category = "unit_born"
                occurrence[(pid, category, raw)] += 1
                macros.append(
                    MacroEventRecord(
                        replay_id=rid,
                        player_id=pid,
                        frame=frame,
                        second=second,
                        event_type=etype,
                        category=category,
                        raw_name=raw,
                        canonical_name=self.taxonomy.canonical_name(raw),
                        unit_key=ukey,
                        x=x,
                        y=y,
                        is_initial=False,
                        is_completed=True,
                        completion_second=second,
                        occurrence_index=occurrence[(pid, category, raw)],
                    )
                )

            elif etype == "UnitTypeChangeEvent":
                to_name = unit_raw_name(event) or getattr(getattr(event, "unit", None), "name", None)
                from_name = previous_unit_type(getattr(event, "unit", None), to_name)
                if not self.taxonomy.is_tech_morph(from_name, to_name):
                    continue
                raw = f"{from_name}->{to_name}"
                category = "tech_morph"
                occurrence[(pid, category, to_name or raw)] += 1
                macros.append(
                    MacroEventRecord(
                        replay_id=rid,
                        player_id=pid,
                        frame=frame,
                        second=second,
                        event_type=etype,
                        category=category,
                        raw_name=raw,
                        canonical_name=self.taxonomy.canonical_name(to_name),
                        unit_key=ukey,
                        x=x,
                        y=y,
                        is_initial=is_initial,
                        is_completed=True,
                        completion_second=second,
                        occurrence_index=occurrence[(pid, category, to_name or raw)],
                    )
                )

            elif etype == "UpgradeCompleteEvent":
                raw = str(getattr(event, "upgrade_type_name", None) or "Unknown")
                if raw in IGNORED_UPGRADES:
                    continue
                if is_initial:
                    continue
                category = "upgrade_complete"
                occurrence[(pid, category, raw)] += 1
                macros.append(
                    MacroEventRecord(
                        replay_id=rid,
                        player_id=pid,
                        frame=frame,
                        second=second,
                        event_type=etype,
                        category=category,
                        raw_name=raw,
                        canonical_name=raw,
                        unit_key=None,
                        x=None,
                        y=None,
                        is_initial=False,
                        is_completed=True,
                        completion_second=second,
                        occurrence_index=occurrence[(pid, category, raw)],
                    )
                )

            elif etype == "UnitDiedEvent":
                raw = unit_raw_name(event) or "Unknown"
                reason = "unknown"
                if ukey and ukey in pending_init:
                    started = pending_init.pop(ukey)
                    started.is_completed = False
                    started.termination_reason = "died_before_done"
                    reason = "died_before_done"
                if is_initial or self.taxonomy.is_ignored(raw):
                    continue
                # Keep death markers only for unfinished constructions / notable cases.
                if reason != "died_before_done":
                    continue
                category = "unit_died"
                occurrence[(pid, category, raw)] += 1
                macros.append(
                    MacroEventRecord(
                        replay_id=rid,
                        player_id=pid,
                        frame=frame,
                        second=second,
                        event_type=etype,
                        category=category,
                        raw_name=raw,
                        canonical_name=self.taxonomy.canonical_name(raw),
                        unit_key=ukey,
                        x=x,
                        y=y,
                        is_initial=False,
                        is_completed=False,
                        completion_second=None,
                        occurrence_index=occurrence[(pid, category, raw)],
                        termination_reason=reason,
                    )
                )

        # Mark unfinished inits at end of game
        for started in pending_init.values():
            if started.is_completed is False and not started.termination_reason:
                started.termination_reason = "game_ended"

        macros.sort(key=lambda e: (e.player_id, e.frame, e.event_type, e.canonical_name))
        initial_plain = {pid: dict(vals) for pid, vals in initial_state.items()}
        return macros, initial_plain


def parse_replay(
    replay_path: str | Path,
    config_dir: str | Path | None = None,
) -> ParsedReplay:
    return ReplayParser(config_dir=config_dir).parse(replay_path)
