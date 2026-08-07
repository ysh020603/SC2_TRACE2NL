#!/usr/bin/env python3
"""Phase 1 data-quality audit for action_json (plan.md §3 / §21).

Reads stratified macro-action JSON under data/action_json/<matchup>/,
builds replay-level and player-opening tables, and writes audit outputs.
"""

from __future__ import annotations

import argparse
import json
import math
import statistics
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

VALID_RACES = {"Terran", "Protoss", "Zerg"}
VALID_RESULTS = {"Win", "Loss", "Tie", "Undecided"}
MATCHUPS = ("PvP", "PvT", "PvZ", "TvT", "TvZ", "ZvZ")
HORIZONS = (210, 300, 420)
MMR_REASONABLE = (1000, 7500)
FPS_HINT = 16  # SC2 game-loop frames per game-second (approx)

# Blizzard replay metadata may localize race display names.
RACE_ALIASES = {
    "terran": "Terran",
    "protoss": "Protoss",
    "zerg": "Zerg",
    "т": "Terran",
    "п": "Protoss",
    "з": "Zerg",
    "терраны": "Terran",
    "протоссы": "Protoss",
    "зерги": "Zerg",
    "terrani": "Terran",
    "protossi": "Protoss",
    "zergowie": "Zerg",
}


def normalize_race(race: Any) -> str | None:
    if race is None:
        return None
    text = str(race).strip()
    if text in VALID_RACES:
        return text
    return RACE_ALIASES.get(text.lower())


def repo_root() -> Path:
    return Path(__file__).resolve().parents[2]


