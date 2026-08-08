"""I/O helpers for skill_mining_v2."""

from __future__ import annotations

import hashlib
import json
import math
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterator, Sequence

import numpy as np
import pandas as pd

from analysis.skill_mining_v2.config import (
    ACTION_JSON_ROOT,
    MACRO_EVENTS,
    MATCHUP_DIR_TO_FILE_MATCHUPS,
    RANDOM_SEED,
    REPO_ROOT,
    SOURCE_MATCHUP_DIRS,
    TAXONOMY_VERSION,
)
from analysis.skill_mining_v2.common.taxonomy import normalize_race

_SKIP_JSON_NAMES = frozenset(
    {"full_parse_summary.json", "parse_errors.jsonl", "summary.json"}
)


def repo_root() -> Path:
    return REPO_ROOT


def ensure_dir(path: Path | str) -> Path:
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return p


def json_safe(obj: Any) -> Any:
    """Convert non-JSON values (NaN/Inf/numpy scalars/pandas NA) into JSON-safe forms."""
    if obj is None:
        return None
    if isinstance(obj, dict):
        return {str(k): json_safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [json_safe(v) for v in obj]
    if isinstance(obj, (np.floating, float)):
        value = float(obj)
        return None if not math.isfinite(value) else value
    if isinstance(obj, (np.integer,)):
        return int(obj)
    if isinstance(obj, (np.bool_,)):
        return bool(obj)
    if isinstance(obj, np.ndarray):
        return json_safe(obj.tolist())
    try:
        if pd.isna(obj):
            return None
    except (TypeError, ValueError):
        pass
    return obj


def write_json(path: Path | str, obj: Any) -> None:
    p = Path(path)
    ensure_dir(p.parent)
    p.write_text(
        json.dumps(json_safe(obj), ensure_ascii=False, indent=2, allow_nan=False),
        encoding="utf-8",
    )


def read_json(path: Path | str) -> Any:
    text = Path(path).read_text(encoding="utf-8")
    # Repair legacy invalid tokens written by older dumps.
    text = (
        text.replace(": NaN", ": null")
        .replace(": -Infinity", ": null")
        .replace(": Infinity", ": null")
    )
    return json.loads(text)


def write_parquet(path: Path | str | None = None, df: pd.DataFrame | None = None, *args, **kwargs) -> None:
    """Write parquet. Supports write_parquet(df, path) or write_parquet(path, df)."""
    if isinstance(path, pd.DataFrame) and (df is None or isinstance(df, (str, Path))):
        # called as write_parquet(df, path)
        real_df, real_path = path, df if df is not None else (args[0] if args else kwargs.get("path"))
    else:
        real_path, real_df = path, df
        if real_df is None and args:
            real_df = args[0]
    p = Path(real_path)
    ensure_dir(p.parent)
    real_df.to_parquet(p, index=False)


def read_parquet(path: Path | str) -> pd.DataFrame:
    return pd.read_parquet(path)


def file_sha256(path: Path | str, chunk: int = 1 << 20) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        while True:
            b = f.read(chunk)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def dir_content_hash(root: Path | str, pattern: str = "*.json", max_files: int = 5000) -> str:
    root = Path(root)
    h = hashlib.sha256()
    files = sorted(root.rglob(pattern))
    h.update(str(len(files)).encode())
    for p in files[:max_files]:
        try:
            st = p.stat()
            h.update(f"{p.relative_to(root)}:{st.st_size}:{st.st_mtime_ns}".encode())
        except OSError:
            continue
    return h.hexdigest()[:32]


def git_commit(repo: Path | str | None = None) -> str:
    cwd = str(repo or REPO_ROOT)
    try:
        return subprocess.check_output(
            ["git", "rev-parse", "HEAD"],
            cwd=cwd,
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except Exception:
        return "unknown"


def filter_macro(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = []
    for ev in events:
        if ev.get("event") not in MACRO_EVENTS:
            continue
        if not isinstance(ev.get("second"), (int, float)):
            continue
        out.append(compact_action(ev))
    out.sort(key=lambda x: (float(x["second"]) if x.get("second") is not None else 1e18))
    return out


def actions_before(actions: list[dict[str, Any]], t: float) -> list[dict[str, Any]]:
    return [a for a in actions if a.get("second") is not None and float(a["second"]) <= t]


def actions_between(actions: list[dict[str, Any]], t0: float, t1: float) -> list[dict[str, Any]]:
    out = []
    for a in actions:
        s = a.get("second")
        if s is None:
            continue
        s = float(s)
        if t0 < s <= t1:
            out.append(a)
    return out


def dumps_actions(actions: list[dict[str, Any]]) -> str:
    return json.dumps(actions, ensure_ascii=False, separators=(",", ":"))


def estimate_tokens(obj: Any) -> int:
    text = obj if isinstance(obj, str) else json.dumps(obj, ensure_ascii=False)
    return max(1, len(text) // 4)


def iter_action_json_files(action_root: Path | str | None = None) -> Iterator[tuple[str, Path]]:
    yield from iter_replay_files(action_root=action_root)


def stage_dir(output_root: Path | str, stage_name: str) -> Path:
    return ensure_dir(Path(output_root) / stage_name)


def loads_actions(raw: Any) -> list[dict[str, Any]]:
    """Deserialize action lists stored as JSON string, bytes, or list."""
    if raw is None:
        return []
    if isinstance(raw, list):
        return [a if isinstance(a, dict) else compact_action(a) for a in raw]
    if isinstance(raw, (bytes, bytearray)):
        raw = raw.decode("utf-8")
    if isinstance(raw, str):
        parsed = json.loads(raw)
        if isinstance(parsed, list):
            return [a if isinstance(a, dict) else compact_action(a) for a in parsed]
    return []


def compact_action(ev: dict[str, Any]) -> dict[str, Any]:
    """Normalize a build-order event to the minimal macro schema."""
    second = ev.get("second")
    return {
        "second": float(second) if isinstance(second, (int, float)) else None,
        "event": ev.get("event"),
        "name": ev.get("standard_result_name") or ev.get("name"),
        "ability": ev.get("standard_action_name") or ev.get("ability"),
        "type": ev.get("standard_result_type"),
        "standard_action_name": ev.get("standard_action_name"),
        "standard_result_name": ev.get("standard_result_name"),
    }


def race_letter(race: str | None) -> str | None:
    if race is None:
        return None
    mapping = {"Terran": "T", "Protoss": "P", "Zerg": "Z"}
    return mapping.get(str(race).strip(), None)


def race_from_letter(letter: str | None) -> str | None:
    if letter is None:
        return None
    mapping = {"T": "Terran", "P": "Protoss", "Z": "Zerg"}
    return mapping.get(letter.upper())


def directional_matchup(race: str | None, opponent_race: str | None) -> str | None:
    """Return directional matchup code like TvP."""
    r = race_letter(normalize_race(race) or race)
    o = race_letter(normalize_race(opponent_race) or opponent_race)
    if r is None or o is None:
        return None
    return f"{r}v{o}"


def file_matchup_for_directional(dm: str) -> str | None:
    """Map directional matchup to on-disk directory name."""
    if len(dm) != 3 or dm[1] != "v":
        return None
    own, opp = dm[0], dm[2]
    direct = f"{own}v{opp}"
    if direct in MATCHUP_DIR_TO_FILE_MATCHUPS:
        return direct
    reverse_map = {"TvP": "PvT", "ZvP": "PvZ", "ZvT": "TvZ"}
    return reverse_map.get(dm)


def _should_skip_json(path: Path) -> bool:
    name = path.name
    if name in _SKIP_JSON_NAMES or name.endswith("_summary.json"):
        return True
    if name.startswith("summary"):
        return True
    return False


def iter_replay_files(
    action_root: Path | str | None = None,
    file_matchups: Sequence[str] | None = None,
    limit: int | None = None,
) -> Iterator[tuple[str, Path]]:
    """Yield (file_matchup_dir, path) for replay JSON files."""
    root = Path(action_root) if action_root is not None else ACTION_JSON_ROOT
    dirs = file_matchups or SOURCE_MATCHUP_DIRS
    count = 0
    for matchup in dirs:
        d = root / matchup
        if not d.is_dir():
            continue
        for path in sorted(d.glob("*.json")):
            if _should_skip_json(path):
                continue
            yield matchup, path
            count += 1
            if limit is not None and count >= limit:
                return


def load_replay(path: Path | str) -> dict[str, Any]:
    return read_json(path)


def save_run_manifest_sidecar(
    output_dir: Path | str,
    run_id: str,
    extra: dict[str, Any] | None = None,
) -> Path:
    """Write run_manifest.json under a stage output directory."""
    out = Path(output_dir)
    ensure_dir(out)

    def _git_commit() -> str | None:
        try:
            return (
                subprocess.check_output(
                    ["git", "rev-parse", "HEAD"],
                    cwd=repo_root(),
                    stderr=subprocess.DEVNULL,
                    text=True,
                )
                .strip()
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None

    def _file_hash(path: Path) -> str | None:
        if not path.is_file():
            return None
        h = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(1 << 20), b""):
                h.update(chunk)
        return h.hexdigest()

    manifest: dict[str, Any] = {
        "run_id": run_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "git_commit": _git_commit(),
        "random_seed": RANDOM_SEED,
        "taxonomy_version": TAXONOMY_VERSION,
        "dataset_hash": _file_hash(ACTION_JSON_ROOT / "PvT" / "full_parse_summary.json"),
    }
    if extra:
        manifest.update(extra)
    path = out / "run_manifest.json"
    write_json(path, manifest)
    return path

