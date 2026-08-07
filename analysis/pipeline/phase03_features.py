"""Phase 3: opening feature engineering (plan.md §6)."""

from __future__ import annotations

import json
import math
from collections import Counter
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from analysis.pipeline.io_utils import HORIZONS, PRIMARY_HORIZON, ensure_dir, write_json
from analysis.pipeline.taxonomy import (
    BASES,
    COMBAT_FAMILY,
    GAS,
    PROD_BUILDINGS,
    STATIC_DEFENSE,
    SUPPLY,
    TECH_BUILDINGS,
    WORKERS,
    build_key_sequence,
    macro_category,
    result_name,
)

MILESTONES = [
    "first_gas",
    "second_gas",
    "first_prod_building",
    "second_prod_building",
    "third_prod_building",
    "second_base",
    "third_base",
    "first_tech_building",
    "second_tech_building",
    "first_combat_unit",
    "first_static_defense",
    "first_upgrade",
]

TECH_FLAGS_BY_RACE = {
    "Terran": [
        "path_rax_expand",
        "path_rax_factory",
        "path_factory_starport",
        "path_multi_rax",
        "path_multi_factory",
        "path_early_ebay",
        "path_early_armory",
        "path_onebase_tech",
    ],
    "Protoss": [
        "path_gate_expand",
        "path_gate_cyber",
        "path_forge_open",
        "path_twilight",
        "path_robotics",
        "path_stargate",
        "path_dark_shrine",
        "path_multi_gate",
        "path_onebase_tech",
    ],
    "Zerg": [
        "path_hatch_first",
        "path_pool_first",
        "path_gas_first",
        "path_roach_warren",
        "path_bane_nest",
        "path_lair",
        "path_spire",
        "path_multi_hatch",
        "path_low_eco_army",
    ],
}


def _first_time(events: list[dict[str, Any]], pred) -> float | None:
    times = []
    for ev in events:
        if pred(ev):
            sec = ev.get("second")
            if isinstance(sec, (int, float)):
                times.append(float(sec))
    return min(times) if times else None


def _nth_time(events: list[dict[str, Any]], pred, n: int) -> float | None:
    times = sorted(
        float(ev["second"])
        for ev in events
        if pred(ev) and isinstance(ev.get("second"), (int, float))
    )
    return times[n - 1] if len(times) >= n else None


def _count(events: list[dict[str, Any]], pred) -> int:
    return sum(1 for ev in events if pred(ev))


def _milestone_features(events: list[dict[str, Any]], horizon: int) -> dict[str, Any]:
    feats: dict[str, Any] = {}

    def set_ms(name: str, t: float | None) -> None:
        obs = t is not None and t <= horizon
        feats[f"{name}_observed"] = int(obs)
        feats[f"{name}_time"] = float(t) if obs else float(horizon)

    set_ms("first_gas", _first_time(events, lambda e: result_name(e) in GAS))
    set_ms("second_gas", _nth_time(events, lambda e: result_name(e) in GAS, 2))
    set_ms(
        "first_prod_building",
        _first_time(events, lambda e: result_name(e) in PROD_BUILDINGS),
    )
    set_ms(
        "second_prod_building",
        _nth_time(events, lambda e: result_name(e) in PROD_BUILDINGS, 2),
    )
    set_ms(
        "third_prod_building",
        _nth_time(events, lambda e: result_name(e) in PROD_BUILDINGS, 3),
    )
    # second/third base: Nexus/CC/Hatch beyond the first
    set_ms("second_base", _nth_time(events, lambda e: result_name(e) in BASES, 2))
    set_ms("third_base", _nth_time(events, lambda e: result_name(e) in BASES, 3))
    set_ms(
        "first_tech_building",
        _first_time(events, lambda e: result_name(e) in TECH_BUILDINGS),
    )
    set_ms(
        "second_tech_building",
        _nth_time(events, lambda e: result_name(e) in TECH_BUILDINGS, 2),
    )
    set_ms(
        "first_combat_unit",
        _first_time(
            events,
            lambda e: result_name(e) in COMBAT_FAMILY
            and result_name(e) not in WORKERS
            and result_name(e) != "Queen",
        ),
    )
    set_ms(
        "first_static_defense",
        _first_time(events, lambda e: result_name(e) in STATIC_DEFENSE),
    )
    set_ms("first_upgrade", _first_time(events, lambda e: e.get("event") == "upgrade_research"))
    return feats


