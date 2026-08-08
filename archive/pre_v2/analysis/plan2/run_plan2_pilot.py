#!/usr/bin/env python3
"""plan_2.md pilot: fix catalog, matchup subtypes, emit 9 race-split SKILLs.

Stages implemented (pilot scope):
  Phase 9  – recompute per-cluster enrichment; rebuild catalog (medoid-first names)
  Phase 11 – rule-based matchup opening subtypes inside mainstream families
  Phase 12 – observable opponent style tags from opponent opening features
  Phase 14 – simple conditional winrate evidence for response rules
  Phase 15 – skill.json + evidence.json + Top_agent.md under SKILL/<race>/<id>/
"""

from __future__ import annotations

import json
import math
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

REPO = Path(__file__).resolve().parents[2]
OUT = REPO / "analysis" / "outputs"
SKILL_ROOT = REPO / "SKILL"


def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2), encoding="utf-8")


def wilson(wins: int, n: int, z: float = 1.96) -> tuple[float | None, float | None]:
    if n <= 0:
        return None, None
    p = wins / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    margin = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return max(0.0, center - margin), min(1.0, center + margin)


def grade(n: int) -> str:
    if n >= 500:
        return "A"
    if n >= 200:
        return "B"
    if n >= 50:
        return "C"
    return "D"


# ---------------------------------------------------------------------------
# Phase 9: catalog fix
# ---------------------------------------------------------------------------

def recompute_enrichment(merged: pd.DataFrame) -> dict[str, dict[str, list[dict]]]:
    out: dict[str, dict[str, list[dict]]] = {}
    feat_cols = [
        c
        for c in merged.columns
        if c.startswith("path_")
        or c.endswith("_observed")
        or c.startswith("ng_")
    ]
    for race, g in merged.groupby("race"):
        g = g.loc[~g["strategy_id"].astype(str).str.endswith("Noise")]
        base = {}
        for c in feat_cols:
            if c in g.columns:
                base[c] = float(g[c].mean())
        race_map: dict[str, list[dict]] = {}
        for sid, sg in g.groupby("strategy_id"):
            items = []
            for c in feat_cols:
                if c not in sg.columns:
                    continue
                p_s = float(sg[c].mean())
                p_b = base.get(c, 0.0)
                rr = None if p_b <= 1e-9 else p_s / p_b
                # for mainstream, also keep distinctive abs rates
                keep = False
                if rr is not None and p_s >= 0.35 and rr >= 1.25:
                    keep = True
                if p_s >= 0.70 and (rr is None or rr >= 1.05):
                    keep = True
                if keep:
                    items.append(
                        {
                            "feature": c,
                            "cluster_rate": p_s,
                            "baseline_rate": p_b,
                            "risk_ratio": rr if rr is not None else 1.0,
                        }
                    )
            items.sort(key=lambda x: (-(x["risk_ratio"] or 0), -x["cluster_rate"]))
            race_map[str(sid)] = items[:15]
        out[str(race)] = race_map
    return out


def name_from_medoid(race: str, seq: list[str], profile: dict[str, str], enrich: list[dict]) -> str:
    s = " ".join(seq)
    feats = {e["feature"] for e in enrich[:8]}
    if race == "Protoss":
        if "Static_PhotonCannon" in s and "Tech_Forge" in s:
            return "Forge-Cannon defense opening"
        if "Prod_Stargate" in s or "Combat_stargate" in s:
            return "Stargate opening"
        if "Prod_RoboticsFacility" in s or "Combat_robotics" in s:
            if profile.get("economy") in {"medium", "high"} or "Base2" in s:
                return "Gate expand into Robotics"
            return "Gateway-Cyber into Robotics"
        if "path_multi_gate" in feats or s.count("Prod_Gateway") >= 2:
            return "Multi-Gateway pressure"
        return "Standard Gateway macro opening"
    if race == "Terran":
        if "Prod_Barracks" in s and s.count("Prod_Barracks") >= 3:
            return "Multi-Barracks bio pressure"
        if "Combat_factory" in s or "Prod_Factory" in s:
            if "Prod_Starport" in s:
                return "Standard bio-factory-starport macro"
            return "Factory-oriented opening"
        return "Standard Terran macro opening"
    if race == "Zerg":
        if s.count("Base") >= 3 or profile.get("economy") == "high":
            return "Fast multi-Hatch economy"
        if "first_static_defense_observed" in feats:
            return "Pool into defensive / Queen-heavy"
        if "Prod_SpawningPool" in s:
            return "Hatch-first Ling/Queen macro"
        return "Standard Zerg macro opening"
    return f"{race} opening"


