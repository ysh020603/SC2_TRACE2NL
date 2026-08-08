"""Statistical helpers for transition value and outcome modeling."""

from __future__ import annotations

import math
from typing import Any, Sequence

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import KFold

from analysis.skill_mining_v2.config import (
    DEFAULT_LIFT_ABS,
    PREFERRED_SUPPORT_DEFAULT,
    adaptive_ess,
    adaptive_lift_threshold,
    adaptive_min_support,
)


def win_rate(wins: int, n: int) -> float | None:
    if n <= 0:
        return None
    return wins / n


def wilson_interval(wins: int, n: int, z: float = 1.96) -> tuple[float | None, float | None]:
    if n <= 0:
        return None, None
    p = wins / n
    denom = 1 + z**2 / n
    center = (p + z**2 / (2 * n)) / denom
    margin = z * math.sqrt(p * (1 - p) / n + z**2 / (4 * n**2)) / denom
    return max(0.0, center - margin), min(1.0, center + margin)


def enrichment(
    cluster_rate: float,
    baseline_rate: float,
    *,
    eps: float = 1e-9,
) -> float | None:
    if baseline_rate <= eps:
        return None
    return cluster_rate / baseline_rate


def bootstrap_ci(
    values: np.ndarray | Sequence[float],
    n_boot: int = 500,
    alpha: float = 0.05,
    seed: int = 42,
    stat: str = "mean",
) -> tuple[float, float, float]:
    arr = np.asarray(values, dtype=float)
    arr = arr[np.isfinite(arr)]
    if len(arr) == 0:
        return float("nan"), float("nan"), float("nan")
    rng = np.random.default_rng(seed)
    boots = []
    for _ in range(n_boot):
        sample = rng.choice(arr, size=len(arr), replace=True)
        boots.append(float(np.mean(sample)) if stat == "mean" else float(np.median(sample)))
    lo = float(np.quantile(boots, alpha / 2))
    hi = float(np.quantile(boots, 1 - alpha / 2))
    point = float(np.mean(arr)) if stat == "mean" else float(np.median(arr))
    return point, lo, hi


def fit_propensity_model(
    df: pd.DataFrame,
    treatment_col: str,
    covariate_cols: list[str],
    *,
    multinomial: bool = True,
    random_state: int = 42,
    max_iter: int = 500,
) -> tuple[LogisticRegression, np.ndarray]:
    """Estimate P(T | X) for multi-treatment or binary treatment."""
    X = df[covariate_cols].fillna(0.0).to_numpy(dtype=float)
    y = df[treatment_col].astype(str).to_numpy()
    model = LogisticRegression(
        max_iter=max_iter,
        random_state=random_state,
        multi_class="multinomial" if multinomial else "auto",
        solver="lbfgs" if multinomial else "liblinear",
        n_jobs=-1,
    )
    model.fit(X, y)
    if hasattr(model, "predict_proba"):
        probs = model.predict_proba(X)
    else:
        probs = model.decision_function(X)
    return model, probs


def fit_outcome_model(
    df: pd.DataFrame,
    outcome_col: str,
    feature_cols: list[str],
    *,
    random_state: int = 42,
) -> LogisticRegression:
    """Binary outcome model P(Y | X, T)."""
    X = df[feature_cols].fillna(0.0).to_numpy(dtype=float)
    y = df[outcome_col].astype(int).to_numpy()
    model = LogisticRegression(max_iter=500, random_state=random_state, n_jobs=-1)
    model.fit(X, y)
    return model


