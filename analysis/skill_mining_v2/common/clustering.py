"""Clustering utilities for skill_mining_v2."""

from __future__ import annotations

from collections import Counter, defaultdict
from typing import Any

import numpy as np
from sklearn.cluster import AgglomerativeClustering, HDBSCAN, KMeans
from sklearn.decomposition import PCA, TruncatedSVD
from sklearn.metrics import (
    adjusted_rand_score,
    calinski_harabasz_score,
    davies_bouldin_score,
    normalized_mutual_info_score,
    pairwise_distances,
    silhouette_score,
)
from sklearn.preprocessing import StandardScaler

from analysis.skill_mining_v2.config import LARGEST_CLUSTER_SPLIT_THRESHOLD


def standardize_fit_transform(X: np.ndarray) -> tuple[np.ndarray, StandardScaler]:
    scaler = StandardScaler()
    return scaler.fit_transform(X), scaler


def reduce_dim(
    X: np.ndarray,
    n_components: int = 30,
    method: str = "pca",
    random_state: int = 42,
) -> np.ndarray:
    n = X.shape[0]
    k = min(n_components, X.shape[1], max(1, n - 1))
    if k < 1:
        return X
    if method == "svd":
        model = TruncatedSVD(n_components=k, random_state=random_state)
    else:
        model = PCA(n_components=k, random_state=random_state)
    return model.fit_transform(X)