def load_manifest(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def iter_action_json(action_root: Path) -> list[tuple[str, Path]]:
    files: list[tuple[str, Path]] = []
    for matchup in MATCHUPS:
        d = action_root / matchup
        if not d.is_dir():
            continue
        for p in sorted(d.glob("*.json")):
            name = p.name
            if (
                name.startswith("summary")
                or name.endswith("_summary.json")
                or name in {"full_parse_summary.json"}
            ):
                continue
            files.append((matchup, p))
    return files


def safe_div(a: float, b: float) -> float | None:
    if b is None or b == 0:
        return None
    return a / b


def percentile(values: list[float], q: float) -> float | None:
    if not values:
        return None
    xs = sorted(values)
    if len(xs) == 1:
        return float(xs[0])
    pos = (len(xs) - 1) * q
    lo = int(math.floor(pos))
    hi = int(math.ceil(pos))
    if lo == hi:
        return float(xs[lo])
    w = pos - lo
    return float(xs[lo] * (1 - w) + xs[hi] * w)


def check_time_consistency(events: list[dict[str, Any]]) -> dict[str, Any]:
    non_mono = 0
    frame_second_mismatch = 0
    prev_second = None
    prev_frame = None
    for ev in events:
        second = ev.get("second")
        frame = ev.get("frame")
        if second is not None and prev_second is not None and second + 1e-9 < prev_second:
            non_mono += 1
        if frame is not None and prev_frame is not None and frame < prev_frame:
            non_mono += 1
        if second is not None and frame is not None and second > 0:
            # allow small drift; expected ~16 fps in game time
            implied = frame / max(second, 1e-9)
            if abs(implied - FPS_HINT) > 1.5:
                frame_second_mismatch += 1
        if second is not None:
            prev_second = second
        if frame is not None:
            prev_frame = frame
    return {
        "time_non_monotonic": non_mono,
        "frame_second_mismatch": frame_second_mismatch,
    }


def find_strict_duplicates(events: list[dict[str, Any]]) -> int:
    """Identical frame+ability+result+occurrence_index duplicates (plan §3.4)."""
    seen: set[tuple[Any, ...]] = set()
    dups = 0
    for ev in events:
        key = (
            ev.get("frame"),
            ev.get("ability"),
            ev.get("standard_action_name") or ev.get("name"),
            ev.get("standard_result_name") or ev.get("name"),
            ev.get("occurrence_index"),
        )
        if key in seen:
            dups += 1
        else:
            seen.add(key)
    return dups


def audit_one(matchup_dir: str, path: Path) -> tuple[dict[str, Any], list[dict[str, Any]], list[str]]:
    issues: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        issues.append(f"json_parse_error:{exc}")
        return (
            {
                "replay_id": path.stem,
                "source_file": str(path),
                "matchup_dir": matchup_dir,
                "valid": False,
                "invalid_reasons": ";".join(issues),
            },
            [],
            issues,
        )

    required = [
        "replay_id",
        "duration_seconds",
        "game_type",
        "players",
        "data_quality",
    ]
    for key in required:
        if key not in data:
            issues.append(f"missing_field:{key}")

    players = data.get("players") or []
    if not isinstance(players, list):
        issues.append("players_not_list")
        players = []

    if len(players) != 2:
        issues.append(f"player_count_ne_2:{len(players)}")

    game_type = data.get("game_type")
    real_type = data.get("real_type")
    if game_type not in (None, "1v1") or real_type not in (None, "1v1"):
        issues.append(f"not_1v1:game_type={game_type}:real_type={real_type}")

    raw_races = [p.get("race") for p in players]
    races = [normalize_race(r) for r in raw_races]
    for raw, norm in zip(raw_races, races, strict=False):
        if norm is None:
            issues.append(f"invalid_race:{raw}")
        elif raw != norm:
            # localized label; keep as soft note only once per distinct raw value
            issues.append(f"localized_race:{raw}->{norm}")

    results = [p.get("result") for p in players]
    for res in results:
        if res not in VALID_RESULTS and res is not None:
            issues.append(f"invalid_result:{res}")

    wins = sum(1 for r in results if r == "Win")
    losses = sum(1 for r in results if r == "Loss")
    if wins == 2:
        issues.append("both_win")
    if losses == 2 and wins == 0:
        issues.append("both_loss")
    if all(r is None for r in results):
        issues.append("results_missing")
    if wins == 1 and losses == 1:
        result_ok = True
    elif wins == 0 and losses == 0 and any(r == "Tie" for r in results):
        result_ok = True
    else:
        result_ok = False
        if "both_win" not in issues and "both_loss" not in issues and "results_missing" not in issues:
            issues.append(f"non_exclusive_results:{results}")

    dq = data.get("data_quality") or {}
    mapped = int(dq.get("standard_action_mapped") or 0)
    unmapped = int(dq.get("standard_action_unmapped") or 0)
    total_map = mapped + unmapped
    map_rate = safe_div(mapped, total_map)

    all_events: list[dict[str, Any]] = []
    player_rows: list[dict[str, Any]] = []
    empty_bo_players = 0
    low_conf_events = 0
    missing_standard_result = 0
    strict_dups = 0
    time_non_mono = 0
    frame_second_mismatch = 0
    max_bo_second = 0.0
    event_cats: Counter[str] = Counter()

    for p in players:
        bo = p.get("build_order") or []
        if not isinstance(bo, list):
            issues.append(f"build_order_not_list:player_{p.get('player_id')}")
            bo = []
        if len(bo) == 0:
            empty_bo_players += 1
        all_events.extend(bo)
        tc = check_time_consistency(bo)
        time_non_mono += tc["time_non_monotonic"]
        frame_second_mismatch += tc["frame_second_mismatch"]
        strict_dups += find_strict_duplicates(bo)
        for ev in bo:
            sec = ev.get("second")
            if isinstance(sec, (int, float)):
                max_bo_second = max(max_bo_second, float(sec))
            conf = ev.get("standard_mapping_confidence")
            if conf is not None and conf < 0.90:
                low_conf_events += 1
            if not ev.get("standard_result_name"):
                missing_standard_result += 1
            event_cats[str(ev.get("event") or "unknown")] += 1

    if time_non_mono:
        issues.append(f"time_non_monotonic:{time_non_mono}")
    if empty_bo_players == len(players) and len(players) == 2:
        issues.append("both_players_empty_bo")

    duration = data.get("duration_seconds")
    try:
        duration_f = float(duration) if duration is not None else None
    except (TypeError, ValueError):
        duration_f = None
        issues.append("bad_duration_seconds")

    time_scale_ratio = None
    if duration_f is not None and duration_f > 0 and max_bo_second > 0:
        time_scale_ratio = max_bo_second / duration_f

    mmrs = []
    for p in players:
        mmr = p.get("mmr")
        available = p.get("mmr_available")
        if mmr is None or available is False:
            continue
        try:
            mmr_f = float(mmr)
        except (TypeError, ValueError):
            issues.append(f"bad_mmr:player_{p.get('player_id')}")
            continue
        mmrs.append(mmr_f)
        if not (MMR_REASONABLE[0] <= mmr_f <= MMR_REASONABLE[1]):
            issues.append(f"mmr_out_of_range:{mmr_f}")

    # Hard-invalid: schema / not 1v1 / bad player count / both win
    hard_flags = {
        "json_parse_error",
        "missing_field",
        "players_not_list",
        "player_count_ne_2",
        "not_1v1",
        "both_win",
    }
    hard_invalid = any(any(i.startswith(h) for h in hard_flags) for i in issues)
    # Soft quality flags remain on the row but do not drop from analysis tables
    valid = not hard_invalid

    replay_row: dict[str, Any] = {
        "replay_id": data.get("replay_id") or path.stem,
        "source_json": str(path),
        "source_file": data.get("source_file"),
        "matchup_dir": matchup_dir,
        "matchup": data.get("matchup"),
        "map_name": data.get("map_name"),
        "version": data.get("version"),
        "base_build": data.get("base_build"),
        "region": data.get("region"),
        "played_at": data.get("played_at"),
        "game_type": game_type,
        "real_type": real_type,
        "duration_real_seconds": duration_f,
        "duration_game_seconds": max_bo_second if max_bo_second > 0 else None,
        "time_scale_ratio": time_scale_ratio,
        "macro_action_count": data.get("macro_action_count", len(all_events)),
        "mapped_actions": mapped,
        "unmapped_actions": unmapped,
        "mapping_rate": map_rate,
        "low_confidence_events": low_conf_events,
        "missing_standard_result_name": missing_standard_result,
        "empty_bo_player_count": empty_bo_players,
        "strict_duplicate_events": strict_dups,
        "time_non_monotonic_events": time_non_mono,
        "frame_second_mismatch_events": frame_second_mismatch,
        "short_game_under_60_seconds": bool(dq.get("short_game_under_60_seconds")),
        "tracker_available": bool(dq.get("tracker_available")),
        "result_ok": result_ok,
        "winner_player_id": (data.get("winner") or {}).get("player_id"),
        "mmr_available_count": len(mmrs),
        "mmr_mean": statistics.mean(mmrs) if mmrs else None,
        "production_count": event_cats.get("production", 0),
        "construction_count": event_cats.get("construction", 0),
        "tech_morph_count": event_cats.get("tech_morph", 0),
        "upgrade_research_count": event_cats.get("upgrade_research", 0),
        "valid": valid,
        "invalid_reasons": ";".join(issues),
        "issue_count": len(issues),
    }

    # opening observation flags (game-time): prefer max BO second, else ratio*duration
    observed_game_seconds = max_bo_second
    if observed_game_seconds <= 0 and duration_f is not None and time_scale_ratio is not None:
        observed_game_seconds = duration_f * time_scale_ratio
    for h in HORIZONS:
        replay_row[f"opening_observed_to_{h}"] = observed_game_seconds >= h

    # player rows (one per player perspective)
    by_id = {p.get("player_id"): p for p in players}
    ids = list(by_id.keys())
    for pid, p in by_id.items():
        opp = None
        for other_id in ids:
            if other_id != pid:
                opp = by_id[other_id]
                break
        bo = p.get("build_order") or []
        if not isinstance(bo, list):
            bo = []
        max_sec = 0.0
        for ev in bo:
            sec = ev.get("second")
            if isinstance(sec, (int, float)):
                max_sec = max(max_sec, float(sec))
        mmr = p.get("mmr") if p.get("mmr_available", True) else None
        opp_mmr = None
        if opp is not None and opp.get("mmr_available", True):
            opp_mmr = opp.get("mmr")
        try:
            mmr_f = float(mmr) if mmr is not None else None
        except (TypeError, ValueError):
            mmr_f = None
        try:
            opp_mmr_f = float(opp_mmr) if opp_mmr is not None else None
        except (TypeError, ValueError):
            opp_mmr_f = None

        horizon_counts = {}
        for h in HORIZONS:
            horizon_counts[f"ordered_by_{h}"] = sum(
                1
                for ev in bo
                if isinstance(ev.get("second"), (int, float)) and float(ev["second"]) <= h
            )

        player_rows.append(
            {
                "replay_id": replay_row["replay_id"],
                "player_id": pid,
                "race": normalize_race(p.get("race")) or p.get("race"),
                "race_raw": p.get("race"),
                "opponent_race": None
                if opp is None
                else (normalize_race(opp.get("race")) or opp.get("race")),
                "result": p.get("result"),
                "mmr": mmr_f,
                "opponent_mmr": opp_mmr_f,
                "mmr_diff": None
                if mmr_f is None or opp_mmr_f is None
                else mmr_f - opp_mmr_f,
                "matchup_dir": matchup_dir,
                "matchup": data.get("matchup"),
                "map_name": data.get("map_name"),
                "version": data.get("version"),
                "base_build": data.get("base_build"),
                "region": data.get("region"),
                "played_at": data.get("played_at"),
                "duration_real_seconds": duration_f,
                "duration_game_seconds": replay_row["duration_game_seconds"],
                "time_scale_ratio": time_scale_ratio,
                "build_order_len": len(bo),
                "max_build_order_second": max_sec if max_sec > 0 else None,
                "opening_observed_to_210": replay_row["opening_observed_to_210"],
                "opening_observed_to_300": replay_row["opening_observed_to_300"],
                "opening_observed_to_420": replay_row["opening_observed_to_420"],
                **horizon_counts,
                "valid_replay": valid,
            }
        )

    return replay_row, player_rows, issues


def summarize(
    replay_df: pd.DataFrame,
    player_df: pd.DataFrame,
    manifest: dict[str, Any],
    action_root: Path,
) -> dict[str, Any]:
    ratios = [
        float(x)
        for x in replay_df["time_scale_ratio"].dropna().tolist()
        if isinstance(x, (int, float)) and math.isfinite(float(x))
    ]
    mmr_vals = [
        float(x)
        for x in player_df["mmr"].dropna().tolist()
        if isinstance(x, (int, float)) and math.isfinite(float(x))
    ]
    total_events = int(replay_df["macro_action_count"].fillna(0).sum())
    mapped = int(replay_df["mapped_actions"].fillna(0).sum())
    unmapped = int(replay_df["unmapped_actions"].fillna(0).sum())

    invalid = replay_df.loc[~replay_df["valid"]]
    soft_issue_counter: Counter[str] = Counter()
    for reasons in replay_df["invalid_reasons"].fillna(""):
        if not reasons:
            continue
        for part in str(reasons).split(";"):
            if not part:
                continue
            soft_issue_counter[part.split(":")[0]] += 1

    race_counts = player_df.loc[player_df["valid_replay"], "race"].value_counts().to_dict()
    localized = player_df.loc[
        player_df["race_raw"].astype(str) != player_df["race"].astype(str),
        "race_raw",
    ].value_counts().to_dict()
    matchup_counts = (
        replay_df.loc[replay_df["valid"], "matchup_dir"].value_counts().to_dict()
    )
    version_counts = (
        replay_df.loc[replay_df["valid"], "version"].value_counts().to_dict()
    )
    region_counts = (
        replay_df.loc[replay_df["valid"], "region"].fillna("unknown").value_counts().to_dict()
    )

    empty_bo_rate = float(
        (replay_df["empty_bo_player_count"] > 0).mean() if len(replay_df) else 0.0
    )
    both_empty = float(
        (replay_df["empty_bo_player_count"] >= 2).mean() if len(replay_df) else 0.0
    )
    mmr_missing_rate = float(player_df["mmr"].isna().mean()) if len(player_df) else 0.0

    summary = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "action_json_root": str(action_root),
        "raw_data_manifest": {
            "written": manifest.get("written"),
            "duplicate_skipped": manifest.get("duplicate_skipped"),
            "parse_errors": manifest.get("parse_errors"),
            "matchup_counts": manifest.get("matchup_counts"),
        },
        "audit_scope": {
            "note": (
                "Full corpus is ~103k .SC2Replay under raw_data/by_matchup. "
                "This audit runs on the stratified action_json sample "
                "(40 per matchup, seed=42) already placed under data/action_json/."
            ),
            "json_files": int(len(replay_df)),
            "valid_replays": int(replay_df["valid"].sum()),
            "invalid_replays": int((~replay_df["valid"]).sum()),
            "player_rows": int(len(player_df)),
        },
        "sample_sizes": {
            "by_matchup_dir": matchup_counts,
            "by_race_player": race_counts,
            "localized_race_raw_counts": localized,
            "by_version": version_counts,
            "by_region": region_counts,
        },
        "mapping": {
            "mapped_actions": mapped,
            "unmapped_actions": unmapped,
            "mapping_rate": safe_div(mapped, mapped + unmapped),
            "total_macro_actions": total_events,
            "event_category_totals": {
                "production": int(replay_df["production_count"].sum()),
                "construction": int(replay_df["construction_count"].sum()),
                "tech_morph": int(replay_df["tech_morph_count"].sum()),
                "upgrade_research": int(replay_df["upgrade_research_count"].sum()),
            },
            "low_confidence_events": int(replay_df["low_confidence_events"].sum()),
            "missing_standard_result_name": int(
                replay_df["missing_standard_result_name"].sum()
            ),
        },
        "mmr": {
            "missing_rate_player": mmr_missing_rate,
            "count": len(mmr_vals),
            "min": min(mmr_vals) if mmr_vals else None,
            "p25": percentile(mmr_vals, 0.25),
            "median": percentile(mmr_vals, 0.50),
            "p75": percentile(mmr_vals, 0.75),
            "max": max(mmr_vals) if mmr_vals else None,
            "reasonable_range": list(MMR_REASONABLE),
        },
        "build_order": {
            "replays_with_any_empty_player_bo": empty_bo_rate,
            "replays_with_both_empty_bo": both_empty,
            "strict_duplicate_events": int(replay_df["strict_duplicate_events"].sum()),
            "time_non_monotonic_events": int(
                replay_df["time_non_monotonic_events"].sum()
            ),
            "frame_second_mismatch_events": int(
                replay_df["frame_second_mismatch_events"].sum()
            ),
            "short_game_under_60_seconds": int(
                replay_df["short_game_under_60_seconds"].sum()
            ),
        },
        "time_scale": {
            "definition": "max_valid_build_order_second / duration_seconds",
            "n": len(ratios),
            "min": min(ratios) if ratios else None,
            "p25": percentile(ratios, 0.25),
            "median": percentile(ratios, 0.50),
            "p75": percentile(ratios, 0.75),
            "max": max(ratios) if ratios else None,
            "fraction_in_1.30_1.50": (
                sum(1 for r in ratios if 1.30 <= r <= 1.50) / len(ratios)
                if ratios
                else None
            ),
            "interpretation": (
                "Values clustered near ~1.38–1.40 indicate real-time duration vs "
                "game-time build_order.second, not parse errors."
            ),
        },
        "opening_windows": {
            f"observed_to_{h}": int(replay_df[f"opening_observed_to_{h}"].sum())
            for h in HORIZONS
        },
        "issue_prefix_counts": dict(soft_issue_counter),
        "hard_invalid_replay_ids": invalid["replay_id"].tolist(),
    }
    return summary


