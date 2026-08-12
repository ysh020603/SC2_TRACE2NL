"""Copy the branch-faithful graph for v8 executable-queue integration."""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path


BASE_METHOD = "full_branch_faithful_graph_v7"
OUTPUT_METHOD = "full_executable_graph_v8"


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
    temporary.replace(path)


def opening_paths(root: Path) -> dict[str, Path]:
    return {path.parent.name: path.parent for path in root.glob("*/*/*/SKILL.md")}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", type=Path, default=Path(__file__).resolve().parents[2])
    args = parser.parse_args()
    repo_root = args.repo_root.resolve()
    base_root = repo_root / "SKILL_MINING_V2_READABLE" / BASE_METHOD
    output_root = repo_root / "SKILL_MINING_V2_READABLE" / OUTPUT_METHOD
    rows = []
    for opening_id, source in sorted(opening_paths(base_root).items()):
        destination = output_root / source.relative_to(source.parents[2])
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(source, destination)
        index_path = destination / "index.json"
        index = json.loads(index_path.read_text(encoding="utf-8"))
        index["method"] = OUTPUT_METHOD
        write_json(index_path, index)
        root_path = destination / "SKILL.md"
        root = root_path.read_text(encoding="utf-8").replace(
            "- Method: Branch-Faithful Full V7", "- Method: Executable Full V8"
        )
        root_path.write_text(root, encoding="utf-8")
        provenance = destination / "provenance"
        provenance.mkdir(exist_ok=True)
        write_json(provenance / "executable_integration.json", {
            "schema_version": 1,
            "method": OUTPUT_METHOD,
            "opening_id": opening_id,
            "base_method": BASE_METHOD,
            "agent_visible": False,
            "runtime_invariants": [
                "ordered_tech_prerequisites",
                "zerg_larva_defense_allocation",
                "terran_bank_to_production",
                "race_specific_supply_precision",
            ],
        })
        rows.append(opening_id)
    summary = {"schema_version": 1, "method": OUTPUT_METHOD, "base_method": BASE_METHOD, "skills": len(rows)}
    write_json(repo_root / "analysis/outputs_readable_skill_v1/13_full_executable_v8/summary.json", summary)
    print(json.dumps(summary, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
