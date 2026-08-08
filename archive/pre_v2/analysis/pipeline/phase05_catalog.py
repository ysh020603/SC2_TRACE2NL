"""Phase 5: strategy cards and catalog (plan.md §9–10)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

from analysis.pipeline.io_utils import ensure_dir, write_json


def _level(v: float | None) -> str:
    if v is None:
        return "unknown"
    if v >= 0.66:
        return "high"
    if v >= 0.33:
        return "medium"
    return "low"


def _name_from_enrichment(race: str, enrich: list[dict[str, Any]], profile: dict[str, str]) -> str:
    feats = [e["feature"] for e in enrich[:6]]
    bits = []
    # economy
    if profile.get("one_base_commitment") == "high":
        bits.append("一矿")
    elif profile.get("economy") == "high":
        bits.append("快扩经济")
    else:
        bits.append("均衡经济")

    mapping = [
        ("path_forge_open", "早Forge"),
        ("path_twilight", "Twilight"),
        ("path_robotics", "Robotics"),
        ("path_stargate", "Stargate"),
        ("path_dark_shrine", "DarkShrine"),
        ("path_multi_gate", "多Gateway"),
        ("path_rax_factory", "Factory线"),
        ("path_factory_starport", "Starport线"),
        ("path_multi_rax", "多兵营"),
        ("path_early_ebay", "早EB"),
        ("path_hatch_first", "HatchFirst"),
        ("path_pool_first", "PoolFirst"),
        ("path_roach_warren", "Roach"),
        ("path_bane_nest", "LingBane"),
        ("path_lair", "Lair"),
        ("path_spire", "Spire"),
        ("first_static_defense_observed", "静态防御"),
        ("path_onebase_tech", "一矿科技"),
    ]
    for key, label in mapping:
        if key in feats and label not in bits:
            bits.append(label)
        if len(bits) >= 4:
            break

    if profile.get("production_commitment") == "high" and "高产能" not in bits:
        bits.append("高产能投入")
    elif profile.get("tech") == "high" and "科技向" not in bits:
        bits.append("科技向")

    name = "-".join(bits[:4])
    # rule checks: forbid unsupported Proxy/Rush wording
    forbidden = ["Proxy", "Rush", "Cannon Rush", "前置"]
    for f in forbidden:
        name = name.replace(f, "")
    return name or f"{race}开局簇"


def _validate_name(name: str, enrich: list[dict[str, Any]]) -> list[str]:
    warnings = []
    for bad in ("Proxy", "Rush", "Cannon Rush", "完成", "建成"):
        if bad in name:
            warnings.append(f"unsupported_term:{bad}")
    # if name mentions Forge, require enrichment or pass if string built from enrich
    return warnings


def run_phase05(
    features_path: Path,
    clusters_dir: Path,
    out_dir: Path,
) -> dict[str, Any]:
    ensure_dir(out_dir)
    review_dir = ensure_dir(out_dir / "manual_review_samples")

    feats = pd.read_parquet(features_path)
    global_df = pd.read_parquet(clusters_dir / "global_clusters.parquet")
    reps = json.loads((clusters_dir / "representative_build_orders.json").read_text(encoding="utf-8"))
    enrich_all = json.loads((clusters_dir / "feature_enrichment.json").read_text(encoding="utf-8"))

    # join indices from features
    key_cols = ["replay_id", "player_id"]
    idx_cols = [
        "idx_economy",
        "idx_production",
        "idx_tech",
        "idx_gas",
        "idx_static_defense",
        "idx_one_base",
        "key_sequence",
        "first_gas_time",
        "second_base_time",
        "first_prod_building_time",
        "first_tech_building_time",
        "first_combat_unit_time",
        "first_static_defense_time",
        "second_base_observed",
        "first_static_defense_observed",
    ]
    present = [c for c in idx_cols if c in feats.columns]
    merged = global_df.merge(
        feats[key_cols + present],
        on=key_cols,
        how="left",
        suffixes=("", "_feat"),
    )

    catalog = []
    md_lines = [
        "# 开局策略目录（Strategy Catalog）",
        "",
        "基于分层抽样 action_json（240 局）在 300 游戏秒窗口的探索性聚类。",
        "命令意图数据，非完成确认；命名避免 Proxy/Rush 等位置依赖措辞。",
        "",
    ]

    for sid, meta in sorted(reps.items()):
        race = meta["race"]
        members = merged.loc[merged["strategy_id"] == sid]
        if members.empty:
            continue
        profile = {
            "economy": _level(members["idx_economy"].mean() if "idx_economy" in members else None),
            "tech": _level(members["idx_tech"].mean() if "idx_tech" in members else None),
            "production_commitment": _level(
                members["idx_production"].mean() if "idx_production" in members else None
            ),
            "gas_commitment": _level(members["idx_gas"].mean() if "idx_gas" in members else None),
            "static_defense": _level(
                members["idx_static_defense"].mean() if "idx_static_defense" in members else None
            ),
            "one_base_commitment": _level(
                members["idx_one_base"].mean() if "idx_one_base" in members else None
            ),
        }
        enrich = meta.get("enriched_features") or enrich_all.get(race, {}).get(
            sid.split("-G")[-1].lstrip("0") or "0", []
        )
        # enrichment keyed by local cluster int in phase04
        if not enrich:
            # try lookup via local_cluster
            lc = members["local_cluster"].iloc[0]
            enrich = enrich_all.get(race, {}).get(str(int(lc)), [])

        name = _name_from_enrichment(str(race), enrich, profile)
        warnings = _validate_name(name, enrich)

        # core sequence from medoid
        med = next((r for r in meta.get("representatives", []) if r.get("is_medoid")), None)
        core_seq = []
        if med and med.get("key_sequence"):
            core_seq = [t.strip() for t in str(med["key_sequence"]).split(">") if t.strip()][:12]

        def med_time(col: str):
            if col not in members.columns:
                return None
            s = members[col].dropna()
            return float(s.median()) if len(s) else None

        card = {
            "strategy_id": sid,
            "race": race,
            "opponent_race": "ALL",
            "strategy_name": name,
            "sample_size": int(meta.get("sample_size") or len(members)),
            "prevalence": float(meta.get("prevalence") or 0.0),
            "cluster_confidence_mean": meta.get("stability"),
            "opening_horizon": 300,
            "core_sequence": core_seq,
            "milestone_median": {
                "first_gas": med_time("first_gas_time"),
                "second_base": med_time("second_base_time"),
                "first_prod_building": med_time("first_prod_building_time"),
                "first_tech_building": med_time("first_tech_building_time"),
                "first_combat_unit": med_time("first_combat_unit_time"),
                "first_static_defense": med_time("first_static_defense_time"),
            },
            "strategic_profile": profile,
            "enriched_features": enrich[:10],
            "representative_replays": meta.get("representatives", [])[:8],
            "name_validation_warnings": warnings,
            "data_limitations": [
                "building positions unavailable",
                "commands are ordered rather than confirmed completed",
                "sample is stratified 240 replays; prevalence not population-calibrated",
            ],
        }
        catalog.append(card)

        # manual review samples (up to 20)
        sample_dir = ensure_dir(review_dir / sid)
        # clear old
        for p in sample_dir.glob("*"):
            if p.is_file():
                p.unlink()
        review_list = []
        for r in meta.get("representatives", [])[:20]:
            review_list.append(r)
        write_json(sample_dir / "samples.json", review_list)

        md_lines += [
            f"## {sid} — {name}",
            "",
            f"- 种族：{race}",
            f"- 样本量：{card['sample_size']}（簇内占比 {card['prevalence']:.1%}）",
            f"- 稳定率：{card['cluster_confidence_mean']}",
            f"- 画像：经济={profile['economy']}, 科技={profile['tech']}, "
            f"产能={profile['production_commitment']}, 气矿={profile['gas_commitment']}, "
            f"静态防御={profile['static_defense']}, 一矿={profile['one_base_commitment']}",
            f"- 关键序列：{' → '.join(core_seq) if core_seq else 'n/a'}",
            "",
        ]
        if enrich:
            md_lines.append("富集特征：")
            md_lines.append("")
            for e in enrich[:6]:
                md_lines.append(
                    f"- `{e['feature']}`: 簇内 {e['cluster_rate']:.0%} / 基线 {e['baseline_rate']:.0%} "
                    f"(RR={e['risk_ratio']:.2f})"
                )
            md_lines.append("")

    write_json(out_dir / "strategy_catalog.json", catalog)
    (out_dir / "strategy_catalog.md").write_text("\n".join(md_lines), encoding="utf-8")

    summary = {"n_strategies": len(catalog), "strategy_ids": [c["strategy_id"] for c in catalog]}
    write_json(out_dir / "phase05_summary.json", summary)
    return summary