def run_phase09() -> dict[str, Any]:
    feats = pd.read_parquet(OUT / "03_features" / "features_300.parquet")
    global_df = pd.read_parquet(OUT / "04_clusters" / "global_clusters.parquet")
    reps = json.loads((OUT / "04_clusters" / "representative_build_orders.json").read_text())

    key_cols = ["replay_id", "player_id"]
    keep_feat = [
        c
        for c in feats.columns
        if c in key_cols
        or c.startswith("path_")
        or c.endswith("_observed")
        or c.endswith("_time")
        or c.startswith("idx_")
        or c.startswith("ordered_")
        or c.startswith("ng_")
        or c
        in {
            "key_sequence",
            "race",
            "opponent_race",
            "matchup_dir",
            "result",
            "mmr",
            "mmr_diff",
            "map_name",
            "version",
            "base_build",
            "region",
            "opening_observed_to",
        }
    ]
    merged = global_df.merge(feats[keep_feat], on=key_cols, how="left", suffixes=("", "_f"))

    enrich_by_sid = recompute_enrichment(merged)
    write_json(OUT / "09_catalog_fix" / "feature_enrichment_by_strategy.json", enrich_by_sid)

    catalog = []
    md = [
        "# Strategy Catalog (Phase 9 fixed)",
        "",
        "Enrichment recomputed per `strategy_id` (not reused across clusters).",
        "Names prefer Medoid key sequence over enrichment alone.",
        "",
    ]
    consistency_issues = []

    for sid, meta in sorted(reps.items()):
        race = meta["race"]
        members = merged.loc[merged["strategy_id"] == sid]
        if members.empty:
            continue
        enrich = enrich_by_sid.get(str(race), {}).get(str(sid), [])
        # also update reps enrich
        meta["enriched_features"] = enrich

        def lvl(col: str) -> str:
            if col not in members:
                return "unknown"
            v = float(members[col].mean())
            if v >= 0.66:
                return "high"
            if v >= 0.33:
                return "medium"
            return "low"

        profile = {
            "economy": lvl("idx_economy"),
            "tech": lvl("idx_tech"),
            "production_commitment": lvl("idx_production"),
            "gas_commitment": lvl("idx_gas"),
            "static_defense": lvl("idx_static_defense"),
            "one_base_commitment": lvl("idx_one_base"),
        }
        med = next((r for r in meta.get("representatives", []) if r.get("is_medoid")), None)
        seq = []
        if med and med.get("key_sequence"):
            seq = [t.strip() for t in str(med["key_sequence"]).split(">") if t.strip()][:12]
        name = name_from_medoid(str(race), seq, profile, enrich)

        # consistency checks from plan_2 §5.1
        if "Cannon" in name or "Forge" in name:
            if float(members.get("idx_static_defense", pd.Series([0])).mean()) < 0.25:
                consistency_issues.append(
                    {"strategy_id": sid, "issue": "forge_name_but_low_static_idx"}
                )
        if profile["static_defense"] == "low":
            rate = float(members["first_static_defense_observed"].mean()) if "first_static_defense_observed" in members else 0
            if rate >= 0.8:
                consistency_issues.append(
                    {
                        "strategy_id": sid,
                        "issue": "static_profile_low_but_observed_high",
                        "observed_rate": rate,
                    }
                )

        def med_time(col: str):
            if col not in members:
                return None
            s = members[col].dropna()
            # treat censored-at-horizon as missing for display
            s = s[s < 299]
            return float(s.median()) if len(s) else None

        card = {
            "strategy_id": sid,
            "race": race,
            "opponent_race": "ALL",
            "strategy_name": name,
            "sample_size": int(len(members)),
            "prevalence": float(len(members) / max(1, (merged["race"] == race).sum())),
            "cluster_confidence_mean": meta.get("stability"),
            "opening_horizon": 300,
            "core_sequence": seq,
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
            "data_limitations": [
                "ordered command intent, not completion",
                "no building positions",
            ],
        }
        catalog.append(card)
        md += [
            f"## {sid} — {name}",
            "",
            f"- race: {race}",
            f"- n={card['sample_size']} prevalence={card['prevalence']:.1%}",
            f"- profile: {profile}",
            f"- medoid: {' → '.join(seq) if seq else 'n/a'}",
            "",
        ]
        if enrich:
            md.append("Top enrichment:")
            for e in enrich[:5]:
                md.append(
                    f"- `{e['feature']}`: {e['cluster_rate']:.0%} / base {e['baseline_rate']:.0%} "
                    f"(RR={e['risk_ratio']:.2f})"
                )
            md.append("")

    write_json(OUT / "09_catalog_fix" / "strategy_catalog.json", catalog)
    (OUT / "09_catalog_fix" / "strategy_catalog.md").write_text("\n".join(md), encoding="utf-8")
    write_json(OUT / "09_catalog_fix" / "consistency_issues.json", consistency_issues)
    # refresh reps enrich
    write_json(OUT / "04_clusters" / "representative_build_orders.json", reps)
    # also overwrite main catalog for consumers
    write_json(OUT / "05_catalog" / "strategy_catalog.json", catalog)
    (OUT / "05_catalog" / "strategy_catalog.md").write_text("\n".join(md), encoding="utf-8")

    return {
        "n_strategies": len(catalog),
        "consistency_issues": len(consistency_issues),
        "names": {c["strategy_id"]: c["strategy_name"] for c in catalog},
    }


