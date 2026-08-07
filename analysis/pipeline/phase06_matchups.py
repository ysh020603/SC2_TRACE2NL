"""Phase 6: counter matrix and win-rate models (plan.md §11–13)."""

from __future__ import annotations

import math
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import OneHotEncoder

from analysis.pipeline.io_utils import ensure_dir, write_json


def wilson_interval(wins: int, n: int, z: float = 1.96) -> tuple[float | None, float | None]:
    if n <= 0:
        return None, None
    p = wins / n
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    margin = z * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denom
    return max(0.0, center - margin), min(1.0, center + margin)


def reliability_grade(n: int) -> str:
    # plan thresholds fixed a priori
    if n >= 500:
        return "A"
    if n >= 200:
        return "B"
    if n >= 50:
        return "C"
    return "D"


def _pair_strategies(global_df: pd.DataFrame) -> pd.DataFrame:
    """One row per replay from player1 perspective with opponent strategy."""
    cols = [
        "replay_id",
        "player_id",
        "race",
        "opponent_race",
        "matchup_dir",
        "result",
        "strategy_id",
        "mmr_diff",
        "map_name",
        "base_build",
        "region",
    ]
    present = [c for c in cols if c in global_df.columns]
    df = global_df[present].copy()
    # drop noise for primary matrix
    df = df.loc[~df["strategy_id"].astype(str).str.endswith("Noise")].copy()

    left = df.rename(
        columns={
            "player_id": "own_player_id",
            "race": "own_race",
            "strategy_id": "own_strategy",
            "result": "own_result",
        }
    )
    right = df[
        ["replay_id", "player_id", "race", "strategy_id"]
    ].rename(
        columns={
            "player_id": "opp_player_id",
            "race": "opp_race_from_row",
            "strategy_id": "opp_strategy",
        }
    )
    pairs = left.merge(right, on="replay_id", how="inner")
    pairs = pairs.loc[pairs["own_player_id"] != pairs["opp_player_id"]].copy()
    # keep only Win/Loss
    pairs = pairs.loc[pairs["own_result"].isin(["Win", "Loss"])].copy()
    pairs["win"] = (pairs["own_result"] == "Win").astype(int)
    # each replay contributes 2 directed rows; analysis should cluster by replay_id
    return pairs


