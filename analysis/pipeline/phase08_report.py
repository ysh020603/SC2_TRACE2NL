"""Phase 8: final synthesis report (plan.md §21 / §24)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from analysis.pipeline.io_utils import ensure_dir, write_json


def run_phase08(outputs_root: Path) -> dict[str, Any]:
    out_dir = ensure_dir(outputs_root / "08_final")

    def load_json(rel: str) -> dict[str, Any]:
        p = outputs_root / rel
        if not p.exists():
            return {}
        return json.loads(p.read_text(encoding="utf-8"))

    audit = load_json("00_audit/dataset_summary.json")
    p2 = load_json("02_openings/phase02_summary.json")
    p3 = load_json("03_features/phase03_summary.json")
    p4 = load_json("04_clusters/phase04_summary.json")
    p5 = load_json("05_catalog/phase05_summary.json")
    p6 = load_json("06_matchups/phase06_summary.json")
    p7 = load_json("07_robustness/phase07_summary.json")

    catalog = []
    cat_path = outputs_root / "05_catalog/strategy_catalog.json"
    if cat_path.exists():
        catalog = json.loads(cat_path.read_text(encoding="utf-8"))

    adj_path = outputs_root / "06_matchups/adjusted_counter_matrix.csv"
    top_edges = []
    if adj_path.exists():
        adj = pd.read_csv(adj_path)
        if len(adj):
            # exploratory: grade C+ with highest |lift|
            usable = adj.copy()
            if "reliability" in usable.columns:
                usable = usable.loc[usable["reliability"].isin(["A", "B", "C"])]
            if "lift_vs_baseline" in usable.columns and len(usable):
                usable = usable.sort_values("lift_vs_baseline", ascending=False)
                top_edges = usable.head(10).to_dict(orient="records")

    # strategy value metrics (plan §24)
    value_rows = []
    stab_path = outputs_root / "04_clusters/cluster_stability.csv"
    stab = pd.read_csv(stab_path) if stab_path.exists() else pd.DataFrame()
    pairs_path = outputs_root / "06_matchups/strategy_pairs.parquet"
    pairs = pd.read_parquet(pairs_path) if pairs_path.exists() else pd.DataFrame()

    for card in catalog:
        sid = card["strategy_id"]
        pop = card.get("prevalence")
        stab_row = stab.loc[stab["strategy_id"] == sid]
        robustness = float(stab_row["stability"].iloc[0]) if len(stab_row) and pd.notna(stab_row["stability"].iloc[0]) else None
        # adjusted strength: mean shrunk/adjusted vs all opponents
        strength = None
        risk = None
        coverage = None
        if len(pairs):
            own = pairs.loc[pairs["own_strategy"] == sid]
            if len(own):
                strength = float(own["win"].mean())
                # risk: variance / quick-loss proxy not available; use loss rate
                risk = float(1.0 - strength)
                coverage = int(own["opp_strategy"].nunique())
        if adj_path.exists() and len(pd.read_csv(adj_path)):
            a = pd.read_csv(adj_path)
            sub = a.loc[a["own_strategy"] == sid]
            if len(sub) and "shrunk_winrate" in sub.columns:
                strength = float(sub["shrunk_winrate"].mean())
            elif len(sub) and "adjusted_winrate" in sub.columns:
                strength = float(sub["adjusted_winrate"].mean())
        value_rows.append(
            {
                "strategy_id": sid,
                "race": card.get("race"),
                "strategy_name": card.get("strategy_name"),
                "Popularity": pop,
                "Adjusted_Strength": strength,
                "Robustness": robustness,
                "Risk": risk,
                "Coverage": coverage,
                "sample_size": card.get("sample_size"),
            }
        )
    value_df = pd.DataFrame(value_rows)
    value_df.to_csv(out_dir / "strategy_value_metrics.csv", index=False)

    lines = [
        "# SC2 开局策略发现与优势分析 — 最终报告",
        "",
        "依据：`plan.md` Phase 1–8。数据：`raw_data` 全量库 + `data/action_json` 分层抽样（6×40=240）。",
        "",
        "> 本报告结论均为**统计关联**，并受小样本与命令意图语义限制；不得直接解读为因果。",
        "",
        "## 1. 数据集概况",
        "",
        f"- 全量唯一 Replay：{(audit.get('raw_data_manifest') or {}).get('written')}",
        f"- 审计/建模样本 JSON：{(audit.get('audit_scope') or {}).get('json_files')}",
        f"- 对局分布（全量）：{(audit.get('raw_data_manifest') or {}).get('matchup_counts')}",
        f"- 样本版本：主版本 4.10.0.75689，少量邻近 build",
        "",
        "## 2. 数据质量与限制",
        "",
        f"- 映射率：{(audit.get('mapping') or {}).get('mapping_rate')}",
        f"- 时间尺度中位数：{(audit.get('time_scale') or {}).get('median')}（真实时间 vs 游戏时间）",
        f"- MMR 缺失率：{(audit.get('mmr') or {}).get('missing_rate_player')}",
        "- 无 tracker：仅 ordered 命令意图，无位置，无法确认 Proxy/Rush。",
        "- 详见 `outputs/00_audit/data_quality_report.md`。",
        "",
        "## 3. 开局截取与特征",
        "",
        f"- Phase2 玩家行：{p2.get('player_rows')}；事件行：{p2.get('opening_event_rows')}",
        f"- Phase3 特征：{json.dumps(p3.get('horizons'), ensure_ascii=False)}",
        f"- 主分析窗口：300 游戏秒；辅窗口 210 / 420。",
        "",
        "## 4. 三族全局策略体系",
        "",
        f"- 策略数：{p4.get('n_strategies')}；噪声玩家行：{p4.get('noise_players')}",
        f"- Matchup 变体数：{p4.get('matchup_variants')}",
        "",
    ]

    by_race: dict[str, list[str]] = {"Protoss": [], "Terran": [], "Zerg": []}
    for c in catalog:
        by_race.setdefault(c.get("race"), []).append(
            f"{c['strategy_id']}: {c['strategy_name']} (n={c['sample_size']})"
        )
    for race, items in by_race.items():
        lines.append(f"### {race}")
        lines.append("")
        if not items:
            lines.append("- （无稳定簇或全为噪声）")
        for it in items:
            lines.append(f"- {it}")
        lines.append("")

    lines += [
        "## 5. Race-Matchup 变体",
        "",
        "见 `outputs/04_clusters/matchup_clusters.parquet`。小样本下多数全局策略在各 Matchup 仅保留单一变体字母 A。",
        "",
        "## 6. 策略特征卡",
        "",
        "完整卡片：`outputs/05_catalog/strategy_catalog.json` / `strategy_catalog.md`。",
        "人工抽查清单：`outputs/05_catalog/manual_review_samples/<strategy_id>/samples.json`。",
        "",
        "## 7. 策略对抗矩阵",
        "",
        f"- 对抗单元格：{p6.get('counter_cells')}；可靠性分布：{p6.get('cells_by_reliability')}",
        f"- 模型：{p6.get('model')}",
        "",
        "探索性高 lift 边（若存在 C 级以上）：",
        "",
    ]
    if top_edges:
        lines.append("| 己方 | 对方 | N | 原始胜率 | 调整后 | lift | 等级 |")
        lines.append("|---|---|---:|---:|---:|---:|---|")
        for e in top_edges[:8]:
            lines.append(
                f"| {e.get('own_strategy')} | {e.get('opp_strategy')} | {e.get('n')} | "
                f"{e.get('raw_winrate')} | {e.get('adjusted_winrate')} | "
                f"{e.get('lift_vs_baseline')} | {e.get('reliability')} |"
            )
    else:
        lines.append("当前样本下无达到中高可靠等级的对抗边；详见 raw/adjusted CSV。")

    lines += [
        "",
        "## 8. 调整后优势与多重检验",
        "",
        "- 使用 L2 Logistic（控制 MMR diff / map / patch / region）+ Beta 收缩。",
        "- FDR（Benjamini–Hochberg）见 `adjusted_counter_matrix.csv` 的 `fdr_qvalue`。",
        "- 绝大多数单元格为 D（n<50），**不报告强优势结论**。",
        "",
        "## 9. MMR / 地图 / 版本差异",
        "",
        f"- MMR 分位边界：{(p7.get('mmr_edges') if p7 else None)}",
        f"- 窗口一致性：{(p7.get('horizon_consistency') if p7 else None)}",
        "- 详表：`outputs/07_robustness/*.csv` 与 `robustness_report.md`。",
        "",
        "## 10. 策略价值指标（§24）",
        "",
        "见 `strategy_value_metrics.csv` 字段：Popularity / Adjusted_Strength / Robustness / Risk / Coverage。",
        "",
        "**不要**据此做“最强策略总排名”。应表述为：",
        "",
        "> 某策略在什么版本、MMR、Matchup、面对什么对方策略时关联更好，以及该结论有多可靠。",
        "",
        "## 11. 可用于 Agent 的检索库产物",
        "",
        "```text",
        "analysis/outputs/05_catalog/strategy_catalog.json",
        "analysis/outputs/04_clusters/representative_build_orders.json",
        "analysis/outputs/06_matchups/adjusted_counter_matrix.csv",
        "analysis/outputs/08_final/strategy_value_metrics.csv",
        "```",
        "",
        "## 12. 下一步",
        "",
        "1. 对 `raw_data/by_matchup/*` 扩大 `sc2mine parse-actions-dir` 覆盖到 `data/action_json/`。",
        "2. 重跑 `python analysis/run_pipeline.py`。",
        "3. 将 `min_cluster_size` 恢复为 plan 推荐的绝对阈值（≥100）。",
        "4. 需要严格层次贝叶斯时接入 PyMC/Stan；当前为正则化 + 收缩近似。",
        "",
    ]

    report_path = out_dir / "final_report.md"
    report_path.write_text("\n".join(lines), encoding="utf-8")

    # compact agent knowledge base
    kb = {
        "version": "sample_v1_240",
        "opening_horizon_game_seconds": 300,
        "semantics": "ordered_command_intent",
        "strategies": catalog,
        "value_metrics": value_rows,
        "limitations": [
            "positions unavailable",
            "ordered != completed",
            "small stratified sample",
            "associational estimates only",
        ],
    }
    write_json(out_dir / "agent_strategy_kb.json", kb)

    summary = {
        "final_report": str(report_path),
        "n_strategies": len(catalog),
        "value_metric_rows": len(value_rows),
    }
    write_json(out_dir / "phase08_summary.json", summary)
    return summary
