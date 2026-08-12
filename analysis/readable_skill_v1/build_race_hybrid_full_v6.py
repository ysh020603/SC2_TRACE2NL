"""Compile Full-v6 from the empirically stable v3/v4 race-matchup branches.

The selection is intentionally coarse and mechanistic: failure-aware v4 is retained
for Terran and Protoss mirrors, where its execution contract helped, while the
contrastive v3 graph is retained for other Protoss matchups and all Zerg openings,
where universal facility/clock thresholds caused negative transfer.
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path
from typing import Any


V3_METHOD = "full_contrastive_graph_v3"
V4_METHOD = "full_failure_aware_graph_v4"
OUTPUT_METHOD = "full_race_hybrid_graph_v6"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    temp.replace(path)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + ".tmp")
    temp.write_text(text.rstrip() + "\n", encoding="utf-8")
    temp.replace(path)


def use_v4(opening_id: str) -> bool:
    return opening_id.startswith("T") or opening_id.startswith("PvP_")


def opening_paths(root: Path) -> dict[str, Path]:
    return {path.parent.name: path.parent for path in root.glob("*/*/*/SKILL.md")}


def compile_one(repo_root: Path, output_root: Path, opening_id: str) -> dict[str, str]:
    source_method = V4_METHOD if use_v4(opening_id) else V3_METHOD
    candidates = opening_paths(repo_root / "SKILL_MINING_V2_READABLE" / source_method)
    source = candidates[opening_id]
    destination = output_root / source.relative_to(source.parents[2])
    if destination.exists():
        shutil.rmtree(destination)
    shutil.copytree(source, destination)

    index_path = destination / "index.json"
    index = read_json(index_path)
    index["method"] = OUTPUT_METHOD
    write_json(index_path, index)

    root_path = destination / "SKILL.md"
    root = root_path.read_text(encoding="utf-8")
    root = root.replace("- Method: Failure-Aware Full V4", "- Method: Race-Hybrid Full V6")
    root = root.replace("- Method: Contrastive Full V3", "- Method: Race-Hybrid Full V6")
    write_text(root_path, root)

    provenance = destination / "provenance"
    provenance.mkdir(exist_ok=True)
    write_json(provenance / "race_hybrid_selection.json", {
        "schema_version": 1,
        "method": OUTPUT_METHOD,
        "opening_id": opening_id,
        "source_method": source_method,
        "agent_visible": False,
        "selection_policy": "v4_for_terran_and_pvp_else_v3",
    })
    return {"opening_id": opening_id, "source_method": source_method}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    parser.add_argument("--openings", default="")
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()
    v3 = opening_paths(repo_root / "SKILL_MINING_V2_READABLE" / V3_METHOD)
    v4 = opening_paths(repo_root / "SKILL_MINING_V2_READABLE" / V4_METHOD)
    if set(v3) != set(v4):
        raise ValueError("v3/v4 opening catalogs differ")
    ids = sorted(v3)
    if args.openings:
        requested = {x.strip() for x in args.openings.split(",") if x.strip()}
        ids = [x for x in ids if x in requested]
        if set(ids) != requested:
            raise ValueError(f"unknown openings: {sorted(requested - set(ids))}")
    output_root = repo_root / "SKILL_MINING_V2_READABLE" / OUTPUT_METHOD
    rows = [compile_one(repo_root, output_root, opening_id) for opening_id in ids]
    summary = {
        "schema_version": 1,
        "method": OUTPUT_METHOD,
        "selection_policy": "v4_for_terran_and_pvp_else_v3",
        "skills": len(rows),
        "source_counts": {
            V3_METHOD: sum(x["source_method"] == V3_METHOD for x in rows),
            V4_METHOD: sum(x["source_method"] == V4_METHOD for x in rows),
        },
    }
    result_root = repo_root / "analysis/outputs_readable_skill_v1/11_full_race_hybrid_v6"
    write_json(result_root / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