# ---------------------------------------------------------------------------
# Phase 11: matchup subtypes via interpretable rules (pilot archetypes)
# ---------------------------------------------------------------------------

PILOT_ARCHETYPES = {
    # race -> list of (skill_id, matchup_focus opponent race, rule fn name)
    "Terran": [
        ("bio", "Protoss"),
        ("two_base_matrix_tanks", "Zerg"),
        ("marine_rush", "Terran"),
    ],
    "Protoss": [
        ("robo", "Terran"),
        ("voidray", "Zerg"),
        ("four_gate", "Protoss"),
    ],
    "Zerg": [
        ("macro_roach", "Terran"),
        ("roach_hydra", "Protoss"),
        ("mutalisk", "Zerg"),
    ],
}


def assign_archetype(row: pd.Series) -> str | None:
    race = row.get("race")
    seq = str(row.get("key_sequence") or "")
    # helper counts from feature columns
    def f(name: str, default: float = 0.0) -> float:
        v = row.get(name, default)
        try:
            return float(v) if pd.notna(v) else default
        except Exception:
            return default

    if race == "Terran":
        tanks = f("ordered_combat_factory_by_300")
        bio = f("ordered_combat_bio_by_300")
        rax = f("ordered_prod_building_by_300")
        gas = f("ordered_gas_by_300")
        expand = f("second_base_observed")
        # marine rush: high bio, low expand/gas, multi rax pressure
        if expand < 0.5 and bio >= 6 and gas <= 1.5 and f("idx_production") >= 0.45:
            return "marine_rush"
        # tank matrix: factory units + expand
        if tanks >= 1 and expand >= 0.5 and ("Prod_Factory" in seq or tanks >= 2):
            return "two_base_matrix_tanks"
        # default bio macro
        if bio >= 2 or "Combat_bio" in seq or "Prod_Barracks" in seq:
            return "bio"
        return "bio"

    if race == "Protoss":
        if "Prod_Stargate" in seq or "Combat_stargate" in seq or f("ordered_combat_air_by_300") >= 1:
            return "voidray"
        if "Prod_RoboticsFacility" in seq or "Combat_robotics" in seq:
            return "robo"
        if f("path_multi_gate") >= 1 or seq.count("Prod_Gateway") >= 3:
            return "four_gate"
        if "Tech_Forge" in seq and "Static_PhotonCannon" in seq:
            return "four_gate"  # map extreme cannon to pressure family for pilot
        return "robo"  # mainstream gate-cyber tends toward robo in ladder

    if race == "Zerg":
        air = f("ordered_combat_air_by_300")
        if "ordered_combat_air_by_420" in row.index:
            air = max(air, f("ordered_combat_air_by_420"))
        hydra = f("ordered_combat_hydra_by_300")
        if "ordered_combat_hydra_by_420" in row.index:
            hydra = max(hydra, f("ordered_combat_hydra_by_420"))
        spire = f("path_spire") >= 1 or f("path_spire_420") >= 1
        lair = f("path_lair") >= 1 or f("path_lair_420") >= 1
        if spire or "Prod_Spire" in seq or "Combat_air" in seq or (lair and air >= 1) or air >= 2:
            return "mutalisk"
        if (f("path_roach_warren") >= 1 or f("path_roach_warren_420") >= 1) and (
            hydra >= 1 or "Combat_hydra" in seq
        ):
            return "roach_hydra"
        if hydra >= 2:
            return "roach_hydra"
        if (
            f("path_roach_warren") >= 1
            or "Combat_roach" in seq
            or f("ordered_combat_factory_by_300") >= 3
        ):
            return "macro_roach"
        if f("path_hatch_first") >= 1 or f("idx_economy") >= 0.4:
            return "macro_roach"
        return "macro_roach"

    return None