def aipw_doubly_robust(
    df: pd.DataFrame,
    treatment_col: str,
    outcome_col: str,
    covariate_cols: list[str],
    treatments: list[str] | None = None,
    n_folds: int = 5,
    random_state: int = 42,
) -> pd.DataFrame:
    """Cross-fitted AIPW estimates for multi-treatment causal contrast vs reference."""
    data = df.copy()
    if treatments is None:
        treatments = sorted(data[treatment_col].astype(str).unique())
    if len(treatments) < 2:
        return pd.DataFrame()

    ref = treatments[0]
    y = data[outcome_col].astype(int).to_numpy()
    t_vals = data[treatment_col].astype(str).to_numpy()
    X = data[covariate_cols].fillna(0.0).to_numpy(dtype=float)
    n = len(data)

    kf = KFold(n_splits=n_folds, shuffle=True, random_state=random_state)
    e_hat = np.zeros(n)

    for train_idx, test_idx in kf.split(X):
        X_tr, X_te = X[train_idx], X[test_idx]
        y_tr = y[train_idx]
        t_tr = t_vals[train_idx]

        prop_model = LogisticRegression(
            max_iter=500,
            multi_class="multinomial",
            solver="lbfgs",
            random_state=random_state,
        )
        prop_model.fit(X_tr, t_tr)
        class_list = list(prop_model.classes_)
        prob_mat = prop_model.predict_proba(X_te)
        for i, row_idx in enumerate(test_idx):
            ti = class_list.index(t_vals[row_idx])
            e_hat[row_idx] = prob_mat[i, ti]

    rows = []
    for treat in treatments:
        if treat == ref:
            continue
        mask_t = t_vals == treat
        mask_r = t_vals == ref
        if mask_t.sum() == 0 or mask_r.sum() == 0:
            continue
        # simple AIPW contrast
        psi_t = np.mean(y[mask_t] / np.clip(e_hat[mask_t], 0.05, 1.0))
        psi_r = np.mean(y[mask_r] / np.clip(e_hat[mask_r], 0.05, 1.0))
        lift = psi_t - psi_r
        _, lo, hi = bootstrap_ci(
            (y[mask_t] / np.clip(e_hat[mask_t], 0.05, 1.0))
            - np.mean(y[mask_r] / np.clip(e_hat[mask_r], 0.05, 1.0)),
            seed=random_state,
        )
        rows.append(
            {
                "treatment": treat,
                "reference": ref,
                "support": int(mask_t.sum()),
                "adjusted_lift": float(lift),
                "ci_low": lo,
                "ci_high": hi,
                "ess_proxy": int(min(mask_t.sum(), mask_r.sum())),
            }
        )
    return pd.DataFrame(rows)


def adjusted_lift_table(
    df: pd.DataFrame,
    group_cols: list[str],
    outcome_col: str = "win",
    covariate_cols: list[str] | None = None,
) -> pd.DataFrame:
    """Compute raw and covariate-adjusted lift by group."""
    rows = []
    covariate_cols = covariate_cols or []
    global_wr = win_rate(int(df[outcome_col].sum()), len(df))

    for keys, sub in df.groupby(group_cols):
        if not isinstance(keys, tuple):
            keys = (keys,)
        wins = int(sub[outcome_col].sum())
        n = len(sub)
        wr = win_rate(wins, n)
        lift = None if global_wr is None or wr is None else wr - global_wr
        row = dict(zip(group_cols, keys))
        row.update({"support": n, "win_rate": wr, "lift_vs_global": lift})
        if covariate_cols:
            try:
                model = fit_outcome_model(
                    sub.assign(win=sub[outcome_col]),
                    "win",
                    covariate_cols,
                )
                row["model_intercept"] = float(model.intercept_[0])
            except Exception:
                row["model_intercept"] = None
        rows.append(row)
    return pd.DataFrame(rows)


