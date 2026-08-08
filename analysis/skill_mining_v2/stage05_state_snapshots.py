"""Stage 05 — temporal strategic state snapshots."""

from __future__ import annotations

from typing import Any

import pandas as pd
from tqdm import tqdm

from analysis.skill_mining_v2.common.features import response_delta_features, state_features
from analysis.skill_mining_v2.common.io import ensure_dir, loads_actions, write_json
from analysis.skill_mining_v2.config import RESPONSE_DELTA, SNAPSHOT_TIMES, PipelineConfig


def run_stage05(cfg: PipelineConfig, traj: pd.DataFrame | None = None) -> pd.DataFrame:
    out_dir = ensure_dir(cfg.stage_dir(5, "05_snapshots"))
    out_path = out_dir / "snapshots.parquet"
    if cfg.resume and out_path.exists():
        print(f"[stage05] resume {out_path}", flush=True)
        return pd.read_parquet(out_path)

    if traj is None:
        traj = pd.read_parquet(cfg.stage_dir(1, "01_trajectories") / "player_trajectories.parquet")
    assign_path = cfg.stage_dir(4, "04_openings") / "opening_assignments.parquet"
    assigns = pd.read_parquet(assign_path)
    merged = traj.merge(
        assigns[
            [
                "replay_id",
                "player_id",
                "directional_matchup",
                "opening_id",
                "opening_window",
            ]
        ],
        on=["replay_id", "player_id", "directional_matchup"],
        how="inner",
    )
    # drop OTHER openings for evolution mining core path (keep for completeness optionally)
    merged = merged[~merged["opening_id"].astype(str).str.endswith("_OTHER")].reset_index(drop=True)

    selection_window = int(merged["opening_window"].mode().iloc[0]) if len(merged) else 300
    times = [t for t in SNAPSHOT_TIMES if t >= selection_window]
    if selection_window not in times:
        times = [selection_window] + times

    rows: list[dict[str, Any]] = []
    for _, r in tqdm(merged.iterrows(), total=len(merged), desc="stage05"):
        own = loads_actions(r["own_actions"])
        opp = loads_actions(r["opponent_actions"])
        duration = float(r["duration"] or 0)
        for t in times:
            if duration and duration + 30 < t:
                continue
            own_state = state_features(own, t)
            opp_state = state_features(opp, t)
            delta = response_delta_features(own, t, t + RESPONSE_DELTA)
            row = {
                "run_id": cfg.run_id,
                "replay_id": r["replay_id"],
                "player_id": r["player_id"],
                "directional_matchup": r["directional_matchup"],
                "race": r["race"],
                "opponent_race": r["opponent_race"],
                "opening_id": r["opening_id"],
                "t": t,
                "is_win": r["is_win"],
                "mmr_diff": r.get("mmr_diff"),
                "map": r.get("map"),
                "patch": r.get("patch"),
                "base_build": r.get("base_build"),
                "region": r.get("region"),
                "duration": r.get("duration"),
                "visibility": "oracle_trace",
                "early_loss_6m": int(r["is_win"] == 0 and float(r.get("duration") or 1e9) <= 360),
                "early_loss_8m": int(r["is_win"] == 0 and float(r.get("duration") or 1e9) <= 480),
                "early_loss_10m": int(r["is_win"] == 0 and float(r.get("duration") or 1e9) <= 600),
            }
            for k, v in own_state.items():
                row[f"own_{k}"] = v
            for k, v in opp_state.items():
                row[f"opp_{k}"] = v
            for k, v in delta.items():
                if k in {"top_actions"} or k.startswith("act_"):
                    row[f"resp_{k}"] = v
                else:
                    row[f"resp_{k}"] = v
            rows.append(row)

    df = pd.DataFrame(rows)
    df.to_parquet(out_path, index=False)
    write_json(
        out_dir / "snapshot_summary.json",
        {
            "n_rows": int(len(df)),
            "times": times,
            "n_replays": int(df[["replay_id", "player_id"]].drop_duplicates().shape[0]) if len(df) else 0,
            "run_id": cfg.run_id,
        },
    )
    print(f"[stage05] snapshots={len(df)} times={times}", flush=True)
    return df
