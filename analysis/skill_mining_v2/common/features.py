"""Feature engineering for skill_mining_v2 (ordered_* semantics, no completed metrics)."""

from __future__ import annotations

import math
from collections import Counter
from typing import Any

import numpy as np
import pandas as pd

from analysis.skill_mining_v2.common.taxonomy import (
    BASES,
    COMBAT_FAMILY,
    GAS,
    PROD_BUILDINGS,
    STATIC_DEFENSE,
    SUPPLY,
    TECH_BUILDINGS,
    WORKERS,
    build_key_sequence,
    investment_bucket,
    is_macro_event,
    result_name,
)

TOP_NGRAM_VOCAB = 80
INVESTMENT_BUCKETS = (
    "economy",
    "production",
    "technology",
    "ground",
    "air",
    "defense",
    "upgrade",
    "expansion",
)


def clip_actions(actions: list[dict[str, Any]], t_max: float) -> list[dict[str, Any]]:
    return [
        ev
        for ev in actions
        if is_macro_event(ev)
        and isinstance(ev.get("second"), (int, float))
        and float(ev["second"]) <= t_max
    ]


def actions_in_window(
    actions: list[dict[str, Any]], t0: float, t1: float
) -> list[dict[str, Any]]:
    return [
        ev
        for ev in actions
        if is_macro_event(ev)
        and isinstance(ev.get("second"), (int, float))
        and t0 <= float(ev["second"]) <= t1
    ]


def first_order_time(actions: list[dict[str, Any]], pred) -> float | None:
    times = [
        float(ev["second"])
        for ev in actions
        if pred(ev) and isinstance(ev.get("second"), (int, float))
    ]
    return min(times) if times else None


def ordered_count(actions: list[dict[str, Any]], pred) -> int:
    return sum(1 for ev in actions if pred(ev))


def _nth_time(actions: list[dict[str, Any]], pred, n: int) -> float | None:
    times = sorted(
        float(ev["second"])
        for ev in actions
        if pred(ev) and isinstance(ev.get("second"), (int, float))
    )
    return times[n - 1] if len(times) >= n else None


def _set_milestone(
    feats: dict[str, Any], name: str, t: float | None, horizon: float
) -> None:
    obs = t is not None and t <= horizon
    feats[f"{name}_observed"] = int(obs)
    feats[f"{name}_time"] = float(t) if obs else float(horizon)