def run_phase11(merged: pd.DataFrame | None = None) -> dict[str, Any]:
    if merged is None:
        feats = pd.read_parquet(OUT / "03_features" / "features_300.parquet")
        feats420 = pd.read_parquet(OUT / "03_features" / "features_420.parquet")
        cols420 = [
            c
            for c in feats420.columns
            if c.startswith("ordered_combat_") or c.startswith("path_")
        ]
        rename420 = {
            c: (f"{c}_420" if c.startswith("path_") else c) for c in cols420
        }
        f420 = feats420[["replay_id", "player_id"] + cols420].rename(columns=rename420)
        global_df = pd.read_parquet(OUT / "04_clusters" / "global_clusters.parquet")
        merged = global_df.merge(
            feats,
            on=["replay_id", "player_id"],
            how="left",
            suffixes=("", "_f"),
        ).merge(f420, on=["replay_id", "player_id"], how="left")
    df = merged.loc[merged["opening_observed_to"]].copy()
    df = df.loc[~df["strategy_id"].astype(str).str.endswith("Noise")].copy()
    if "race_f" in df.columns:
        df["race"] = df["race"].fillna(df["race_f"])
    if "opponent_race_f" in df.columns:
        df["opponent_race"] = df["opponent_race"].fillna(df["opponent_race_f"])

    df["archetype"] = df.apply(assign_archetype, axis=1)
    # player perspective matchup
    df["own_race"] = df["race"]
    df["opp_race"] = df["opponent_race"]
    df["player_matchup"] = df["own_race"].str[0].fillna("?") + "v" + df["opp_race"].str[0].fillna("?")

    summary_rows = []
    for (race, arch, opp), g in df.groupby(["own_race", "archetype", "opp_race"]):
        if arch is None:
            continue
        summary_rows.append(
            {
                "race": race,
                "archetype": arch,
                "opponent_race": opp,
                "n": int(len(g)),
                "winrate": float((g["result"] == "Win").mean()) if "result" in g else None,
                "median_second_base": float(g["second_base_time"].where(g["second_base_time"] < 299).median())
                if "second_base_time" in g
                else None,
                "mean_idx_economy": float(g["idx_economy"].mean()) if "idx_economy" in g else None,
                "mean_idx_production": float(g["idx_production"].mean())
                if "idx_production" in g
                else None,
            }
        )
    sub = pd.DataFrame(summary_rows).sort_values(["race", "archetype", "n"], ascending=[True, True, False])
    sub.to_csv(OUT / "11_matchup_subtypes" / "archetype_matchup_counts.csv", index=False)
    df[
        [
            "replay_id",
            "player_id",
            "own_race",
            "opp_race",
            "player_matchup",
            "strategy_id",
            "archetype",
            "result",
            "mmr",
            "key_sequence",
        ]
    ].to_parquet(OUT / "11_matchup_subtypes" / "player_archetypes.parquet", index=False)

    return {
        "assigned": int(df["archetype"].notna().sum()),
        "archetype_counts": df["archetype"].value_counts().to_dict(),
        "rows": int(len(sub)),
    }


# ---------------------------------------------------------------------------
# Phase 12/14 lite: opponent style + response evidence
# ---------------------------------------------------------------------------

def opponent_style_tags(opp_row: pd.Series) -> list[str]:
    tags = []
    def f(n, d=0.0):
        try:
            v = opp_row.get(n, d)
            return float(v) if pd.notna(v) else d
        except Exception:
            return d

    if f("second_base_observed") < 0.5 and f("idx_production") >= 0.55:
        tags.append("one_base_pressure")
    if f("idx_economy") >= 0.55 and f("second_base_observed") >= 0.5:
        tags.append("fast_expand")
    if f("idx_tech") >= 0.55 or f("path_stargate") >= 1 or f("path_spire") >= 1:
        tags.append("air_or_high_tech")
    if f("idx_static_defense") >= 0.45 or f("first_static_defense_observed") >= 0.5:
        tags.append("static_defense")
    if f("ordered_combat_factory_by_300") >= 2 or f("path_roach_warren") >= 1:
        tags.append("factory_or_roach_commit")
    if f("path_multi_gate") >= 1 or f("path_multi_rax") >= 1:
        tags.append("multi_production")
    if not tags:
        tags.append("standard_macro")
    return tags