def _count_features(events: list[dict[str, Any]], horizon: int) -> dict[str, Any]:
    clipped = [
        e
        for e in events
        if isinstance(e.get("second"), (int, float)) and float(e["second"]) <= horizon
    ]
    fam_counts: Counter[str] = Counter()
    for e in clipped:
        name = result_name(e)
        if name in COMBAT_FAMILY:
            fam_counts[COMBAT_FAMILY[name]] += 1

    return {
        f"ordered_worker_by_{horizon}": _count(clipped, lambda e: result_name(e) in WORKERS),
        f"ordered_base_by_{horizon}": _count(clipped, lambda e: result_name(e) in BASES),
        f"ordered_gas_by_{horizon}": _count(clipped, lambda e: result_name(e) in GAS),
        f"ordered_supply_by_{horizon}": _count(clipped, lambda e: result_name(e) in SUPPLY),
        f"ordered_prod_building_by_{horizon}": _count(
            clipped, lambda e: result_name(e) in PROD_BUILDINGS
        ),
        f"ordered_tech_building_by_{horizon}": _count(
            clipped, lambda e: result_name(e) in TECH_BUILDINGS
        ),
        f"ordered_static_by_{horizon}": _count(
            clipped, lambda e: result_name(e) in STATIC_DEFENSE
        ),
        f"ordered_upgrade_by_{horizon}": _count(
            clipped, lambda e: e.get("event") == "upgrade_research"
        ),
        f"ordered_macro_by_{horizon}": len(clipped),
        f"ordered_combat_bio_by_{horizon}": fam_counts.get("bio", 0)
        + fam_counts.get("gateway", 0)
        + fam_counts.get("ling_bane", 0),
        f"ordered_combat_factory_by_{horizon}": fam_counts.get("factory", 0)
        + fam_counts.get("robotics", 0)
        + fam_counts.get("roach", 0),
        f"ordered_combat_air_by_{horizon}": fam_counts.get("air", 0)
        + fam_counts.get("stargate", 0),
        f"ordered_combat_hydra_by_{horizon}": fam_counts.get("hydra", 0),
        f"ordered_queen_by_{horizon}": fam_counts.get("queen", 0),
    }


def _before(a: float | None, b: float | None) -> bool:
    return a is not None and b is not None and a < b