def _ngrams(tokens: list[str], n: int) -> list[str]:
    if len(tokens) < n:
        return []
    return ["||".join(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]


def _sparse_ngram_features(
    tokens: list[str], vocab: list[str] | None = None, top_k: int = TOP_NGRAM_VOCAB
) -> dict[str, float]:
    grams = Counter(_ngrams(tokens, 1) + _ngrams(tokens, 2) + _ngrams(tokens, 3))
    if vocab is None:
        vocab = [g for g, _ in grams.most_common(top_k)]
    out: dict[str, float] = {}
    gram_set = set(grams)
    for i, g in enumerate(vocab):
        out[f"ng_{i:03d}"] = float(g in gram_set)
    out["seq_token_count"] = float(len(tokens))
    return out


def _investment_indices(clipped: list[dict[str, Any]], horizon: float) -> dict[str, float]:
    bucket_counts: Counter[str] = Counter(investment_bucket(ev) for ev in clipped)
    h = max(horizon, 1.0)

    def norm(count: int, cap: float) -> float:
        return round(min(1.0, count / cap), 4)

    economy = norm(bucket_counts.get("economy", 0), 25.0)
    production = norm(bucket_counts.get("production", 0), 6.0)
    technology = norm(bucket_counts.get("technology", 0), 4.0)
    ground = norm(bucket_counts.get("ground", 0), 15.0)
    air = norm(bucket_counts.get("air", 0), 8.0)
    defense = norm(bucket_counts.get("defense", 0), 4.0)
    upgrade = norm(bucket_counts.get("upgrade", 0), 3.0)
    expansion = norm(bucket_counts.get("expansion", 0), 3.0)

    # timing bonuses for early gas / expansion
    t_gas = first_order_time(clipped, lambda e: result_name(e) in GAS)
    t_exp = _nth_time(clipped, lambda e: result_name(e) in BASES, 2)
    if t_gas is not None and t_gas <= 120:
        economy = min(1.0, economy + 0.15)
    if t_exp is not None and t_exp <= 200:
        expansion = min(1.0, expansion + 0.2)

    return {
        "idx_economy": economy,
        "idx_production": production,
        "idx_technology": technology,
        "idx_ground": ground,
        "idx_air": air,
        "idx_defense": defense,
        "idx_upgrade": upgrade,
        "idx_expansion": expansion,
    }


def extract_opening_features(
    actions: list[dict[str, Any]],
    horizon: int | float,
    *,
    ngram_vocab: list[str] | None = None,
) -> dict[str, Any]:
    """Opening-window features using ordered_* semantics up to horizon."""
    h = float(horizon)
    clipped = clip_actions(actions, h)
    feats: dict[str, Any] = {}

    _set_milestone(feats, "first_gas", first_order_time(clipped, lambda e: result_name(e) in GAS), h)
    _set_milestone(
        feats,
        "first_expansion",
        _nth_time(clipped, lambda e: result_name(e) in BASES, 2),
        h,
    )
    _set_milestone(
        feats,
        "first_production",
        first_order_time(clipped, lambda e: result_name(e) in PROD_BUILDINGS),
        h,
    )
    _set_milestone(
        feats,
        "second_production",
        _nth_time(clipped, lambda e: result_name(e) in PROD_BUILDINGS, 2),
        h,
    )
    _set_milestone(
        feats,
        "first_tech",
        first_order_time(clipped, lambda e: result_name(e) in TECH_BUILDINGS),
        h,
    )
    _set_milestone(
        feats,
        "first_combat_unit",
        first_order_time(
            clipped,
            lambda e: result_name(e) in COMBAT_FAMILY and result_name(e) not in WORKERS,
        ),
        h,
    )
    _set_milestone(
        feats,
        "first_upgrade",
        first_order_time(clipped, lambda e: e.get("event") == "upgrade_research"),
        h,
    )
    _set_milestone(
        feats,
        "first_static_defense",
        first_order_time(clipped, lambda e: result_name(e) in STATIC_DEFENSE),
        h,
    )

    feats[f"ordered_workers_by_{int(h)}"] = ordered_count(clipped, lambda e: result_name(e) in WORKERS)
    feats[f"ordered_prod_buildings_by_{int(h)}"] = ordered_count(
        clipped, lambda e: result_name(e) in PROD_BUILDINGS
    )
    feats[f"ordered_tech_by_{int(h)}"] = ordered_count(
        clipped, lambda e: result_name(e) in TECH_BUILDINGS
    )
    feats[f"ordered_combat_by_{int(h)}"] = ordered_count(
        clipped,
        lambda e: result_name(e) in COMBAT_FAMILY and result_name(e) not in WORKERS,
    )
    feats[f"ordered_upgrades_by_{int(h)}"] = ordered_count(
        clipped, lambda e: e.get("event") == "upgrade_research"
    )
    feats[f"ordered_expansions_by_{int(h)}"] = ordered_count(
        clipped, lambda e: result_name(e) in BASES
    )
    feats[f"ordered_gas_by_{int(h)}"] = ordered_count(clipped, lambda e: result_name(e) in GAS)
    feats[f"ordered_supply_by_{int(h)}"] = ordered_count(clipped, lambda e: result_name(e) in SUPPLY)
    feats[f"ordered_macro_by_{int(h)}"] = len(clipped)

    feats.update(_investment_indices(clipped, h))

    key_seq = build_key_sequence(clipped)
    tokens = [x["token"] for x in key_seq]
    feats["key_sequence"] = " > ".join(tokens[:40])
    feats.update(_sparse_ngram_features(tokens, vocab=ngram_vocab))

    return feats


def extract_state_features(
    actions: list[dict[str, Any]],
    t: float,
    recent_window: float = 60.0,
) -> dict[str, Any]:
    """Cumulative state at t plus recent commitment in [t-recent_window, t]."""
    cumulative = clip_actions(actions, t)
    recent = actions_in_window(actions, max(0.0, t - recent_window), t)

    feats: dict[str, Any] = {
        "snapshot_time": t,
        "cumulative_macro_count": len(cumulative),
        "recent_macro_count": len(recent),
    }

    for prefix, evs in (("cum", cumulative), ("recent", recent)):
        bucket_counts = Counter(investment_bucket(ev) for ev in evs)
        for bucket in INVESTMENT_BUCKETS:
            feats[f"{prefix}_{bucket}_count"] = bucket_counts.get(bucket, 0)

    feats.update(_investment_indices(cumulative, max(t, 1.0)))

    # top entity counts in recent window
    entity_counts = Counter(result_name(ev) for ev in recent)
    for name, cnt in entity_counts.most_common(8):
        safe = name.replace(" ", "_")
        feats[f"recent_entity_{safe}"] = cnt

    return feats


def extract_response_delta(
    actions: list[dict[str, Any]],
    t: float,
    delta: float = 60.0,
) -> dict[str, Any]:
    """Action counts in (t, t+delta] by investment bucket and entity deltas."""
    window = actions_in_window(actions, t + 1e-6, t + delta)
    feats: dict[str, Any] = {"response_delta": delta, "response_start": t, "response_action_count": len(window)}

    bucket_counts = Counter(investment_bucket(ev) for ev in window)
    for bucket in INVESTMENT_BUCKETS:
        feats[f"delta_{bucket}_count"] = bucket_counts.get(bucket, 0)

    entity_counts = Counter(result_name(ev) for ev in window)
    for name, cnt in entity_counts.most_common(10):
        safe = name.replace(" ", "_")
        feats[f"delta_entity_{safe}"] = cnt

    return feats


DEFAULT_META_COLS = frozenset(
    {
        "replay_id",
        "player_id",
        "race",
        "opponent_race",
        "directional_matchup",
        "matchup_dir",
        "result",
        "mmr",
        "mmr_diff",
        "map_name",
        "version",
        "base_build",
        "region",
        "horizon",
        "snapshot_time",
        "key_sequence",
        "opening_observed_to",
        "early_terminated",
    }
)


def feature_matrix(
    df: pd.DataFrame,
    meta_cols: set[str] | frozenset[str] | None = None,
) -> tuple[np.ndarray, list[str]]:
    """Build numeric feature matrix excluding metadata columns."""
    meta = meta_cols or DEFAULT_META_COLS
    cols: list[str] = []
    for c in df.columns:
        if c in meta:
            continue
        if df[c].dtype.kind in "iufcb":
            cols.append(c)
        elif df[c].dtype == bool:
            cols.append(c)
    if not cols:
        return np.zeros((len(df), 0), dtype=np.float64), []
    X = df[cols].fillna(0.0).to_numpy(dtype=np.float64)
    X[~np.isfinite(X)] = 0.0
    return X, cols


def standardize_fit(X: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return standardized X, mean, scale."""
    mean = X.mean(axis=0)
    scale = X.std(axis=0)
    scale[scale == 0] = 1.0
    return (X - mean) / scale, mean, scale


def standardize_transform(X: np.ndarray, mean: np.ndarray, scale: np.ndarray) -> np.ndarray:
    return (X - mean) / scale


def robust_scale_within(
    df: pd.DataFrame, cols: list[str], group_cols: list[str]
) -> pd.DataFrame:
    """Robust z-score within groups using median/IQR."""
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


# ---- Compatibility aliases used by stage modules ----

def opening_features(actions: list[dict[str, Any]], horizon: int) -> dict[str, Any]:
    feats = extract_opening_features(actions, horizon)
    # normalize to stage-expected keys
    h = int(horizon)
    alias = {
        "ordered_worker": feats.get(f"ordered_workers_by_{h}", 0),
        "ordered_prod": feats.get(f"ordered_prod_buildings_by_{h}", 0),
        "ordered_tech": feats.get(f"ordered_tech_by_{h}", 0),
        "ordered_combat": feats.get(f"ordered_combat_by_{h}", 0),
        "ordered_upgrade": feats.get(f"ordered_upgrades_by_{h}", 0),
        "ordered_base": feats.get(f"ordered_expansions_by_{h}", 0),
        "ordered_gas": feats.get(f"ordered_gas_by_{h}", 0),
        "ordered_supply": feats.get(f"ordered_supply_by_{h}", 0),
        "horizon": h,
        "n_actions": feats.get(f"ordered_macro_by_{h}", len(actions)),
    }
    # investment aliases
    for src, dst in [
        ("idx_economy", "inv_economy"),
        ("idx_production", "inv_production"),
        ("idx_technology", "inv_technology"),
        ("idx_ground", "inv_ground"),
        ("idx_air", "inv_air"),
        ("idx_defense", "inv_defense"),
        ("idx_upgrade", "inv_upgrade"),
        ("idx_expansion", "inv_expansion"),
    ]:
        if src in feats:
            alias[dst] = feats[src]
            alias[f"cnt_{dst[4:]}"] = feats.get(src, 0)
    # tech path flags
    names = {result_name(a) for a in clip_actions(actions, h)}
    for flag, entity in [
        ("has_factory", "Factory"),
        ("has_starport", "Starport"),
        ("has_barracks", "Barracks"),
        ("has_robo", "RoboticsFacility"),
        ("has_stargate", "Stargate"),
        ("has_twilight", "TwilightCouncil"),
        ("has_forge", "Forge"),
        ("has_spire", "Spire"),
        ("has_lair", "Lair"),
        ("has_roach_warren", "RoachWarren"),
        ("has_baneling_nest", "BanelingNest"),
        ("has_hydra_den", "HydraliskDen"),
        ("has_armory", "Armory"),
        ("has_ebay", "EngineeringBay"),
        ("has_cyber", "CyberneticsCore"),
    ]:
        alias[flag] = int(entity in names)
    feats.update(alias)
    return feats


def state_features(actions: list[dict[str, Any]], t: float, recent_window: float = 60.0) -> dict[str, Any]:
    feats = extract_state_features(actions, t, recent_window=recent_window)
    out = {"t": t, "n_cum": feats.get("cumulative_macro_count", 0), "n_recent": feats.get("recent_macro_count", 0)}
    # map cum_/recent_ *_count to expected keys
    for k, v in feats.items():
        if k.startswith("cum_") and k.endswith("_count"):
            bucket = k[len("cum_") : -len("_count")]
            out[f"cum_{bucket}"] = float(v)
            out[f"cnt_cum_{bucket}"] = int(v)
        elif k.startswith("recent_") and k.endswith("_count") and not k.startswith("recent_entity"):
            bucket = k[len("recent_") : -len("_count")]
            tot = max(1, feats.get("recent_macro_count", 1))
            out[f"recent_{bucket}"] = float(v) / tot
            out[f"cnt_recent_{bucket}"] = int(v)
        elif k.startswith("idx_"):
            out[k.replace("idx_", "cum_")] = v
    out["ordered_worker"] = feats.get("cum_economy_count", 0)
    out["ordered_base"] = feats.get("cum_expansion_count", 0)
    out["ordered_prod"] = feats.get("cum_production_count", 0)
    out["ordered_tech"] = feats.get("cum_technology_count", 0)
    out["ordered_combat"] = feats.get("cum_ground_count", 0) + feats.get("cum_air_count", 0)
    out["ordered_static"] = feats.get("cum_defense_count", 0)
    out["ordered_upgrade"] = feats.get("cum_upgrade_count", 0)
    out["ordered_air"] = feats.get("cum_air_count", 0)
    return out


def response_delta_features(actions: list[dict[str, Any]], t0: float, t1: float) -> dict[str, Any]:
    delta = max(1.0, float(t1) - float(t0))
    feats = extract_response_delta(actions, t0, delta=delta)
    out = {"t0": t0, "t1": t1, "n_delta": feats.get("response_action_count", 0)}
    tot = max(1, out["n_delta"])
    for k, v in feats.items():
        if k.startswith("delta_") and k.endswith("_count") and not k.startswith("delta_entity"):
            bucket = k[len("delta_") : -len("_count")]
            out[f"d_{bucket}"] = float(v) / tot
            out[f"dc_{bucket}"] = int(v)
        elif k.startswith("delta_entity_"):
            name = k[len("delta_entity_") :]
            out[f"act_{name}"] = int(v)
    # top actions string
    tops = []
    for k, v in feats.items():
        if k.startswith("delta_entity_"):
            tops.append((k[len("delta_entity_") :], int(v)))
    tops.sort(key=lambda x: -x[1])
    out["top_actions"] = ",".join(f"{n}:{c}" for n, c in tops[:8])
    return out


def numeric_feature_cols(df_columns, prefixes=None, exclude=None) -> list[str]:
    exclude = set(exclude or [])
    cols = []
    for c in df_columns:
        if c in exclude:
            continue
        if c.startswith(("ng_", "act_", "inv_", "cnt_", "cum_", "recent_", "d_", "dc_", "ordered_", "first_", "second_", "has_", "idx_", "delta_")):
            cols.append(c)
            continue
        if c.endswith("_observed") or c.endswith("_time_z") or c.endswith("_z"):
            cols.append(c)
    use = []
    colset = set(df_columns)
    for c in cols:
        if c.endswith("_time") and f"{c}_z" in colset:
            continue
        use.append(c)
    return sorted(set(use))