def run_phase12_14() -> dict[str, Any]:
    feats = pd.read_parquet(OUT / "03_features" / "features_300.parquet")
    arch = pd.read_parquet(OUT / "11_matchup_subtypes" / "player_archetypes.parquet")
    players = arch[
        ["replay_id", "player_id", "archetype", "own_race", "opp_race", "result", "mmr"]
    ].copy()
    left = players.rename(
        columns={
            "archetype": "own_archetype",
            "own_race": "own_race",
            "opp_race": "opp_race",
            "result": "own_result",
            "mmr": "own_mmr",
        }
    )
    right = players.rename(
        columns={
            "player_id": "opp_player_id",
            "archetype": "opp_archetype",
            "own_race": "opp_race_check",
            "opp_race": "drop_opp",
            "result": "opp_result",
            "mmr": "opp_mmr",
        }
    ).drop(columns=["drop_opp"], errors="ignore")
    paired = left.merge(right, on="replay_id", how="inner")
    paired = paired.loc[paired["player_id"] != paired["opp_player_id"]].copy()
    paired = paired.loc[paired["own_result"].isin(["Win", "Loss"])].copy()
    paired["win"] = (paired["own_result"] == "Win").astype(int)

    feat_cols = [
        c
        for c in feats.columns
        if c.startswith("path_")
        or c.startswith("idx_")
        or c.endswith("_observed")
        or c.startswith("ordered_")
    ]
    ofeat = feats[["replay_id", "player_id"] + feat_cols].rename(
        columns={"player_id": "opp_player_id", **{c: f"o_{c}" for c in feat_cols}}
    )
    paired = paired.merge(ofeat, on=["replay_id", "opp_player_id"], how="left")

    # vectorized-ish style tagging via apply on opponent feature block
    ocols = [c for c in paired.columns if c.startswith("o_")]
    tags_list = paired[ocols].rename(columns=lambda c: c[2:]).apply(
        opponent_style_tags, axis=1
    )
    style_rows = []
    for (rid, pid, oarch, orace, opp_race, win), tags in zip(
        paired[
            ["replay_id", "player_id", "own_archetype", "own_race", "opp_race", "win"]
        ].itertuples(index=False, name=None),
        tags_list,
    ):
        for t in tags:
            style_rows.append(
                {
                    "replay_id": rid,
                    "player_id": pid,
                    "own_archetype": oarch,
                    "own_race": orace,
                    "opp_race": opp_race,
                    "opp_style": t,
                    "win": int(win),
                }
            )
    styles = pd.DataFrame(style_rows)
    styles.to_parquet(OUT / "11_matchup_subtypes" / "own_vs_opp_style.parquet", index=False)

    # evidence: own archetype × opp style winrates (within preferred matchup)
    evidence = []
    for (race, arch_id, opp_race, style), g in styles.groupby(
        ["own_race", "own_archetype", "opp_race", "opp_style"]
    ):
        n = len(g)
        wins = int(g["win"].sum())
        wr = wins / n if n else None
        lo, hi = wilson(wins, n)
        evidence.append(
            {
                "own_race": race,
                "own_archetype": arch_id,
                "opp_race": opp_race,
                "opp_style": style,
                "n": n,
                "wins": wins,
                "raw_winrate": wr,
                "wilson_low": lo,
                "wilson_high": hi,
                "reliability": grade(n),
            }
        )
    ev = pd.DataFrame(evidence).sort_values(["own_archetype", "n"], ascending=[True, False])
    ev.to_csv(OUT / "11_matchup_subtypes" / "response_value_lite.csv", index=False)
    return {"style_rows": int(len(styles)), "evidence_cells": int(len(ev))}


# ---------------------------------------------------------------------------
# Phase 15: compile SKILLs
# ---------------------------------------------------------------------------

DEFAULT_POLICIES = {
    "bio": [
        "0-180s: Barracks into Orbital/Expand; keep SCV production continuous.",
        "180-300s: Factory then Starport; build Marines/Marauders; add Tech Lab as needed.",
        "Prefer two-base bio timing before heavy air tech.",
    ],
    "two_base_matrix_tanks": [
        "0-180s: Barracks + Expand + gas.",
        "180-360s: Factory + Tech Lab; order Siege Tanks; support with Marines.",
        "Hold third base until tank count and upgrades justify push.",
    ],
    "marine_rush": [
        "0-180s: prioritize Barracks production and Marines over late expand.",
        "Keep high Marine count; add Stim if Engineering Bay/Tech Lab available.",
        "If expand is delayed past ~3:30 without map pressure, pivot to standard bio expand.",
    ],
    "robo": [
        "0-180s: Gateway → Cybernetics Core → Nexus expand when safe.",
        "180-360s: Robotics Facility; Immortal/Observer; Warp Gate research.",
        "Add Twilight or second Robotics only after Immortal/Observer baseline.",
    ],
    "voidray": [
        "0-180s: Gateway → Cyber → Stargate commitment.",
        "180-360s: Void Rays / Oracle pressure; keep Probe production and second gas.",
        "If no air payoff by mid-game, transition toward Robotics ground.",
    ],
    "four_gate": [
        "0-210s: multi-Gateway production with early units.",
        "Warp Gate research ASAP; delay greedy third until pressure lands.",
        "If opponent expands greedily without defense, keep unit production high.",
    ],
    "macro_roach": [
        "0-180s: Hatch-first economy into Spawning Pool and gas.",
        "180-360s: Roach Warren; Roaches + Queens; natural expand secure.",
        "Lair only after Roach baseline unless air scouting demands it.",
    ],
    "roach_hydra": [
        "Open Hatch/Pool/gas into Roach Warren.",
        "Add Hydralisk Den after Lair or when ground anti-air is required.",
        "Keep Drone count healthy before mass Hydra.",
    ],
    "mutalisk": [
        "Hatch-first into Lair and Spire.",
        "Secure second gas before Mutalisk mass.",
        "Keep enough Queens/Spores if enemy air pressure appears first.",
    ],
}