def classify_edge_label(
    support: int,
    lift: float,
    ci: tuple[float | None, float | None],
    thresholds: dict[str, float] | None = None,
    n_population: int | None = None,
) -> str:
    """Classify transition edge as preferred/harmful/default/uncertain."""
    n = n_population or support
    min_support = adaptive_min_support(n, default=PREFERRED_SUPPORT_DEFAULT)
    min_ess = adaptive_ess(n)
    pref_lift, harm_lift = adaptive_lift_threshold(n)
    if thresholds:
        pref_lift = thresholds.get("preferred_lift", pref_lift)
        harm_lift = thresholds.get("harmful_lift", harm_lift)
        min_support = int(thresholds.get("min_support", min_support))

    if support < min_support or support < min_ess:
        return "uncertain"

    lo, hi = ci
    if lo is not None and hi is not None:
        if lo > pref_lift:
            return "preferred"
        if hi < harm_lift:
            return "harmful"
        if abs(lift) <= DEFAULT_LIFT_ABS:
            return "default"
        return "uncertain"

    if lift >= pref_lift:
        return "preferred"
    if lift <= harm_lift:
        return "harmful"
    if abs(lift) <= DEFAULT_LIFT_ABS:
        return "default"
    return "uncertain"


def adaptive_thresholds(n: int) -> dict[str, float | int]:
    pref, harm = adaptive_lift_threshold(n)
    return {
        "min_support": adaptive_min_support(n),
        "min_ess": adaptive_ess(n),
        "preferred_lift": pref,
        "harmful_lift": harm,
        "default_lift_abs": DEFAULT_LIFT_ABS,
    }


# ---- Compatibility aliases used by stage modules ----

def normalize_series(s: pd.Series) -> pd.Series:
    s = s.astype(float)
    lo, hi = s.min(), s.max()
    if not np.isfinite(lo) or not np.isfinite(hi) or hi - lo < 1e-12:
        return pd.Series(np.zeros(len(s)), index=s.index)
    return (s - lo) / (hi - lo)


def opponent_leakage_score(own_labels: np.ndarray, opp_features: pd.DataFrame, *, seed: int = 42) -> float:
    from sklearn.preprocessing import LabelEncoder, StandardScaler

    y_raw = np.asarray(own_labels)
    if len(set(y_raw)) < 2 or len(y_raw) < 40:
        return 0.0
    X = opp_features.fillna(0.0).to_numpy(dtype=np.float64)
    X[~np.isfinite(X)] = 0.0
    n = len(y_raw)
    if n > 8000:
        rng = np.random.default_rng(seed)
        idx = rng.choice(n, size=8000, replace=False)
        X, y_raw = X[idx], y_raw[idx]
    le = LabelEncoder()
    y = le.fit_transform(y_raw)
    if len(set(y)) < 2:
        return 0.0
    Xs = StandardScaler().fit_transform(X)
    maj = max(np.bincount(y)) / len(y)
    try:
        clf = LogisticRegression(max_iter=200, solver="lbfgs", random_state=seed)
        rng = np.random.default_rng(seed)
        perm = rng.permutation(len(y))
        cut = max(10, int(0.8 * len(y)))
        tr, te = perm[:cut], perm[cut:]
        if len(set(y[tr])) < 2 or len(te) < 5:
            return 0.0
        clf.fit(Xs[tr], y[tr])
        return float(max(0.0, clf.score(Xs[te], y[te]) - maj))
    except Exception:
        return 0.0


def classify_edge(row, *, min_support: int, min_ess: int) -> str:
    support = int(row.get("support") or 0)
    ess = float(row.get("ess") or support)
    lift = float(row.get("adjusted_lift") or row.get("win_enrichment") or 0.0)
    p = float(row.get("p_response") or 0.0)
    ci_low = row.get("ci_low")
    ci_high = row.get("ci_high")
    q_value = row.get("q_value")
    positive_prob = float(row.get("bootstrap_positive_prob") or 0.5)
    confidence_positive = (
        (q_value is not None and np.isfinite(q_value) and float(q_value) < 0.05)
        or positive_prob >= 0.90
        or (ci_low is not None and np.isfinite(ci_low) and float(ci_low) > 0)
    )
    confidence_negative = (
        (q_value is not None and np.isfinite(q_value) and float(q_value) < 0.05)
        or positive_prob <= 0.10
        or (ci_high is not None and np.isfinite(ci_high) and float(ci_high) < 0)
    )
    robust = bool(row.get("robustness_pass", True))
    if support >= min_support and ess >= min_ess and lift >= 0.03 and confidence_positive and robust:
        return "preferred"
    if support >= min_support and ess >= min_ess and lift <= -0.03 and confidence_negative and robust:
        return "harmful"
    if p >= 0.25 and abs(lift) < 0.015:
        return "default"
    if bool(row.get("is_default_candidate")) and abs(lift) < 0.02:
        return "default"
    return "uncertain"