def run_phase06(clusters_dir: Path, out_dir: Path) -> dict[str, Any]:
    ensure_dir(out_dir)
    global_df = pd.read_parquet(clusters_dir / "global_clusters.parquet")
    pairs = _pair_strategies(global_df)
    pairs.to_parquet(out_dir / "strategy_pairs.parquet", index=False)

    # raw counter matrix
    rows = []
    for (own, opp), g in pairs.groupby(["own_strategy", "opp_strategy"]):
        # dedupe to one row per replay for win rate from first player? keep directed but
        # since both sides present, n counts directed player-games; also report unique replays
        n = len(g)
        wins = int(g["win"].sum())
        wr = wins / n if n else None
        lo, hi = wilson_interval(wins, n)
        rows.append(
            {
                "own_strategy": own,
                "opp_strategy": opp,
                "n": n,
                "n_replays": int(g["replay_id"].nunique()),
                "wins": wins,
                "raw_winrate": wr,
                "wilson_low": lo,
                "wilson_high": hi,
                "reliability": reliability_grade(n),
            }
        )
    raw = pd.DataFrame(rows).sort_values(["own_strategy", "opp_strategy"])
    raw.to_csv(out_dir / "raw_counter_matrix.csv", index=False)

    # matchup baseline winrate by own race vs opponent race
    baseline = (
        pairs.groupby(["own_race", "opponent_race"], dropna=False)["win"].mean().to_dict()
    )

    # adjusted via L2 logistic: win ~ own + opp + own:opp + mmr_diff + map + patch + region
    # with small-n shrinkage; hierarchical Bayes approximated by strong regularization
    model_rows = []
    coef_rows = []
    posterior_rows = []  # shrinkage-style predictive winrates

    use = pairs.dropna(subset=["own_strategy", "opp_strategy"]).copy()
    if len(use) >= 20 and use["win"].nunique() == 2:
        use["pair"] = use["own_strategy"].astype(str) + "__vs__" + use["opp_strategy"].astype(str)
        use["mmr_diff"] = use["mmr_diff"].fillna(0.0)
        use["map_name"] = use["map_name"].fillna("unknown")
        use["base_build"] = use["base_build"].fillna(-1).astype(str)
        use["region"] = use["region"].fillna("unknown")

        y = use["win"].to_numpy()
        cat = use[["own_strategy", "opp_strategy", "pair", "map_name", "base_build", "region"]]
        enc = OneHotEncoder(handle_unknown="ignore", sparse_output=True)
        X_cat = enc.fit_transform(cat)
        X_num = use[["mmr_diff"]].to_numpy()
        # scale mmr
        X_num = (X_num - X_num.mean()) / (X_num.std() + 1e-6)
        from scipy import sparse

        X = sparse.hstack([X_cat, X_num])

        clf = LogisticRegression(
            penalty="l2",
            C=0.5,
            max_iter=1000,
            solver="lbfgs",
        )
        clf.fit(X, y)

        # coefficients
        feat_names = list(enc.get_feature_names_out()) + ["mmr_diff"]
        for name, coef in zip(feat_names, clf.coef_.ravel(), strict=False):
            coef_rows.append({"feature": name, "coefficient": float(coef)})

        # predicted adjusted winrate per pair at mmr_diff=0, modal map/patch/region
        modal_map = use["map_name"].mode().iloc[0]
        modal_patch = use["base_build"].mode().iloc[0]
        modal_region = use["region"].mode().iloc[0]
        for (own, opp), g in use.groupby(["own_strategy", "opp_strategy"]):
            row = pd.DataFrame(
                [
                    {
                        "own_strategy": own,
                        "opp_strategy": opp,
                        "pair": f"{own}__vs__{opp}",
                        "map_name": modal_map,
                        "base_build": modal_patch,
                        "region": modal_region,
                        "mmr_diff": 0.0,
                    }
                ]
            )
            Xc = enc.transform(row[["own_strategy", "opp_strategy", "pair", "map_name", "base_build", "region"]])
            Xn = np.array([[0.0]])
            Xp = sparse.hstack([Xc, Xn])
            p = float(clf.predict_proba(Xp)[0, 1])
            n = len(g)
            wins = int(g["win"].sum())
            raw_wr = wins / n
            own_race = g["own_race"].iloc[0]
            opp_race = g["opponent_race"].iloc[0]
            base = baseline.get((own_race, opp_race), 0.5)
            lift = p - base
            lo, hi = wilson_interval(wins, n)
            # Bayesian-ish: posterior mean shrink raw to adjusted
            # Beta(1+wins,1+losses) mean as simple posterior summary
            post_mean = (1 + wins) / (2 + n)
            # mix with model prediction
            shrink = (n / (n + 30)) * raw_wr + (30 / (n + 30)) * p
            model_rows.append(
                {
                    "own_strategy": own,
                    "opp_strategy": opp,
                    "n": n,
                    "raw_winrate": raw_wr,
                    "adjusted_winrate": p,
                    "shrunk_winrate": shrink,
                    "baseline_matchup_wr": base,
                    "lift_vs_baseline": lift,
                    "wilson_low": lo,
                    "wilson_high": hi,
                    "reliability": reliability_grade(n),
                    "p_winrate_gt_0_5": None,  # filled below from beta
                }
            )
            # P(wr>0.5) under Beta(1+w,1+n-w)
            # approximate via normal on logit or monte carlo
            alpha = 1 + wins
            beta = 1 + (n - wins)
            # Monte Carlo
            samples = np.random.default_rng(0).beta(alpha, beta, size=4000)
            p_gt = float((samples > 0.5).mean())
            p_lift = float((samples > base + 0.05).mean())
            model_rows[-1]["p_winrate_gt_0_5"] = p_gt
            model_rows[-1]["p_lift_gt_5pp"] = p_lift
            posterior_rows.append(
                {
                    "own_strategy": own,
                    "opp_strategy": opp,
                    "n": n,
                    "beta_alpha": alpha,
                    "beta_beta": beta,
                    "posterior_mean": post_mean,
                    "p_winrate_gt_0_5": p_gt,
                    "p_lift_gt_5pp": p_lift,
                    "model_adjusted_winrate": p,
                    "shrunk_winrate": shrink,
                    "reliability": reliability_grade(n),
                }
            )

        # BH-FDR on exploratory tests: H0 raw_wr == 0.5 using Wilson not containing 0.5
        # use simple two-sided p from beta-binomial style: 2*min(P(>0.5), P(<0.5))
        pvals = []
        for r in model_rows:
            p_gt = r["p_winrate_gt_0_5"] or 0.5
            pval = 2 * min(p_gt, 1 - p_gt)
            pvals.append(pval)
        order = np.argsort(pvals)
        m = len(pvals)
        bh = [None] * m
        prev = 1.0
        for rank, idx in enumerate(reversed(list(order)), start=1):
            # reverse for step-up
            pass
        # standard BH
        adj = np.zeros(m)
        sorted_idx = list(order)
        for i, idx in enumerate(sorted_idx):
            rank = i + 1
            adj[idx] = min(1.0, pvals[idx] * m / rank)
        # enforce monotone
        for i in range(m - 2, -1, -1):
            idx = sorted_idx[i]
            idx_next = sorted_idx[i + 1]
            adj[idx] = min(adj[idx], adj[idx_next])
        for r, p, q in zip(model_rows, pvals, adj, strict=False):
            r["pvalue_two_sided"] = float(p)
            r["fdr_qvalue"] = float(q)

    adj_df = pd.DataFrame(model_rows)
    if len(adj_df):
        adj_df.to_csv(out_dir / "adjusted_counter_matrix.csv", index=False)
    else:
        # fallback empty with header
        raw.assign(
            adjusted_winrate=np.nan,
            lift_vs_baseline=np.nan,
            fdr_qvalue=np.nan,
        ).to_csv(out_dir / "adjusted_counter_matrix.csv", index=False)

    pd.DataFrame(coef_rows).to_csv(out_dir / "model_coefficients.csv", index=False)
    pd.DataFrame(posterior_rows).to_csv(out_dir / "posterior_summary.csv", index=False)

    summary = {
        "pair_rows": int(len(pairs)),
        "unique_replays": int(pairs["replay_id"].nunique()) if len(pairs) else 0,
        "counter_cells": int(len(raw)),
        "cells_by_reliability": raw["reliability"].value_counts().to_dict() if len(raw) else {},
        "model": "L2 logistic + Beta shrinkage (hierarchical Bayes approximation for small n)",
        "note": (
            "With n≈240 stratified sample, most cells are grade D/C; "
            "do not treat adjusted edges as population causal effects."
        ),
    }
    write_json(out_dir / "phase06_summary.json", summary)
    return summary