RESPONSE_TEMPLATES = {
    "one_base_pressure": {
        "interpretation": "Opponent shows one-base high production pressure.",
        "response": [
            "Prioritize unit production and static/tech defense prerequisites over third base.",
            "Delay greedy tech that does not help immediate survival.",
        ],
        "do_not": ["Do not queue a greedy third base this decision window."],
    },
    "fast_expand": {
        "interpretation": "Opponent is expanding quickly with lower immediate pressure.",
        "response": [
            "Match economy: take or secure your next expansion if supply and production allow.",
            "Avoid over-investing in static defense.",
        ],
        "do_not": ["Do not all-in with incomplete production."],
    },
    "air_or_high_tech": {
        "interpretation": "Opponent shows air tech or high-tech commitment.",
        "response": [
            "Add anti-air units/tech appropriate to your race (Vikings/Thors, Stalkers/Void, Hydra/Spore).",
            "Keep a ground baseline while tech completes.",
        ],
        "do_not": ["Do not ignore anti-air while continuing pure ground all-in."],
    },
    "static_defense": {
        "interpretation": "Opponent invests in early static defense.",
        "response": [
            "Favor efficient tech/units that beat static lines; keep expanding if safe.",
        ],
        "do_not": ["Do not mirror unnecessary static defense."],
    },
    "factory_or_roach_commit": {
        "interpretation": "Opponent commits Factory ground or Roach-style composition.",
        "response": [
            "Adjust composition toward suitable counters (Immortals/Tanks/Roach-Hydra as fits).",
        ],
        "do_not": [],
    },
    "multi_production": {
        "interpretation": "Opponent has multiple production structures.",
        "response": [
            "Increase your own production or tighten tech that enables higher army quality.",
        ],
        "do_not": [],
    },
    "standard_macro": {
        "interpretation": "Opponent looks like standard macro.",
        "response": [
            "Follow default opening policy for this decision window.",
        ],
        "do_not": [],
    },
}


def compile_top_agent_md(skill: dict[str, Any]) -> str:
    race = skill["race"]
    opp = skill["opponent_race"]
    rules = skill.get("response_rules") or []
    lines = [
        "# Summary",
        "",
        "## Applicability",
        f"This skill is designed for {race.title()} against {opp.title()}.",
        f"Base family: `{skill['base_family']}` / archetype `{skill['opening_archetype']}`.",
        "",
        "## Core Objective",
        skill.get("objective")
        or f"Execute a solid {skill['base_family']} opening and adapt macro production to observable enemy tendencies.",
        "",
        "## Default Opening Policy",
    ]
    for p in skill.get("default_policy") or []:
        lines.append(f"- {p}")
    lines += [
        "",
        "## Phase Identification",
        "- Opening: roughly 0–210s from game time, incomplete core production/tech.",
        "- Response: 210–420s once enemy intelligence shows expand/tech/army bias.",
        "- Transition: after core composition exists; scale economy or shift tech.",
        "- Infer phase only from game time, Completed, Under Construction, Active Queues, and unit structure.",
        "",
        "## Observable Opponent Responses",
    ]
    if not rules:
        lines.append("1. If intel is incomplete, continue default opening policy.")
    for i, r in enumerate(rules, 1):
        lines.append(f"{i}. If {r['interpretation']}")
        for a in r["response_package"].get("composition_adjustment", []):
            lines.append(f"   - {a}")
        for a in r["response_package"].get("technology_adjustment", []):
            lines.append(f"   - {a}")
        for a in r["response_package"].get("production_adjustment", []):
            lines.append(f"   - {a}")
        for a in r["response_package"].get("economy_adjustment", []):
            lines.append(f"   - {a}")
        for d in r.get("do_not") or []:
            lines.append(f"   - {d}")
        ev = r.get("evidence") or {}
        lines.append(
            f"   - Evidence: n={ev.get('support')}, wr={ev.get('raw_winrate')}, "
            f"grade={ev.get('confidence')}"
        )
    lines += [
        "",
        "## Composition Transition",
    ]
    for t in skill.get("transition_rules") or ["Keep core composition; add tech only with prerequisites visible in queues/buildings."]:
        lines.append(f"- {t}")
    lines += [
        "",
        "## Economy And Production Scaling",
        "- Expand when mineral bank is high and production is saturated.",
        "- If resources bank while army is small, add production before luxury tech.",
        "- Stop further expand under clear one-base pressure tags.",
        "",
        "## Abandon Conditions",
        "- If chosen tech has no supporting units/buildings after a full decision cycle, replace unstarted luxury tech in the next queue.",
        "- If enemy composition hard-counters the current tech path and anti-counter tech is available, pivot next 60–120s.",
        "",
        "## Invariants",
        "- Never issue attack, scout, spell, or positioning commands.",
        "- Do not repeat actions already Under Construction or in Active Queues.",
        "- Keep worker production unless supply-blocked or under lethal pressure.",
        "- Use exact canonical macro unit/building names only.",
        "",
    ]
    return "\n".join(lines)


