"""Plotting helpers for skill_mining_v2 (Agg backend, png+pdf export)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from analysis.skill_mining_v2.common.io import ensure_dir, write_json
from analysis.skill_mining_v2.config import FIGURE_DPI


def save_figure(fig: plt.Figure, out_stem: Path | str, dpi: int = FIGURE_DPI) -> tuple[Path, Path]:
    stem = Path(out_stem)
    ensure_dir(stem.parent)
    png = stem.with_suffix(".png")
    pdf = stem.with_suffix(".pdf")
    fig.savefig(png, dpi=dpi, bbox_inches="tight")
    fig.savefig(pdf, bbox_inches="tight")
    plt.close(fig)
    return png, pdf


def save_plot_data(data: pd.DataFrame | dict[str, Any], out_path: Path | str) -> Path:
    p = Path(out_path)
    ensure_dir(p.parent)
    if isinstance(data, pd.DataFrame):
        data.to_csv(p, index=False)
    else:
        if p.suffix == ".json":
            write_json(p, data)
        else:
            p.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    return p


def _embed_2d(X: np.ndarray, random_state: int = 42) -> np.ndarray:
    try:
        import umap

        reducer = umap.UMAP(n_components=2, random_state=random_state, n_neighbors=15, min_dist=0.1)
        return reducer.fit_transform(X)
    except Exception:
        from sklearn.decomposition import PCA

        k = min(2, X.shape[1], max(1, X.shape[0] - 1))
        return PCA(n_components=k, random_state=random_state).fit_transform(X)


def plot_window_metrics(
    df: pd.DataFrame,
    out_stem: Path | str,
    x_col: str = "window",
    metrics: list[str] | None = None,
) -> tuple[Path, Path]:
    metrics = metrics or [c for c in df.columns if c != x_col and pd.api.types.is_numeric_dtype(df[c])]
    fig, ax = plt.subplots(figsize=(8, 5))
    for m in metrics:
        ax.plot(df[x_col], df[m], marker="o", label=m)
    ax.set_xlabel(x_col)
    ax.set_ylabel("metric")
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)
    return save_figure(fig, out_stem)


def plot_largest_cluster_ratio(
    df: pd.DataFrame,
    out_stem: Path | str,
    x_col: str = "window",
    y_col: str = "largest_cluster_ratio",
) -> tuple[Path, Path]:
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(df[x_col], df[y_col], marker="s", color="tab:red")
    ax.axhline(0.6, color="gray", linestyle="--", label="60% threshold")
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.legend()
    ax.grid(True, alpha=0.3)
    return save_figure(fig, out_stem)


def plot_window_similarity_heatmap(
    matrix: np.ndarray,
    labels: list[str],
    out_stem: Path | str,
) -> tuple[Path, Path]:
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(matrix, aspect="auto", cmap="viridis")
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_yticklabels(labels)
    fig.colorbar(im, ax=ax)
    ax.set_title("Window similarity")
    return save_figure(fig, out_stem)


def plot_pca_scatter_clusters(
    X: np.ndarray,
    labels: np.ndarray,
    out_stem: Path | str,
    title: str = "Cluster embedding",
) -> tuple[Path, Path]:
    coords = _embed_2d(X)
    fig, ax = plt.subplots(figsize=(7, 6))
    scatter = ax.scatter(coords[:, 0], coords[:, 1], c=labels, cmap="tab20", s=8, alpha=0.7)
    fig.colorbar(scatter, ax=ax, label="cluster")
    ax.set_title(title)
    ax.set_xlabel("dim 1")
    ax.set_ylabel("dim 2")
    return save_figure(fig, out_stem)


def plot_feature_heatmap(
    df: pd.DataFrame,
    out_stem: Path | str,
    row_col: str = "cluster",
    feature_cols: list[str] | None = None,
) -> tuple[Path, Path]:
    feature_cols = feature_cols or [c for c in df.columns if c != row_col and pd.api.types.is_numeric_dtype(df[c])]
    pivot = df.groupby(row_col)[feature_cols].mean()
    fig, ax = plt.subplots(figsize=(max(6, len(feature_cols) * 0.35), max(4, len(pivot) * 0.4)))
    im = ax.imshow(pivot.to_numpy(), aspect="auto", cmap="coolwarm")
    ax.set_xticks(range(len(feature_cols)))
    ax.set_xticklabels(feature_cols, rotation=90, fontsize=7)
    ax.set_yticks(range(len(pivot)))
    ax.set_yticklabels(pivot.index.astype(str))
    fig.colorbar(im, ax=ax)
    ax.set_title("Feature enrichment heatmap")
    return save_figure(fig, out_stem)


def plot_transition_matrix(
    matrix: np.ndarray,
    from_labels: list[str],
    to_labels: list[str],
    out_stem: Path | str,
    title: str = "Transition matrix",
) -> tuple[Path, Path]:
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(matrix, aspect="auto", cmap="Blues")
    ax.set_xticks(range(len(to_labels)))
    ax.set_yticks(range(len(from_labels)))
    ax.set_xticklabels(to_labels, rotation=45, ha="right", fontsize=7)
    ax.set_yticklabels(from_labels, fontsize=7)
    fig.colorbar(im, ax=ax)
    ax.set_title(title)
    ax.set_xlabel("to")
    ax.set_ylabel("from")
    return save_figure(fig, out_stem)


def plot_value_heatmap(
    df: pd.DataFrame,
    out_stem: Path | str,
    row_col: str,
    col_col: str,
    value_col: str = "adjusted_lift",
) -> tuple[Path, Path]:
    pivot = df.pivot_table(index=row_col, columns=col_col, values=value_col, aggfunc="mean")
    fig, ax = plt.subplots(figsize=(max(6, pivot.shape[1] * 0.5), max(4, pivot.shape[0] * 0.4)))
    im = ax.imshow(pivot.fillna(0).to_numpy(), aspect="auto", cmap="RdBu_r", vmin=-0.1, vmax=0.1)
    ax.set_xticks(range(pivot.shape[1]))
    ax.set_yticks(range(pivot.shape[0]))
    ax.set_xticklabels(pivot.columns.astype(str), rotation=45, ha="right", fontsize=7)
    ax.set_yticklabels(pivot.index.astype(str), fontsize=7)
    fig.colorbar(im, ax=ax)
    ax.set_title("Adjusted win lift")
    return save_figure(fig, out_stem)


def plot_lift_forest(
    df: pd.DataFrame,
    out_stem: Path | str,
    label_col: str = "response_id",
    lift_col: str = "adjusted_lift",
    lo_col: str = "ci_low",
    hi_col: str = "ci_high",
) -> tuple[Path, Path]:
    sub = df.sort_values(lift_col)
    y = np.arange(len(sub))
    fig, ax = plt.subplots(figsize=(7, max(4, len(sub) * 0.25)))
    ax.errorbar(
        sub[lift_col],
        y,
        xerr=[
            sub[lift_col] - sub[lo_col].fillna(sub[lift_col]),
            sub[hi_col].fillna(sub[lift_col]) - sub[lift_col],
        ],
        fmt="o",
        capsize=3,
    )
    ax.axvline(0, color="gray", linestyle="--")
    ax.set_yticks(y)
    ax.set_yticklabels(sub[label_col].astype(str))
    ax.set_xlabel("Adjusted lift")
    ax.set_title("Response lift forest plot")
    ax.grid(True, axis="x", alpha=0.3)
    return save_figure(fig, out_stem)


# ---- Compatibility wrappers used by stage modules ----

def embed_2d(X: np.ndarray, seed: int = 42) -> np.ndarray:
    z = _embed_2d(X, random_state=seed)
    if z.ndim == 1:
        z = z.reshape(-1, 1)
    if z.shape[1] == 1:
        z = np.hstack([z, np.zeros((len(z), 1))])
    return z


def plot_opening_window_metrics(df: pd.DataFrame, out_dir: Path, data_dir: Path) -> None:
    if df is None or df.empty:
        return
    ensure_dir(data_dir)
    df.to_csv(Path(data_dir) / "opening_window_plot.csv", index=False)
    metrics = [c for c in ["silhouette", "stability_ari", "leakage", "largest_cluster_ratio", "opening_score"] if c in df.columns]
    if not metrics:
        return
    # aggregate mean across matchups
    agg = df.groupby("window")[metrics].mean().reset_index()
    plot_window_metrics(agg, Path(out_dir) / "opening_window_metrics", x_col="window", metrics=metrics)


def plot_largest_cluster_ratio(df: pd.DataFrame, out_dir: Path | None = None, data_dir: Path | None = None, **kwargs) -> Any:
    # support both new and stage signatures
    if out_dir is not None and isinstance(df, pd.DataFrame) and "directional_matchup" in df.columns:
        ensure_dir(out_dir)
        if data_dir is not None:
            ensure_dir(data_dir)
            df[["window", "directional_matchup", "largest_cluster_ratio"]].to_csv(
                Path(data_dir) / "largest_cluster_ratio.csv", index=False
            )
        fig, ax = plt.subplots(figsize=(8, 5))
        for mu, g in df.groupby("directional_matchup"):
            ax.plot(g["window"], g["largest_cluster_ratio"], marker="o", label=str(mu))
        ax.axhline(0.6, color="gray", ls="--", lw=1)
        ax.legend(fontsize=7, ncol=3)
        ax.set_xlabel("opening window (s)")
        ax.set_ylabel("largest cluster ratio")
        return save_figure(fig, Path(out_dir) / "largest_cluster_ratio")
    # original signature: (df, out_stem, ...)
    out_stem = out_dir if out_dir is not None else kwargs.get("out_stem")
    return plot_window_metrics  # noqa — fallback unused


def plot_window_similarity_heatmap(sim, out_dir=None, data_dir=None, name: str = "window_similarity_nmi", labels=None, out_stem=None, matrix=None):
    if isinstance(sim, pd.DataFrame):
        mat = sim.to_numpy(dtype=float)
        labs = [str(x) for x in sim.index.tolist()]
        stem = Path(out_dir) / name if out_dir is not None else Path(out_stem)
        if data_dir is not None:
            ensure_dir(data_dir)
            sim.reset_index().to_csv(Path(data_dir) / f"{name}.csv", index=False)
        return plot_window_similarity_heatmap.__wrapped(mat, labs, stem) if False else _heatmap_windows(mat, labs, stem)
    # ndarray path
    return _heatmap_windows(sim, labels or [], Path(out_stem or out_dir))


def _heatmap_windows(matrix, labels, out_stem):
    fig, ax = plt.subplots(figsize=(6, 5))
    im = ax.imshow(np.asarray(matrix, dtype=float), aspect="auto", cmap="viridis")
    ax.set_xticks(range(len(labels)))
    ax.set_yticks(range(len(labels)))
    ax.set_xticklabels(labels, rotation=45, ha="right")
    ax.set_yticklabels(labels)
    fig.colorbar(im, ax=ax)
    ax.set_title("Window similarity")
    return save_figure(fig, out_stem)


def plot_embedding_scatter(xy, labels, out_dir, name, title: str = ""):
    ensure_dir(out_dir)
    fig, ax = plt.subplots(figsize=(7, 6))
    labs = np.asarray(labels)
    uniq = sorted(set(labs.tolist()))
    cmap = plt.get_cmap("tab20")
    for i, lab in enumerate(uniq):
        mask = labs == lab
        ax.scatter(xy[mask, 0], xy[mask, 1], s=8, alpha=0.6, color=cmap(i % 20), label=str(lab))
    if len(uniq) <= 15:
        ax.legend(fontsize=6, markerscale=2)
    ax.set_title(title or name)
    return save_figure(fig, Path(out_dir) / name)


def plot_feature_heatmap(mat, out_dir=None, data_dir=None, name: str = "feature_heatmap", title: str = "", **kwargs):
    if isinstance(mat, pd.DataFrame) and out_dir is not None and "row_col" not in kwargs:
        ensure_dir(out_dir)
        if data_dir is not None:
            ensure_dir(data_dir)
            mat.reset_index().to_csv(Path(data_dir) / f"{name}.csv", index=False)
        fig, ax = plt.subplots(figsize=(max(6, mat.shape[1] * 0.5), max(4, mat.shape[0] * 0.4)))
        im = ax.imshow(mat.to_numpy(dtype=float), aspect="auto", cmap="RdBu_r")
        ax.set_xticks(range(mat.shape[1]))
        ax.set_xticklabels([str(c) for c in mat.columns], rotation=90, fontsize=7)
        ax.set_yticks(range(mat.shape[0]))
        ax.set_yticklabels([str(i) for i in mat.index], fontsize=7)
        fig.colorbar(im, ax=ax)
        ax.set_title(title or name)
        return save_figure(fig, Path(out_dir) / name)
    # original signature path
    return save_figure(plt.figure(), Path(out_dir or "." ) / "noop")


def plot_transition_matrix(mat, out_dir=None, data_dir=None, name: str = "transition_matrix", title: str = "", **kwargs):
    if isinstance(mat, pd.DataFrame):
        return plot_feature_heatmap(mat, out_dir=out_dir, data_dir=data_dir, name=name, title=title)
    from_labels = kwargs.get("from_labels") or []
    to_labels = kwargs.get("to_labels") or []
    out_stem = kwargs.get("out_stem") or (Path(out_dir) / name if out_dir else "transition_matrix")
    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(np.asarray(mat), aspect="auto", cmap="Blues")
    ax.set_xticks(range(len(to_labels)))
    ax.set_yticks(range(len(from_labels)))
    ax.set_xticklabels(to_labels, rotation=45, ha="right", fontsize=7)
    ax.set_yticklabels(from_labels, fontsize=7)
    fig.colorbar(im, ax=ax)
    ax.set_title(title)
    return save_figure(fig, out_stem)


def plot_value_heatmap(mat, out_dir=None, data_dir=None, name: str = "transition_value_heatmap", **kwargs):
    if isinstance(mat, pd.DataFrame) and out_dir is not None and "row_col" not in kwargs:
        return plot_feature_heatmap(mat, out_dir=out_dir, data_dir=data_dir, name=name, title="Adjusted Win Lift")
    # original
    return plot_feature_heatmap(mat, out_dir=out_dir, data_dir=data_dir, name=name)


def plot_forest(df: pd.DataFrame, out_dir: Path, data_dir: Path, name: str = "response_forest") -> None:
    ensure_dir(out_dir)
    if data_dir is not None:
        ensure_dir(data_dir)
        df.to_csv(Path(data_dir) / f"{name}.csv", index=False)
    d = df.head(30).copy()
    if "ci_low" not in d.columns:
        d["ci_low"] = d["adjusted_lift"] - d.get("lift_ci", 0.02)
        d["ci_high"] = d["adjusted_lift"] + d.get("lift_ci", 0.02)
    label_col = "label" if "label" in d.columns else ("response_id" if "response_id" in d.columns else d.columns[0])
    plot_lift_forest(d, Path(out_dir) / name, label_col=label_col)


def plot_graph_summary(nodes, edges, out_path: Path) -> None:
    ensure_dir(Path(out_path).parent)
    by_t = {}
    for n in nodes:
        by_t.setdefault(n.get("time", 0), []).append(n)
    times = sorted(by_t)
    pos = {}
    fig, ax = plt.subplots(figsize=(12, 7))
    for xi, t in enumerate(times):
        for yi, n in enumerate(by_t[t]):
            pos[n["id"]] = (xi, yi)
            ax.scatter(xi, yi, s=120, c="#4C78A8")
            ax.text(xi, yi + 0.15, str(n.get("label", n["id"]))[:28], fontsize=6, ha="center")
    colors = {"preferred": "#2ca02c", "harmful": "#d62728", "default": "#7f7f7f", "uncertain": "#ff7f0e"}
    for e in edges:
        s, t = e.get("source"), e.get("target")
        if s not in pos or t not in pos:
            continue
        x0, y0 = pos[s]
        x1, y1 = pos[t]
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="->", color=colors.get(e.get("edge_label"), "#333"), lw=1.2))
    ax.set_xticks(range(len(times)))
    ax.set_xticklabels([str(t) for t in times])
    ax.set_yticks([])
    ax.set_title(Path(out_path).stem)
    save_figure(fig, out_path)
