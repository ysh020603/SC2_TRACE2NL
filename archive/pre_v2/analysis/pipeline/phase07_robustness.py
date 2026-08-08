"""Phase 7: robustness / stratified analyses (plan.md §14–15 / §21)."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from analysis.pipeline.io_utils import HORIZONS, ensure_dir, write_json


def _mmr_tier(mmr: float | None, edges: list[float]) -> str:
    if mmr is None or (isinstance(mmr, float) and np.isnan(mmr)):
        return "unknown"
    labels = ["Low", "Lower-middle", "Upper-middle", "High", "Elite"]
    for i, e in enumerate(edges):
        if mmr <= e:
            return labels[i]
    return labels[-1]


def run_phase07(
    features_dir: Path,
    clusters_dir: Path,
    matchups_dir: Path,
    out_dir: Path,
) -> dict[str, Any]:
    ensure_dir(out_dir)
    global_df = pd.read_parquet(clusters_dir / "global_clusters.parquet")
    feats300 = pd.read_parquet(features_dir / "features_300.parquet")
    pairs = pd.read_parquet(matchups_dir / "strategy_pairs.parquet")

    meta = feats300[
        ["replay_id", "player_id", "mmr", "map_name", "base_build", "version", "region", "result"]
    ].drop_duplicates()
    g = global_df.merge(meta, on=["replay_id", "player_id"], how="left", suffixes=("", "_y"))

    mmrs = g["mmr"].dropna().astype(float)
    if len(mmrs) >= 5:
        edges = [float(np.quantile(mmrs, q)) for q in (0.2, 0.4, 0.6, 0.8)]
    else:
        edges = [2000, 3000, 4000, 5000]
    g["mmr_tier"] = g["mmr"].apply(lambda x: _mmr_tier(None if pd.isna(x) else float(x), edges))

    # strategy usage by MMR tier
    mmr_rows = []
    for (race, sid, tier), sub in g.groupby(["race", "strategy_id", "mmr_tier"]):
        race_tier_n = len(g.loc[(g["race"] == race) & (g["mmr_tier"] == tier)])
        wins = (sub["result"] == "Win").sum() if "result" in sub else 0
        n = len(sub)
        mmr_rows.append(
            {
                "race": race,
                "strategy_id": sid,
                "mmr_tier": tier,
                "n": n,
                "usage_within_race_tier": n / race_tier_n if race_tier_n else None,
                "winrate": wins / n if n else None,
            }
        )
    mmr_df = pd.DataFrame(mmr_rows)
    mmr_df.to_csv(out_dir / "mmr_analysis.csv", index=False)

    # patch / version
    patch_rows = []
    for (race, sid, ver), sub in g.groupby(["race", "strategy_id", "version"]):
        race_ver_n = len(g.loc[(g["race"] == race) & (g["version"] == ver)])
        n = len(sub)
        wins = (sub["result"] == "Win").sum()
        patch_rows.append(
            {
                "race": race,
                "strategy_id": sid,
                "version": ver,
                "base_build": sub["base_build"].iloc[0] if len(sub) else None,
                "n": n,
                "usage_within_race_version": n / race_ver_n if race_ver_n else None,
                "winrate": wins / n if n else None,
            }
        )
    pd.DataFrame(patch_rows).to_csv(out_dir / "patch_analysis.csv", index=False)

    # map
    map_rows = []
    for (race, sid, mp), sub in g.groupby(["race", "strategy_id", "map_name"]):
        race_map_n = len(g.loc[(g["race"] == race) & (g["map_name"] == mp)])
        n = len(sub)
        wins = (sub["result"] == "Win").sum()
        map_rows.append(
            {
                "race": race,
                "strategy_id": sid,
                "map_name": mp,
                "n": n,
                "usage_within_race_map": n / race_map_n if race_map_n else None,
                "winrate": wins / n if n else None,
            }
        )
    pd.DataFrame(map_rows).to_csv(out_dir / "map_analysis.csv", index=False)

    # horizon consistency: compare strategy assignment stability across horizons via re-cluster proxy
    # Here: compare key strategic indices correlation for same players across horizons
    horizon_rows = []
    players = feats300[["replay_id", "player_id"]].drop_duplicates()
    for h in HORIZONS:
        fpath = features_dir / f"features_{h}.parquet"
        if not fpath.exists():
            continue
        fh = pd.read_parquet(fpath)
        obs = int(fh["opening_observed_to"].sum())
        horizon_rows.append(
            {
                "horizon": h,
                "rows": len(fh),
                "observed_rows": obs,
                "mean_idx_economy": float(fh.loc[fh["opening_observed_to"], "idx_economy"].mean())
                if obs
                else None,
                "mean_idx_one_base": float(fh.loc[fh["opening_observed_to"], "idx_one_base"].mean())
                if obs
                else None,
                "mean_idx_tech": float(fh.loc[fh["opening_observed_to"], "idx_tech"].mean())
                if obs
                else None,
            }
        )
    # player-level index correlation 210 vs 300 vs 420
    f210 = pd.read_parquet(features_dir / "features_210.parquet")
    f420 = pd.read_parquet(features_dir / "features_420.parquet")
    keys = ["replay_id", "player_id"]
    m = (
        f210[keys + ["idx_economy", "idx_tech", "idx_one_base", "opening_observed_to"]]
        .rename(
            columns={
                "idx_economy": "eco_210",
                "idx_tech": "tech_210",
                "idx_one_base": "onebase_210",
                "opening_observed_to": "obs_210",
            }
        )
        .merge(
            feats300[keys + ["idx_economy", "idx_tech", "idx_one_base", "opening_observed_to"]].rename(
                columns={
                    "idx_economy": "eco_300",
                    "idx_tech": "tech_300",
                    "idx_one_base": "onebase_300",
                    "opening_observed_to": "obs_300",
                }
            ),
            on=keys,
        )
        .merge(
            f420[keys + ["idx_economy", "idx_tech", "idx_one_base", "opening_observed_to"]].rename(
                columns={
                    "idx_economy": "eco_420",
                    "idx_tech": "tech_420",
                    "idx_one_base": "onebase_420",
                    "opening_observed_to": "obs_420",
                }
            ),
            on=keys,
        )
    )
    both = m.loc[m["obs_210"] & m["obs_300"] & m["obs_420"]]
    consistency = {
        "n_fully_observed_all_horizons": int(len(both)),
        "corr_economy_210_300": float(both["eco_210"].corr(both["eco_300"])) if len(both) > 2 else None,
        "corr_economy_300_420": float(both["eco_300"].corr(both["eco_420"])) if len(both) > 2 else None,
        "corr_tech_210_300": float(both["tech_210"].corr(both["tech_300"])) if len(both) > 2 else None,
        "corr_onebase_210_300": float(both["onebase_210"].corr(both["onebase_300"]))
        if len(both) > 2
        else None,
    }
    pd.DataFrame(horizon_rows).to_csv(out_dir / "horizon_consistency.csv", index=False)
    write_json(out_dir / "horizon_correlations.json", consistency)

    # early termination sensitivity: winrate among noise / early terminated
    early = feats300.loc[~feats300["opening_observed_to"]]
    early_sens = {
        "early_terminated_players": int(len(early)),
        "early_winrate": float((early["result"] == "Win").mean()) if len(early) else None,
        "full_obs_winrate": float(
            (feats300.loc[feats300["opening_observed_to"], "result"] == "Win").mean()
        ),
    }

    # counter stability across MMR for cells with n>=5 in each of two tiers
    if len(pairs):
        p = pairs.merge(
            g[["replay_id", "player_id", "mmr_tier"]].rename(
                columns={"player_id": "own_player_id", "mmr_tier": "own_mmr_tier"}
            ),
            on=["replay_id", "own_player_id"],
            how="left",
        )
        cell_tier = (
            p.groupby(["own_strategy", "opp_strategy", "own_mmr_tier"])
            .agg(n=("win", "size"), wr=("win", "mean"))
            .reset_index()
        )
        cell_tier.to_csv(out_dir / "counter_by_mmr_tier.csv", index=False)
    else:
        cell_tier = pd.DataFrame()

    report = [
        "# 稳健性报告（Phase 7）",
        "",
        "样本量来自 240 局分层抽样，本报告以探索性稳定性诊断为主。",
        "",
        "## MMR 分层边界",
        "",
        f"- 分位边界（20/40/60/80%）：{edges}",
        f"- 层级标签：Low / Lower-middle / Upper-middle / High / Elite",
        "",
        "## 开局窗口一致性",
        "",
        f"- 三窗口均可观察玩家数：{consistency.get('n_fully_observed_all_horizons')}",
        f"- 经济指数 corr(210,300)：{consistency.get('corr_economy_210_300')}",
        f"- 经济指数 corr(300,420)：{consistency.get('corr_economy_300_420')}",
        f"- 科技指数 corr(210,300)：{consistency.get('corr_tech_210_300')}",
        "",
        "## 快速结束敏感性",
        "",
        f"- 未观察满 300s 的玩家行：{early_sens['early_terminated_players']}",
        f"- 其胜率：{early_sens['early_winrate']}",
        f"- 完整观察组胜率：{early_sens['full_obs_winrate']}",
        "",
        "## 产出文件",
        "",
        "- `mmr_analysis.csv`",
        "- `patch_analysis.csv`",
        "- `map_analysis.csv`",
        "- `horizon_consistency.csv`",
        "- `counter_by_mmr_tier.csv`",
        "",
        "## 限制",
        "",
        "1. 小样本下跨地图/版本分层极易空单元格。",
        "2. 未宣称因果；仅报告关联与稳定性。",
        "3. 扩大到全量 action_json 后应重跑本阶段。",
        "",
    ]
    (out_dir / "robustness_report.md").write_text("\n".join(report), encoding="utf-8")

    summary = {
        "mmr_edges": edges,
        "horizon_consistency": consistency,
        "early_termination": early_sens,
        "mmr_rows": int(len(mmr_df)),
        "map_rows": int(len(map_rows)),
        "patch_rows": int(len(patch_rows)),
    }
    write_json(out_dir / "phase07_summary.json", summary)
    return summary