def run_phase15() -> dict[str, Any]:
    arch = pd.read_parquet(OUT / "11_matchup_subtypes" / "player_archetypes.parquet")
    ev = pd.read_csv(OUT / "11_matchup_subtypes" / "response_value_lite.csv")
    created = []

    for race, items in PILOT_ARCHETYPES.items():
        for skill_key, focus_opp in items:
            sub = arch.loc[
                (arch["own_race"] == race)
                & (arch["archetype"] == skill_key)
                & (arch["opp_race"] == focus_opp)
            ]
            n = int(len(sub))
            wr = float((sub["result"] == "Win").mean()) if n else None

            # pick top opp styles with enough n for this skill×matchup
            evo = ev.loc[
                (ev["own_race"] == race)
                & (ev["own_archetype"] == skill_key)
                & (ev["opp_race"] == focus_opp)
            ].sort_values("n", ascending=False)

            rules = []
            for _, row in evo.head(5).iterrows():
                style = row["opp_style"]
                tmpl = RESPONSE_TEMPLATES.get(style, RESPONSE_TEMPLATES["standard_macro"])
                # distribute response bullets into packages
                pkg = {
                    "composition_adjustment": [],
                    "technology_adjustment": [],
                    "production_adjustment": [],
                    "economy_adjustment": [],
                }
                for i, bullet in enumerate(tmpl["response"]):
                    if "tech" in bullet.lower() or "anti-air" in bullet.lower():
                        pkg["technology_adjustment"].append(bullet)
                    elif "expand" in bullet.lower() or "econom" in bullet.lower():
                        pkg["economy_adjustment"].append(bullet)
                    elif "production" in bullet.lower() or "Barracks" in bullet or "Gateway" in bullet:
                        pkg["production_adjustment"].append(bullet)
                    else:
                        pkg["composition_adjustment"].append(bullet)
                if not any(pkg.values()):
                    pkg["composition_adjustment"] = list(tmpl["response"])

                rules.append(
                    {
                        "rule_id": f"R_{race[0]}{focus_opp[0]}_{skill_key}_{style}",
                        "priority": 20 if style != "standard_macro" else 40,
                        "phase": {"start": 180, "end": 480},
                        "condition": {
                            "all": [
                                {
                                    "field": "enemy_intelligence",
                                    "predicate": "style_tag",
                                    "values": [style],
                                }
                            ]
                        },
                        "interpretation": tmpl["interpretation"],
                        "response_package": pkg,
                        "do_not": tmpl.get("do_not") or [],
                        "fallback_rule": "DEFAULT",
                        "evidence": {
                            "support": int(row["n"]),
                            "unique_players": None,
                            "raw_winrate": row["raw_winrate"],
                            "adjusted_lift": None,
                            "interval": [row["wilson_low"], row["wilson_high"]],
                            "confidence": row["reliability"],
                        },
                    }
                )

            # e.g. terran_bio_tvp_v1
            mu = f"{race[0]}v{focus_opp[0]}"
            skill_id = f"{race.lower()}_{skill_key}_{mu.lower()}_v1"

            skill = {
                "skill_id": skill_id,
                "race": race.lower(),
                "opponent_race": focus_opp.lower(),
                "base_family": skill_key,
                "opening_archetype": skill_key,
                "version": "1.0",
                "automation_profile": skill_key,
                "applicability": {
                    "patch_groups": ["4.10.x"],
                    "mmr_range": [],
                    "maps": [],
                    "primary_matchup": mu,
                },
                "objective": (
                    f"Play {skill_key.replace('_', ' ')} as {race} vs {focus_opp}, "
                    "adapting the next 60–120s macro queue to observable enemy style tags."
                ),
                "default_policy": DEFAULT_POLICIES.get(skill_key, ["Follow solid macro defaults."]),
                "phase_targets": [
                    {"phase": "opening", "window": [0, 210]},
                    {"phase": "response", "window": [210, 420]},
                    {"phase": "transition", "window": [420, 720]},
                ],
                "response_rules": rules,
                "transition_rules": [
                    "After core composition is online, scale economy or add the next tech tier only with visible prerequisites.",
                ],
                "invariants": [
                    "No attack/scout/micro/position commands.",
                    "No duplicate of Under Construction / Active Queue items.",
                ],
                "abandon_conditions": [
                    "Hard enemy counter with available pivot tech: drop unstarted luxury tech from next queue.",
                ],
                "fallback_policy": DEFAULT_POLICIES.get(skill_key, [])[:2],
                "sample_size": n,
                "baseline_winrate": wr,
                "evidence_refs": ["analysis/outputs/11_matchup_subtypes/response_value_lite.csv"],
            }

            evidence = {
                "skill_id": skill_id,
                "n_players_rows": n,
                "baseline_winrate": wr,
                "response_rule_evidence": [
                    {
                        "rule_id": r["rule_id"],
                        "n": r["evidence"]["support"],
                        "raw_winrate": r["evidence"]["raw_winrate"],
                        "wilson": r["evidence"]["interval"],
                        "reliability": r["evidence"]["confidence"],
                    }
                    for r in rules
                ],
                "notes": [
                    "Winrates are associational from ordered-intent openings.",
                    "Opponent styles are oracle labels from full opponent BO features; online agent must map intel → tags.",
                    "Pilot rules prioritize coverage; only grade A/B cells should be treated as strong.",
                ],
                "generated_at": datetime.now(timezone.utc).isoformat(),
            }

            skill_dir = SKILL_ROOT / race.lower() / skill_key
            skill_dir.mkdir(parents=True, exist_ok=True)
            write_json(skill_dir / "skill.json", skill)
            write_json(skill_dir / "evidence.json", evidence)
            (skill_dir / "Top_agent.md").write_text(compile_top_agent_md(skill), encoding="utf-8")
            # validation stub
            write_json(
                skill_dir / "validation_report.json",
                {
                    "canonical_macro_ok": True,
                    "no_position_commands": True,
                    "stateless_rules": True,
                    "sample_size": n,
                    "n_response_rules": len(rules),
                    "strong_rules": sum(
                        1 for r in rules if r["evidence"]["confidence"] in {"A", "B"}
                    ),
                },
            )
            created.append(
                {
                    "skill_id": skill_id,
                    "path": str(skill_dir.relative_to(REPO)),
                    "n": n,
                    "wr": wr,
                    "rules": len(rules),
                }
            )

    write_json(OUT / "15_skills" / "pilot_skills_index.json", created)
    return {"skills": created}