def _tech_path_flags(events: list[dict[str, Any]], race: str, horizon: int) -> dict[str, int]:
    clipped = [
        e
        for e in events
        if isinstance(e.get("second"), (int, float)) and float(e["second"]) <= horizon
    ]
    t = {name: _first_time(clipped, lambda e, n=name: result_name(e) == n) for name in set(
        list(PROD_BUILDINGS) + list(TECH_BUILDINGS) + list(BASES) + list(GAS) + ["SpawningPool"]
    )}
    flags = {k: 0 for k in TECH_FLAGS_BY_RACE.get(race, [])}
    second_base = _nth_time(clipped, lambda e: result_name(e) in BASES, 2)

    if race == "Terran":
        if _before(t.get("Barracks"), second_base) and second_base is not None:
            flags["path_rax_expand"] = 1
        if _before(t.get("Barracks"), t.get("Factory")):
            flags["path_rax_factory"] = 1
        if _before(t.get("Factory"), t.get("Starport")):
            flags["path_factory_starport"] = 1
        if _count(clipped, lambda e: result_name(e) == "Barracks") >= 2:
            flags["path_multi_rax"] = 1
        if _count(clipped, lambda e: result_name(e) == "Factory") >= 2:
            flags["path_multi_factory"] = 1
        if t.get("EngineeringBay") is not None and t["EngineeringBay"] <= 180:
            flags["path_early_ebay"] = 1
        if t.get("Armory") is not None and t["Armory"] <= 300:
            flags["path_early_armory"] = 1
        if second_base is None or second_base > 270:
            if _count(clipped, lambda e: result_name(e) in TECH_BUILDINGS) >= 1:
                flags["path_onebase_tech"] = 1

    elif race == "Protoss":
        if _before(t.get("Gateway"), second_base) and second_base is not None:
            flags["path_gate_expand"] = 1
        if _before(t.get("Gateway"), t.get("CyberneticsCore")):
            flags["path_gate_cyber"] = 1
        forge = t.get("Forge")
        gate = t.get("Gateway")
        if forge is not None and (gate is None or forge <= gate + 15):
            flags["path_forge_open"] = 1
        if t.get("TwilightCouncil") is not None:
            flags["path_twilight"] = 1
        if t.get("RoboticsFacility") is not None:
            flags["path_robotics"] = 1
        if t.get("Stargate") is not None:
            flags["path_stargate"] = 1
        if t.get("DarkShrine") is not None:
            flags["path_dark_shrine"] = 1
        if _count(clipped, lambda e: result_name(e) in {"Gateway", "WarpGate"}) >= 3:
            flags["path_multi_gate"] = 1
        if second_base is None or second_base > 270:
            if any(t.get(x) is not None for x in ("TwilightCouncil", "RoboticsFacility", "Stargate", "DarkShrine")):
                flags["path_onebase_tech"] = 1

    elif race == "Zerg":
        hatch2 = _nth_time(clipped, lambda e: result_name(e) == "Hatchery", 2)
        # first hatch is starting; hatch_first means second hatch before pool
        pool = t.get("SpawningPool")
        gas1 = _first_time(clipped, lambda e: result_name(e) in GAS)
        if hatch2 is not None and (pool is None or hatch2 < pool):
            flags["path_hatch_first"] = 1
        if pool is not None and (hatch2 is None or pool <= hatch2):
            flags["path_pool_first"] = 1
        if gas1 is not None and (pool is None or gas1 < pool) and (hatch2 is None or gas1 < hatch2):
            flags["path_gas_first"] = 1
        if t.get("RoachWarren") is not None:
            flags["path_roach_warren"] = 1
        if t.get("BanelingNest") is not None:
            flags["path_bane_nest"] = 1
        if t.get("Lair") is not None:
            flags["path_lair"] = 1
        if t.get("Spire") is not None:
            flags["path_spire"] = 1
        if _count(clipped, lambda e: result_name(e) == "Hatchery") >= 2:
            flags["path_multi_hatch"] = 1
        workers = _count(clipped, lambda e: result_name(e) in WORKERS)
        army = _count(clipped, lambda e: result_name(e) in COMBAT_FAMILY and result_name(e) != "Queen")
        if army >= 8 and workers <= 16:
            flags["path_low_eco_army"] = 1

    return flags