def estimate_response_values(
    df: pd.DataFrame,
    *,
    context_cols: list[str],
    response_col: str = "response_id",
    outcome_col: str = "is_win",
    covariate_cols: list[str] | None = None,
    n_splits: int = 5,
    seed: int = 42,
) -> pd.DataFrame:
    """Simplified AIPW-style response value table compatible with stage08."""
    from scipy import sparse
    from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler
    from sklearn.model_selection import StratifiedKFold

    work = df.dropna(subset=[response_col, outcome_col]).reset_index(drop=True)
    if len(work) < 40 or work[response_col].nunique() < 2:
        rows = []
        for keys, g in work.groupby(context_cols, dropna=False):
            if not isinstance(keys, tuple):
                keys = (keys,)
            base = {c: v for c, v in zip(context_cols, keys)}
            for resp, rg in g.groupby(response_col):
                rows.append({
                    **base,
                    response_col: resp,
                    "support": int(len(rg)),
                    "ess": float(len(rg)),
                    "p_response": len(rg) / max(1, len(g)),
                    "p_win_raw": float(rg[outcome_col].mean()),
                    "adjusted_lift": float(rg[outcome_col].mean() - g[outcome_col].mean()),
                    "win_enrichment": float(rg[outcome_col].mean() - g[outcome_col].mean()),
                    "loss_enrichment": 0.0,
                    "is_default_candidate": False,
                    "ci_low": float("nan"),
                    "ci_high": float("nan"),
                    "p_value": float("nan"),
                    "bootstrap_positive_prob": 0.5,
                })
        return pd.DataFrame(rows)

    le = LabelEncoder()
    work["_resp"] = le.fit_transform(work[response_col].astype(str))
    y = work[outcome_col].astype(int).to_numpy()
    r = work["_resp"].to_numpy()
    responses = list(le.classes_)
    model_cols = list(context_cols) + list(covariate_cols or [])
    categorical = [
        c
        for c in model_cols
        if c in work.columns
        and (
            not pd.api.types.is_numeric_dtype(work[c])
            or c in {"map", "patch", "base_build", "region"}
        )
    ]
    numeric = [c for c in model_cols if c in work.columns and c not in categorical]
    matrices = []
    if categorical:
        encoder = OneHotEncoder(handle_unknown="ignore", sparse_output=True)
        matrices.append(encoder.fit_transform(work[categorical].fillna("unknown").astype(str)))
    if numeric:
        num = work[numeric].fillna(0.0).to_numpy(dtype=np.float64)
        num[~np.isfinite(num)] = 0.0
        matrices.append(sparse.csr_matrix(StandardScaler().fit_transform(num)))
    Xs = sparse.hstack(matrices, format="csr") if matrices else sparse.csr_matrix((len(work), 1))
    n, n_resp = len(work), len(responses)
    prop = np.full((n, n_resp), 1.0 / n_resp)
    mu = np.full((n, n_resp), float(y.mean()))
    try:
        splitter = StratifiedKFold(n_splits=min(n_splits, max(2, n // 50)), shuffle=True, random_state=seed)
        splits = list(splitter.split(Xs, r))
    except Exception:
        splits = [(np.arange(n), np.arange(n))]
    for tr, te in splits:
        if len(set(r[tr])) < 2:
            continue
        try:
            pm = LogisticRegression(max_iter=250, solver="lbfgs", random_state=seed)
            pm.fit(Xs[tr], r[tr])
            proba = pm.predict_proba(Xs[te])
            full = np.full((len(te), n_resp), 1.0 / n_resp)
            for j, cls in enumerate(pm.classes_):
                full[:, int(cls)] = proba[:, j]
            prop[te] = full
        except Exception:
            pass
        for resp_i in range(n_resp):
            mask_tr = r[tr] == resp_i
            if mask_tr.sum() < 8 or len(set(y[tr][mask_tr])) < 2:
                mu[te, resp_i] = float(y[tr][mask_tr].mean()) if mask_tr.sum() else float(y[tr].mean())
                continue
            try:
                om = LogisticRegression(max_iter=250, solver="lbfgs", random_state=seed)
                om.fit(Xs[tr][mask_tr], y[tr][mask_tr])
                mu[te, resp_i] = om.predict_proba(Xs[te])[:, 1]
            except Exception:
                mu[te, resp_i] = float(y[tr][mask_tr].mean())
    prop = np.clip(prop, 1e-3, 1 - 1e-3)
    aipw = np.zeros((n, n_resp))
    for a in range(n_resp):
        ind = (r == a).astype(float)
        aipw[:, a] = mu[:, a] + ind * (y - mu[:, a]) / prop[:, a]
    rows = []
    for keys, gidx in work.groupby(context_cols, dropna=False).groups.items():
        if not isinstance(keys, tuple):
            keys = (keys,)
        base = {c: v for c, v in zip(context_cols, keys)}
        idx = np.asarray(list(gidx))
        if len(idx) < 5:
            continue
        vals, counts = np.unique(r[idx], return_counts=True)
        local_default = int(vals[int(np.argmax(counts))])
        v_default = float(aipw[idx, local_default].mean())
        for a, resp_name in enumerate(responses):
            support = int((r[idx] == a).sum())
            if support == 0:
                continue
            observed = idx[r[idx] == a]
            weights = 1.0 / prop[observed, a]
            ess = (
                float((weights.sum() ** 2) / np.square(weights).sum())
                if len(weights) and weights.sum() > 0
                else 0.0
            )
            contrast = aipw[idx, a] - aipw[idx, local_default]
            lift = float(contrast.mean())
            se = float(contrast.std(ddof=1) / np.sqrt(len(contrast))) if len(contrast) > 1 else float("nan")
            ci_low = lift - 1.96 * se if np.isfinite(se) else float("nan")
            ci_high = lift + 1.96 * se if np.isfinite(se) else float("nan")
            z = abs(lift / se) if np.isfinite(se) and se > 0 else 0.0
            p_value = math.erfc(z / math.sqrt(2.0)) if z > 0 else 1.0
            positive_prob = (
                0.5 * math.erfc(-lift / (se * math.sqrt(2.0)))
                if np.isfinite(se) and se > 0
                else (1.0 if lift > 0 else 0.0 if lift < 0 else 0.5)
            )
            rows.append({
                **base,
                response_col: resp_name,
                "support": support,
                "ess": ess,
                "p_response": support / len(idx),
                "p_win_raw": float(y[idx][r[idx] == a].mean()),
                "v_hat": float(aipw[idx, a].mean()),
                "v_default": v_default,
                "adjusted_lift": lift,
                "ci_low": ci_low,
                "ci_high": ci_high,
                "p_value": p_value,
                "bootstrap_positive_prob": positive_prob,
                "win_enrichment": float(y[idx][r[idx] == a].mean() - y[idx].mean()),
                "loss_enrichment": 0.0,
                "default_response": responses[local_default],
                "is_default_candidate": resp_name == responses[local_default],
            })
    result = pd.DataFrame(rows)
    if not result.empty:
        # Benjamini-Hochberg FDR correction over all tested context-response edges.
        pvals = result["p_value"].fillna(1.0).to_numpy(dtype=float)
        order = np.argsort(pvals)
        ranked = pvals[order] * len(pvals) / np.arange(1, len(pvals) + 1)
        ranked = np.minimum.accumulate(ranked[::-1])[::-1]
        qvals = np.empty_like(ranked)
        qvals[order] = np.clip(ranked, 0.0, 1.0)
        result["q_value"] = qvals
    return result