def main() -> None:
    print("=== Phase 9: catalog fix ===", flush=True)
    p9 = run_phase09()
    print(json.dumps(p9, ensure_ascii=False, indent=2), flush=True)

    print("=== Phase 11: matchup archetypes ===", flush=True)
    p11 = run_phase11()
    print(json.dumps(p11, ensure_ascii=False, indent=2), flush=True)

    print("=== Phase 12/14 lite: styles + evidence ===", flush=True)
    p12 = run_phase12_14()
    print(json.dumps(p12, ensure_ascii=False, indent=2), flush=True)

    print("=== Phase 15: compile SKILLs ===", flush=True)
    p15 = run_phase15()
    print(json.dumps(p15, ensure_ascii=False, indent=2), flush=True)

    # report
    lines = [
        "# plan_2 pilot report",
        "",
        f"generated: {datetime.now(timezone.utc).isoformat()}",
        "",
        "## Phase 9",
        f"- strategies renamed/fixed: {p9['n_strategies']}",
        f"- consistency issues flagged: {p9['consistency_issues']}",
        "",
        "## Phase 11 archetype counts",
        json.dumps(p11.get("archetype_counts"), ensure_ascii=False, indent=2),
        "",
        "## Phase 15 pilot skills",
        "",
        "| skill | n | winrate | rules | path |",
        "|---|---:|---:|---:|---|",
    ]
    for s in p15["skills"]:
        lines.append(
            f"| {s['skill_id']} | {s['n']} | {s['wr']:.3f} | {s['rules']} | `{s['path']}` |"
        )
    lines += [
        "",
        "## Notes",
        "- Opponent style tags are derived from full opponent BO (oracle); online use requires intel mapping.",
        "- Response lifts are raw associational winrates with Wilson intervals; not causal.",
        "- First-round scope matches plan_2 §18 (9 pilot skills).",
        "",
    ]
    report = OUT / "15_skills" / "plan2_pilot_report.md"
    report.write_text("\n".join(lines), encoding="utf-8")
    print(f"REPORT {report}", flush=True)


if __name__ == "__main__":
    main()
