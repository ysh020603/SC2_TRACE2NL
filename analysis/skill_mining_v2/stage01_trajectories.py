"""Stage 01 — build directional player trajectories from action_json."""

from __future__ import annotations

from collections import defaultdict
from typing import Any

import pandas as pd
from tqdm import tqdm

from analysis.skill_mining_v2.common.io import (
    dumps_actions,
    ensure_dir,
    filter_macro,
    iter_action_json_files,
    load_replay,
    write_json,
    write_parquet,
)
from analysis.skill_mining_v2.common.taxonomy import normalize_race
from analysis.skill_mining_v2.config import RACE_TO_CODE, PipelineConfig


def _result_to_is_win(result: Any) -> int | None:
    if result is None:
        return None
    s = str(result).lower()
    if s in {"win", "victory", "1"}:
        return 1
    if s in {"loss", "defeat", "0"}:
        return 0
    return None


def _directional(race: str, opp_race: str) -> str | None:
    a = RACE_TO_CODE.get(normalize_race(race) or race)
    b = RACE_TO_CODE.get(normalize_race(opp_race) or opp_race)
    if not a or not b:
        return None
    return f"{a}v{b}"


def run_stage01(cfg: PipelineConfig) -> pd.DataFrame:
    out_dir = ensure_dir(cfg.stage_dir(1, "01_trajectories"))
    out_path = out_dir / "player_trajectories.parquet"
    if cfg.resume and out_path.exists():
        print(f"[stage01] resume {out_path}", flush=True)
        return pd.read_parquet(out_path)

    wanted = set(cfg.matchups)
    # Only scan source dirs that can produce wanted directional matchups
    needed_dirs = set()
    reverse_src = {"TvP": "PvT", "ZvP": "PvZ", "ZvT": "TvZ"}
    for dm in wanted:
        if dm in {"PvP", "PvT", "PvZ", "TvT", "TvZ", "ZvZ"}:
            needed_dirs.add(dm)
        elif dm in reverse_src:
            needed_dirs.add(reverse_src[dm])
        else:
            needed_dirs.update({"PvP", "PvT", "PvZ", "TvT", "TvZ", "ZvZ"})

    rows: list[dict[str, Any]] = []
    per_matchup_counts: dict[str, int] = defaultdict(int)
    rng_limit = cfg.limit

    files = [
        (mu, p)
        for mu, p in iter_action_json_files(cfg.action_root)
        if mu in needed_dirs
    ]
    print(
        f"[stage01] scanning {len(files)} action_json files from {sorted(needed_dirs)}",
        flush=True,
    )

    for source_mu, path in tqdm(files, desc="stage01"):
        try:
            data = load_replay(path)
        except Exception:
            continue
        players = list(data.get("players") or [])
        if len(players) < 2:
            continue
        # build per-player macro BO
        by_id = {}
        for p in players:
            bo = filter_macro(list(p.get("build_order") or []))
            by_id[p.get("player_id")] = (p, bo)

        for p, own_actions in by_id.values():
            opp = next((x for x in players if x.get("player_id") != p.get("player_id")), None)
            if opp is None:
                continue
            race = normalize_race(p.get("race")) or p.get("race")
            opp_race = normalize_race(opp.get("race")) or opp.get("race")
            dmu = _directional(race, opp_race)
            if dmu is None or dmu not in wanted:
                continue
            if rng_limit is not None and per_matchup_counts[dmu] >= rng_limit:
                continue

            opp_actions = by_id[opp.get("player_id")][1]
            mmr = p.get("mmr") if p.get("mmr_available", True) else None
            opp_mmr = opp.get("mmr") if opp.get("mmr_available", True) else None
            try:
                mmr_f = float(mmr) if mmr is not None else None
            except (TypeError, ValueError):
                mmr_f = None
            try:
                opp_mmr_f = float(opp_mmr) if opp_mmr is not None else None
            except (TypeError, ValueError):
                opp_mmr_f = None

            is_win = _result_to_is_win(p.get("result"))
            if is_win is None:
                is_win = 1 if p.get("is_winner") else 0

            dq = data.get("data_quality") or {}
            rows.append(
                {
                    "run_id": cfg.run_id,
                    "replay_id": data.get("replay_id") or path.stem,
                    "player_id": p.get("player_id"),
                    "race": race,
                    "opponent_race": opp_race,
                    "directional_matchup": dmu,
                    "source_matchup_dir": source_mu,
                    "result": p.get("result"),
                    "is_win": int(is_win),
                    "mmr": mmr_f,
                    "opponent_mmr": opp_mmr_f,
                    "mmr_diff": None
                    if mmr_f is None or opp_mmr_f is None
                    else mmr_f - opp_mmr_f,
                    "map": data.get("map_name"),
                    "patch": data.get("version"),
                    "base_build": data.get("base_build"),
                    "region": data.get("region"),
                    "duration": data.get("duration_seconds"),
                    "own_actions": dumps_actions(own_actions),
                    "opponent_actions": dumps_actions(opp_actions),
                    "data_quality": str(dq.get("semantics") or dq.get("parse_mode") or ""),
                }
            )
            per_matchup_counts[dmu] += 1

        # early stop if all wanted matchups saturated
        if rng_limit is not None and all(per_matchup_counts[m] >= rng_limit for m in wanted):
            break

    df = pd.DataFrame(rows)
    write_parquet(df, out_path)
    summary = {
        "n_rows": int(len(df)),
        "per_matchup": {k: int(v) for k, v in sorted(per_matchup_counts.items())},
        "run_id": cfg.run_id,
    }
    write_json(out_dir / "trajectory_summary.json", summary)
    print(f"[stage01] wrote {len(df)} trajectories -> {out_path}", flush=True)
    return df