def _strategic_dims(ms: dict[str, Any], counts: dict[str, Any], horizon: int) -> dict[str, float]:
    # Higher = more of that dimension. Values roughly in [0, 1].
    h = float(horizon)

    def inv_time(obs_key: str, time_key: str, early: float, late: float) -> float:
        if not ms.get(obs_key):
            return 0.0
        t = float(ms[time_key])
        if t <= early:
            return 1.0
        if t >= late:
            return 0.15
        return max(0.15, 1.0 - (t - early) / (late - early))

    economy = 0.0
    economy += inv_time("second_base_observed", "second_base_time", 100, 280) * 0.45
    economy += min(1.0, counts.get(f"ordered_worker_by_{horizon}", 0) / 20.0) * 0.35
    economy += inv_time("second_gas_observed", "second_gas_time", 120, 300) * 0.20

    production = 0.0
    production += min(1.0, counts.get(f"ordered_prod_building_by_{horizon}", 0) / 4.0) * 0.5
    combat = (
        counts.get(f"ordered_combat_bio_by_{horizon}", 0)
        + counts.get(f"ordered_combat_factory_by_{horizon}", 0)
        + counts.get(f"ordered_combat_air_by_{horizon}", 0)
        + counts.get(f"ordered_combat_hydra_by_{horizon}", 0)
    )
    production += min(1.0, combat / 12.0) * 0.5

    tech = 0.0
    tech += inv_time("first_tech_building_observed", "first_tech_building_time", 80, 260) * 0.4
    tech += min(1.0, counts.get(f"ordered_tech_building_by_{horizon}", 0) / 3.0) * 0.35
    tech += min(1.0, counts.get(f"ordered_upgrade_by_{horizon}", 0) / 2.0) * 0.25

    gas = 0.0
    gas += inv_time("first_gas_observed", "first_gas_time", 50, 180) * 0.4
    gas += inv_time("second_gas_observed", "second_gas_time", 100, 280) * 0.3
    gas += min(1.0, counts.get(f"ordered_gas_by_{horizon}", 0) / 3.0) * 0.3

    static = 0.0
    static += inv_time("first_static_defense_observed", "first_static_defense_time", 60, 210) * 0.5
    static += min(1.0, counts.get(f"ordered_static_by_{horizon}", 0) / 3.0) * 0.5

    one_base = 0.0
    if not ms.get("second_base_observed") or float(ms.get("second_base_time", h)) > 270:
        one_base += 0.45
    one_base += min(1.0, counts.get(f"ordered_prod_building_by_{horizon}", 0) / 4.0) * 0.3
    one_base += tech * 0.25

    return {
        "idx_economy": round(economy, 4),
        "idx_production": round(production, 4),
        "idx_tech": round(tech, 4),
        "idx_gas": round(gas, 4),
        "idx_static_defense": round(static, 4),
        "idx_one_base": round(one_base, 4),
    }