def cluster_hdbscan(
    X: np.ndarray,
    min_cluster_size: int = 50,
    min_samples: int | None = None,
) -> np.ndarray:
    n = X.shape[0]
    if n < max(4, min_cluster_size):
        return np.zeros(n, dtype=int)
    ms = min_samples if min_samples is not None else max(5, min_cluster_size // 5)
    model = HDBSCAN(
        min_cluster_size=min_cluster_size,
        min_samples=ms,
        metric="euclidean",
        cluster_selection_method="eom",
        n_jobs=-1,
    )
    labels = model.fit_predict(X)
    if len(set(labels) - {-1}) >= 1:
        return labels
    return np.zeros(n, dtype=int)


def cluster_kmeans(
    X: np.ndarray,
    k: int,
    random_state: int = 42,
) -> np.ndarray:
    n = X.shape[0]
    k = max(1, min(k, n))
    if k <= 1:
        return np.zeros(n, dtype=int)
    model = KMeans(n_clusters=k, random_state=random_state, n_init=10)
    return model.fit_predict(X)


def largest_cluster_ratio(labels: np.ndarray) -> float:
    valid = labels[labels >= 0]
    if len(valid) == 0:
        return 1.0
    counts = Counter(valid)
    return counts.most_common(1)[0][1] / len(valid)


def recursive_split_cluster(
    X: np.ndarray,
    max_largest_ratio: float = LARGEST_CLUSTER_SPLIT_THRESHOLD,
    k_range: tuple[int, int] = (2, 8),
    min_cluster_size: int = 30,
    random_state: int = 42,
    max_depth: int = 5,
) -> np.ndarray:
    """Recursively split the largest cluster if it exceeds max_largest_ratio."""
    n = X.shape[0]
    labels = np.zeros(n, dtype=int)
    if n < min_cluster_size * 2:
        return labels

    next_label = 1
    queue: list[tuple[np.ndarray, int]] = [(np.arange(n), 0)]

    for _depth in range(max_depth):
        new_queue: list[tuple[np.ndarray, int]] = []
        for idx, lab in queue:
            sub_X = X[idx]
            if len(idx) < min_cluster_size * 2:
                labels[idx] = lab
                continue
            sub_labels = _split_once(sub_X, k_range, min_cluster_size, random_state)
            if len(set(sub_labels)) <= 1:
                labels[idx] = lab
                continue
            ratios = Counter(sub_labels)
            largest = max(ratios.values()) / len(sub_labels)
            if largest <= max_largest_ratio:
                for sl in set(sub_labels):
                    mask = sub_labels == sl
                    sub_idx = idx[mask]
                    if lab == 0 and sl == 0:
                        labels[sub_idx] = 0
                    else:
                        assigned = lab if (lab != 0 and sl == 0) else next_label
                        if assigned == next_label and not (lab != 0 and sl == 0):
                            next_label += 1
                        labels[sub_idx] = assigned if sl == 0 else next_label
                        if sl != 0:
                            next_label += 1
                continue
            # still dominated — recurse on largest child
            maj = ratios.most_common(1)[0][0]
            for sl in set(sub_labels):
                mask = sub_labels == sl
                sub_idx = idx[mask]
                child_lab = lab if sl != maj else lab
                if sl == maj and largest > max_largest_ratio:
                    new_queue.append((sub_idx, child_lab))
                else:
                    assigned = child_lab if child_lab != 0 else next_label
                    if assigned == next_label:
                        next_label += 1
                    labels[sub_idx] = assigned
        if not new_queue:
            break
        queue = new_queue

    # assign any remaining zeros
    unassigned = np.where(labels == 0)[0]
    if len(unassigned) == n:
        labels = cluster_kmeans(X, k=min(k_range[1], max(k_range[0], n // min_cluster_size)), random_state=random_state)
    return labels


def _split_once(
    X: np.ndarray,
    k_range: tuple[int, int],
    min_cluster_size: int,
    random_state: int,
) -> np.ndarray:
    n = X.shape[0]
    if n < min_cluster_size * 2:
        return np.zeros(n, dtype=int)
    best_k = k_range[0]
    best_score = -1.0
    best_labels = np.zeros(n, dtype=int)
    for k in range(k_range[0], min(k_range[1], n // min_cluster_size) + 1):
        if k < 2:
            continue
        lab = cluster_kmeans(X, k, random_state=random_state)
        score = silhouette_safe(X, lab)
        if score is not None and score > best_score:
            best_score = score
            best_k = k
            best_labels = lab
    if best_score < 0:
        # sklearn HDBSCAN has shown native-code segfaults after many repeated
        # full-data/bootstrap fits. KMeans is deterministic and safe here.
        fallback_k = min(k_range[1], max(2, n // max(min_cluster_size, 1)))
        return cluster_kmeans(X, fallback_k, random_state=random_state)
    return best_labels if best_k >= 2 else np.zeros(n, dtype=int)


def medoid_indices(
    X: np.ndarray,
    labels: np.ndarray,
    max_sample: int = 1500,
    random_state: int = 0,
) -> dict[int, int]:
    medoids: dict[int, int] = {}
    rng = np.random.default_rng(random_state)
    for c in sorted(set(labels) - {-1}):
        idx = np.where(labels == c)[0]
        if len(idx) == 0:
            continue
        sample = rng.choice(idx, size=min(len(idx), max_sample), replace=False) if len(idx) > max_sample else idx
        D = pairwise_distances(X[sample])
        medoids[int(c)] = int(sample[int(np.argmin(D.mean(axis=1)))])
    return medoids


def bootstrap_stability(
    X: np.ndarray,
    labels: np.ndarray,
    min_cluster_size: int = 30,
    min_samples: int | None = None,
    repeats: int | None = None,
    seed: int = 42,
) -> dict[str, Any]:
    rng = np.random.default_rng(seed)
    n = X.shape[0]
    if n < 8 or len(set(labels) - {-1}) < 1:
        return {"repeats": 0, "mean_ari": None, "mean_nmi": None, "per_cluster_stability": {}}

    if repeats is None:
        repeats = 5 if n >= 5000 else 10
    sample_size = min(n, 8000 if n >= 5000 else n)

    aris: list[float] = []
    nmis: list[float] = []
    member_hits: dict[int, list[float]] = defaultdict(list)

    for _ in range(repeats):
        idx = rng.choice(n, size=sample_size, replace=True)
        uniq = np.unique(idx)
        if len(uniq) < max(4, min_cluster_size):
            continue
        mcs = max(20, int(min_cluster_size * sample_size / max(n, 1)))
        base_cluster_count = max(2, len(set(labels) - {-1}))
        bootstrap_k = min(base_cluster_count, max(2, len(uniq) // mcs))
        lab_b = cluster_kmeans(
            X[uniq],
            k=bootstrap_k,
            random_state=seed + len(aris) + len(nmis),
        )
        base = labels[uniq]
        mask = (base >= 0) & (lab_b >= 0)
        if mask.sum() >= 4 and len(set(base[mask])) > 1 and len(set(lab_b[mask])) > 1:
            aris.append(float(adjusted_rand_score(base[mask], lab_b[mask])))
            nmis.append(float(normalized_mutual_info_score(base[mask], lab_b[mask])))
        for c in set(base) - {-1}:
            sampled_pos = [i for i, u in enumerate(uniq) if base[i] == c]
            if len(sampled_pos) < 2:
                continue
            labs = lab_b[sampled_pos]
            labs = labs[labs >= 0]
            if len(labs) == 0:
                member_hits[int(c)].append(0.0)
            else:
                maj = Counter(labs).most_common(1)[0][1] / len(labs)
                member_hits[int(c)].append(float(maj))

    per = {str(c): float(np.mean(v)) if v else None for c, v in sorted(member_hits.items())}
    return {
        "repeats": repeats,
        "mean_ari": float(np.mean(aris)) if aris else None,
        "mean_nmi": float(np.mean(nmis)) if nmis else None,
        "per_cluster_stability": per,
        "retention": per,
    }


def silhouette_safe(X: np.ndarray, labels: np.ndarray) -> float | None:
    mask = labels >= 0
    if mask.sum() < 4 or len(set(labels[mask])) < 2:
        return None
    try:
        return float(silhouette_score(X[mask], labels[mask]))
    except Exception:
        return None


def calinski_harabasz_safe(X: np.ndarray, labels: np.ndarray) -> float | None:
    mask = labels >= 0
    if mask.sum() < 4 or len(set(labels[mask])) < 2:
        return None
    try:
        return float(calinski_harabasz_score(X[mask], labels[mask]))
    except Exception:
        return None


def davies_bouldin_safe(X: np.ndarray, labels: np.ndarray) -> float | None:
    mask = labels >= 0
    if mask.sum() < 4 or len(set(labels[mask])) < 2:
        return None
    try:
        return float(davies_bouldin_score(X[mask], labels[mask]))
    except Exception:
        return None


def choose_k_by_silhouette(
    X: np.ndarray,
    k_range: tuple[int, int] = (2, 8),
    random_state: int = 42,
) -> tuple[int, dict[int, float | None]]:
    scores: dict[int, float | None] = {}
    best_k = k_range[0]
    best_score = -1.0
    n = X.shape[0]
    for k in range(k_range[0], min(k_range[1], n - 1) + 1):
        if k < 2 or k >= n:
            continue
        lab = cluster_kmeans(X, k, random_state=random_state)
        sc = silhouette_safe(X, lab)
        scores[k] = sc
        if sc is not None and sc > best_score:
            best_score = sc
            best_k = k
    return best_k, scores


# ---- Compatibility aliases used by stage modules ----

def prepare_matrix(
    df,
    feature_cols: list[str],
    max_dim: int = 40,
):
    from sklearn.decomposition import TruncatedSVD
    from sklearn.preprocessing import StandardScaler

    X = df[feature_cols].fillna(0.0).to_numpy(dtype=np.float64)
    X[~np.isfinite(X)] = 0.0
    scaler = StandardScaler()
    Xs = scaler.fit_transform(X)
    svd = None
    if Xs.shape[1] > max_dim and Xs.shape[0] > max_dim + 1:
        svd = TruncatedSVD(n_components=max_dim, random_state=42)
        Xs = svd.fit_transform(Xs)
    return Xs, scaler, svd, feature_cols


def recursive_cluster(
    X: np.ndarray,
    *,
    k_range: tuple[int, int] = (2, 8),
    largest_threshold: float = LARGEST_CLUSTER_SPLIT_THRESHOLD,
    min_cluster_size: int = 30,
    seed: int = 42,
    max_depth: int = 2,
) -> np.ndarray:
    return recursive_split_cluster(
        X,
        max_largest_ratio=largest_threshold,
        k_range=k_range,
        min_cluster_size=min_cluster_size,
        random_state=seed,
        max_depth=max_depth,
    )


def cluster_metrics(X: np.ndarray, labels: np.ndarray) -> dict:
    n = X.shape[0]
    labs = set(int(x) for x in labels)
    counts = Counter(int(x) for x in labels)
    largest_ratio = (max(counts.values()) / n) if counts and n else 1.0
    return {
        "n": n,
        "n_clusters": len(labs),
        "largest_cluster_ratio": float(largest_ratio),
        "noise_ratio": 0.0,
        "silhouette": silhouette_safe(X, labels),
        "calinski_harabasz": calinski_harabasz_safe(X, labels),
        "davies_bouldin": davies_bouldin_safe(X, labels),
        "cluster_sizes": dict(sorted(counts.items())),
    }


def semantic_distinctiveness(df, labels: np.ndarray, feature_cols: list[str]) -> float:
    if len(set(labels)) < 2:
        return 0.0
    scores = []
    for c in sorted(set(int(x) for x in labels)):
        mask = labels == c
        other = ~mask
        if mask.sum() < 3 or other.sum() < 3:
            continue
        diffs = []
        for col in feature_cols:
            if col not in df.columns or col.startswith("ng_"):
                continue
            a = float(df.loc[mask, col].mean())
            b = float(df.loc[other, col].mean())
            diffs.append(abs(a - b))
        if diffs:
            scores.append(float(np.mean(sorted(diffs, reverse=True)[:10])))
    return float(np.mean(scores)) if scores else 0.0


def label_cluster_ids(matchup: str, labels: np.ndarray, prefix: str = "O") -> list[str]:
    mapping = {}
    next_i = 1
    out = []
    for lab in labels:
        lab = int(lab)
        if lab not in mapping:
            mapping[lab] = f"{matchup}_{prefix}{next_i:02d}"
            next_i += 1
        out.append(mapping[lab])
    return out