def render_report(
    summary: dict[str, Any],
    replay_df: pd.DataFrame,
    out_md: Path,
) -> None:
    m = summary
    raw = m.get("raw_data_manifest") or {}
    scope = m.get("audit_scope") or {}
    mapping = m.get("mapping") or {}
    mmr = m.get("mmr") or {}
    bo = m.get("build_order") or {}
    ts = m.get("time_scale") or {}
    samples = m.get("sample_sizes") or {}

    def fmt(x: Any, digits: int = 4) -> str:
        if x is None:
            return "n/a"
        if isinstance(x, float):
            return f"{x:.{digits}f}"
        return str(x)

    lines = [
        "# 数据质量报告（Phase 1）",
        "",
        f"生成时间（UTC）：`{m.get('generated_at')}`",
        "",
        "依据：`plan.md` §3 数据质量审计 / §21 Phase 1。",
        "",
        "## 1. 数据范围与放置",
        "",
        "- 原始 replay：`raw_data/by_matchup/<matchup>/*.SC2Replay`",
        "- 宏观指令 JSON（分析输入）：`data/action_json/<matchup>/*.json`",
        "- 本报告审计对象：已放置的分层抽样 action JSON（每对局 40 局，seed=42）",
        "",
        "### 1.1 全量 raw_data（manifest）",
        "",
        f"| 项目 | 值 |",
        f"|---|---:|",
        f"| 唯一写入局数 | {raw.get('written')} |",
        f"| 跨 ZIP 重复跳过 | {raw.get('duplicate_skipped')} |",
        f"| 解压/分类解析失败 | {raw.get('parse_errors')} |",
        "",
        "对局分布：",
        "",
        "| Matchup | 局数 |",
        "|---|---:|",
    ]
    for k, v in sorted((raw.get("matchup_counts") or {}).items()):
        lines.append(f"| {k} | {v} |")

    lines += [
        "",
        "### 1.2 本次审计样本（action_json）",
        "",
        f"- JSON 文件数：{scope.get('json_files')}",
        f"- 有效 Replay：{scope.get('valid_replays')}",
        f"- 硬无效 Replay：{scope.get('invalid_replays')}",
        f"- Player 行数：{scope.get('player_rows')}",
        "",
        f"> {scope.get('note')}",
        "",
        "## 2. 基础合法性检查",
        "",
        "| 检查项 | 结果 |",
        "|---|---|",
        f"| `replay_id` 唯一 | "
        f"{'是' if replay_df['replay_id'].is_unique else '否（存在重复）'} |",
        f"| 恰好两名玩家 / 1v1 | 硬无效数 = {scope.get('invalid_replays')} |",
        f"| 种族 ∈ {{Terran,Protoss,Zerg}} | 见 issue 前缀计数 |",
        f"| 胜负互斥 | `result_ok` 为假的局数 = "
        f"{int((~replay_df['result_ok']).sum())} |",
        f"| tracker 可用 | 本批 action_json 均无 tracker（预期） |",
        "",
        "Issue 前缀计数（含软质量标签，不等于删除）：",
        "",
        "| 前缀 | 局数 |",
        "|---|---:|",
    ]
    for k, v in sorted((m.get("issue_prefix_counts") or {}).items(), key=lambda kv: -kv[1]):
        lines.append(f"| `{k}` | {v} |")

    lines += [
        "",
        "## 3. 样本量分布（有效局）",
        "",
        "### 3.1 Matchup",
        "",
        "| Matchup | n |",
        "|---|---:|",
    ]
    for k, v in sorted((samples.get("by_matchup_dir") or {}).items()):
        lines.append(f"| {k} | {v} |")

    lines += [
        "",
        "### 3.2 种族（玩家视角）",
        "",
        "| Race | n |",
        "|---|---:|",
    ]
    for k, v in sorted((samples.get("by_race_player") or {}).items()):
        lines.append(f"| {k} | {v} |")

    loc = samples.get("localized_race_raw_counts") or {}
    if loc:
        lines += [
            "",
            "原始 metadata 中出现本地化种族名（已归一）：",
            "",
            "| race_raw | n |",
            "|---|---:|",
        ]
        for k, v in sorted(loc.items(), key=lambda kv: -kv[1]):
            lines.append(f"| {k} | {v} |")

    lines += [
        "",
        "### 3.3 版本 / 地区",
        "",
        "| Version | n |",
        "|---|---:|",
    ]
    for k, v in sorted((samples.get("by_version") or {}).items(), key=lambda kv: -kv[1]):
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        "| Region | n |",
        "|---|---:|",
    ]
    for k, v in sorted((samples.get("by_region") or {}).items(), key=lambda kv: -kv[1]):
        lines.append(f"| {k} | {v} |")

    lines += [
        "",
        "## 4. 映射与宏观动作",
        "",
        f"- 宏观动作总数：{mapping.get('total_macro_actions')}",
        f"- 标准 Action 映射成功：{mapping.get('mapped_actions')} / "
        f"{(mapping.get('mapped_actions') or 0) + (mapping.get('unmapped_actions') or 0)} "
        f"（rate={fmt(mapping.get('mapping_rate'))}）",
        f"- 未映射：{mapping.get('unmapped_actions')}",
        f"- `standard_mapping_confidence < 0.90`：{mapping.get('low_confidence_events')}",
        f"- 缺少 `standard_result_name`：{mapping.get('missing_standard_result_name')}",
        "",
        "事件类别：",
        "",
        "| event | count |",
        "|---|---:|",
    ]
    for k, v in (mapping.get("event_category_totals") or {}).items():
        lines.append(f"| {k} | {v} |")

    lines += [
        "",
        "## 5. MMR",
        "",
        f"- 玩家侧缺失率：{fmt(mmr.get('missing_rate_player'))}",
        f"- 可用 MMR 数：{mmr.get('count')}",
        f"- 范围：min={fmt(mmr.get('min'), 1)}, p25={fmt(mmr.get('p25'), 1)}, "
        f"median={fmt(mmr.get('median'), 1)}, p75={fmt(mmr.get('p75'), 1)}, "
        f"max={fmt(mmr.get('max'), 1)}",
        f"- 合理区间设定：{mmr.get('reasonable_range')}",
        "",
        "## 6. Build Order 与时间尺度",
        "",
        f"- 至少一名玩家 BO 为空的局比例：{fmt(bo.get('replays_with_any_empty_player_bo'))}",
        f"- 双方 BO 皆空比例：{fmt(bo.get('replays_with_both_empty_bo'))}",
        f"- 严格重复事件数：{bo.get('strict_duplicate_events')}",
        f"- 时间非单调事件数：{bo.get('time_non_monotonic_events')}",
        f"- frame/second 不一致事件数：{bo.get('frame_second_mismatch_events')}",
        f"- `<60s` 短局标记：{bo.get('short_game_under_60_seconds')}",
        "",
        "### 时间尺度 ratio = max(BO second) / duration_seconds",
        "",
        f"- n={ts.get('n')}, median={fmt(ts.get('median'))}, "
        f"p25={fmt(ts.get('p25'))}, p75={fmt(ts.get('p75'))}",
        f"- 落在 1.30–1.50 的比例：{fmt(ts.get('fraction_in_1.30_1.50'))}",
        f"- 说明：{ts.get('interpretation')}",
        "",
        "## 7. 开局窗口可达性（游戏秒）",
        "",
        "| 窗口 | 可观察局数 |",
        "|---|---:|",
    ]
    for h in HORIZONS:
        lines.append(
            f"| 0–{h}s | {(m.get('opening_windows') or {}).get(f'observed_to_{h}')} |"
        )

    lines += [
        "",
        "## 8. 分析限制（必须写入后续报告）",
        "",
        "1. 本批 JSON 来自 `game.events` 命令意图，不是 tracker 完成确认。",
        "2. 不得把 `estimated_completion_second` 当作真实完成时间。",
        "3. `duration_seconds` 与 `build_order.second` 可能分属真实时间/游戏时间，"
        "开局截取必须统一使用游戏时间。",
        "4. 极短局可导致空 BO；属于对局本身，不是解析失败。",
        "5. 全量 10 万局尚未全部转成 action_json；策略发现前需扩大解析覆盖。",
        "",
        "## 9. 产出文件",
        "",
        "```text",
        "analysis/outputs/00_audit/data_quality_report.md",
        "analysis/outputs/00_audit/invalid_replays.csv",
        "analysis/outputs/00_audit/dataset_summary.json",
        "analysis/outputs/01_tables/replays.parquet",
        "analysis/outputs/01_tables/player_games.parquet",
        "```",
        "",
    ]
    out_md.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    root = repo_root()
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--action-json-root",
        type=Path,
        default=root / "data" / "action_json",
    )
    parser.add_argument(
        "--manifest",
        type=Path,
        default=root / "raw_data" / "manifest.json",
    )
    parser.add_argument(
        "--out-root",
        type=Path,
        default=root / "analysis" / "outputs",
    )
    args = parser.parse_args()

    audit_dir = args.out_root / "00_audit"
    tables_dir = args.out_root / "01_tables"
    audit_dir.mkdir(parents=True, exist_ok=True)
    tables_dir.mkdir(parents=True, exist_ok=True)

    files = iter_action_json(args.action_json_root)
    if not files:
        raise SystemExit(f"No action JSON found under {args.action_json_root}")

    replay_rows: list[dict[str, Any]] = []
    player_rows: list[dict[str, Any]] = []
    for matchup, path in files:
        rrow, prows, _ = audit_one(matchup, path)
        replay_rows.append(rrow)
        player_rows.extend(prows)

    replay_df = pd.DataFrame(replay_rows)
    player_df = pd.DataFrame(player_rows)

    # dedupe check / keep first
    dup_ids = replay_df["replay_id"][replay_df["replay_id"].duplicated()].tolist()
    if dup_ids:
        replay_df = replay_df.drop_duplicates(subset=["replay_id"], keep="first")
        player_df = player_df[
            player_df["replay_id"].isin(set(replay_df["replay_id"]))
        ].copy()

    manifest = load_manifest(args.manifest)
    summary = summarize(replay_df, player_df, manifest, args.action_json_root)
    summary["duplicate_replay_ids_in_sample"] = dup_ids

    replay_df.to_parquet(tables_dir / "replays.parquet", index=False)
    player_df.to_parquet(tables_dir / "player_games.parquet", index=False)

    invalid = replay_df.loc[~replay_df["valid"]].copy()
    # also export soft-flagged rows with issues for triage
    soft = replay_df.loc[replay_df["invalid_reasons"].fillna("") != ""].copy()
    soft.to_csv(audit_dir / "invalid_replays.csv", index=False)
    # keep hard-invalid list inside summary; CSV includes all issue-bearing rows

    (audit_dir / "dataset_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    render_report(summary, replay_df, audit_dir / "data_quality_report.md")

    print(f"audited={len(replay_df)} valid={int(replay_df['valid'].sum())}")
    print(f"hard_invalid={int((~replay_df['valid']).sum())} issue_rows={len(soft)}")
    print(f"wrote={audit_dir} and {tables_dir}")
    if dup_ids:
        print(f"warning: duplicate replay_ids in sample: {dup_ids}")


if __name__ == "__main__":
    main()