def _ngrams(tokens: list[str], n: int) -> list[str]:
    if len(tokens) < n:
        return []
    return ["||".join(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]


def _robust_scale_within(df: pd.DataFrame, cols: list[str], group_cols: list[str]) -> pd.DataFrame:
    out = df.copy()
    for col in cols:
        if col not in out.columns:
            continue

        def _scale(s: pd.Series) -> pd.Series:
            med = s.median()
            q1 = s.quantile(0.25)
            q3 = s.quantile(0.75)
            iqr = q3 - q1
            if iqr == 0 or math.isnan(iqr):
                return s * 0.0
            return (s - med) / iqr

        out[f"{col}_z"] = out.groupby(group_cols, dropna=False)[col].transform(_scale)
    return out


def run_phase03(sequences_jsonl: Path, out_dir: Path, action_root: Path) -> dict[str, Any]:
    """Build feature tables. Reloads action JSON for raw BO access."""
    from analysis.pipeline.io_utils import iter_action_json, player_views

    ensure_dir(out_dir)
    # load sequences for key tokens / observed flags
    seq_index: dict[tuple[Any, Any], dict[str, Any]] = {}
    with sequences_jsonl.open(encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            seq_index[(rec["replay_id"], rec["player_id"])] = rec

    rows_by_h: dict[int, list[dict[str, Any]]] = {h: [] for h in HORIZONS}
    all_ngrams: Counter[str] = Counter()

    # first pass: collect ngrams on primary horizon for vocabulary
    primary_docs: list[tuple[tuple[Any, Any], list[str]]] = []

    for matchup_dir, _path, data in iter_action_json(action_root):
        for view in player_views(data, matchup_dir):
            key = (view["replay_id"], view["player_id"])
            seq_rec = seq_index.get(key)
            if seq_rec is None:
                continue
            bo = view["build_order"]
            race = view["race"]
            if race not in TECH_FLAGS_BY_RACE:
                continue

            for h in HORIZONS:
                hinfo = seq_rec["horizons"][str(h)]
                clipped = [
                    e
                    for e in bo
                    if isinstance(e.get("second"), (int, float)) and float(e["second"]) <= h
                ]
                ms = _milestone_features(clipped, h)
                counts = _count_features(bo, h)
                paths = _tech_path_flags(bo, race, h)
                dims = _strategic_dims(ms, counts, h)
                tokens = hinfo.get("key_sequence") or [
                    x["token"] for x in build_key_sequence(clipped)
                ]
                grams = _ngrams(tokens, 1) + _ngrams(tokens, 2) + _ngrams(tokens, 3)
                if h == PRIMARY_HORIZON:
                    primary_docs.append((key, grams))
                    all_ngrams.update(grams)

                row = {
                    "replay_id": view["replay_id"],
                    "player_id": view["player_id"],
                    "race": race,
                    "opponent_race": view["opponent_race"],
                    "matchup_dir": matchup_dir,
                    "result": view["result"],
                    "mmr": view["mmr"],
                    "mmr_diff": view["mmr_diff"],
                    "map_name": view["map_name"],
                    "version": view["version"],
                    "base_build": view["base_build"],
                    "region": view["region"],
                    "horizon": h,
                    "opening_observed_to": bool(hinfo["opening_observed_to"]),
                    "early_terminated": bool(hinfo["early_terminated"]),
                    "key_sequence": " > ".join(tokens[:40]),
                    **ms,
                    **counts,
                    **paths,
                    **dims,
                }
                rows_by_h[h].append(row)

    # top n-grams for primary horizon SVD-like binary features (hashing via top-K)
    top_grams = [g for g, _ in all_ngrams.most_common(80)]
    gram_to_idx = {g: i for i, g in enumerate(top_grams)}

    feature_dictionary = {
        "milestones": MILESTONES,
        "tech_flags_by_race": TECH_FLAGS_BY_RACE,
        "strategic_indices": [
            "idx_economy",
            "idx_production",
            "idx_tech",
            "idx_gas",
            "idx_static_defense",
            "idx_one_base",
        ],
        "primary_horizon": PRIMARY_HORIZON,
        "top_ngrams": top_grams,
        "notes": [
            "Times for unobserved milestones are censored at horizon; paired with *_observed.",
            "Indices are heuristic ordered-intent scores, not completed-economy metrics.",
            "N-gram features attached on all horizons using vocabulary from primary horizon.",
        ],
    }
    write_json(out_dir / "feature_dictionary.json", feature_dictionary)

    summaries = {}
    for h in HORIZONS:
        df = pd.DataFrame(rows_by_h[h])
        # attach ngram binary features using primary vocabulary; recompute grams per row
        gram_mat = np.zeros((len(df), len(top_grams)), dtype=np.float32)
        for i, row in enumerate(rows_by_h[h]):
            tokens = [t.strip() for t in (row.get("key_sequence") or "").split(">") if t.strip()]
            grams = set(_ngrams(tokens, 1) + _ngrams(tokens, 2) + _ngrams(tokens, 3))
            for g in grams:
                j = gram_to_idx.get(g)
                if j is not None:
                    gram_mat[i, j] = 1.0
        for j, g in enumerate(top_grams):
            col = f"ng_{j:03d}"
            df[col] = gram_mat[:, j]

        # robust scale continuous timing / indices within race × matchup × base_build
        cont_cols = [c for c in df.columns if c.endswith("_time") or c.startswith("idx_")]
        cont_cols += [c for c in df.columns if c.startswith("ordered_") and f"_{h}" in c]
        df = _robust_scale_within(
            df, cont_cols, ["race", "matchup_dir", "base_build"]
        )
        path = out_dir / f"features_{h}.parquet"
        df.to_parquet(path, index=False)
        summaries[str(h)] = {
            "rows": int(len(df)),
            "observed_rows": int(df["opening_observed_to"].sum()),
            "columns": int(df.shape[1]),
            "path": str(path),
        }

    summary = {"horizons": summaries, "ngram_vocab_size": len(top_grams)}
    write_json(out_dir / "phase03_summary.json", summary)
    return summary
