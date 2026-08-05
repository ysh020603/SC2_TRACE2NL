#!/usr/bin/env python3
"""Extract Blizzard replay ZIPs and organize by AssignedRace matchup."""

from __future__ import annotations

import argparse
import io
import json
import os
import shutil
import sys
import time
import zipfile
from collections import Counter
from pathlib import Path

import mpyq

RACE = {"Prot": "P", "Terr": "T", "Zerg": "Z"}
MATCHUP_NAME = {
    "PP": "PvP",
    "PT": "PvT",
    "PZ": "PvZ",
    "TT": "TvT",
    "TZ": "TvZ",
    "ZZ": "ZvZ",
}
ZIP_PASSWORD = b"iagreetotheeula"


def race_code(value: str | None) -> str:
    if not value:
        return "?"
    return RACE.get(value, value[:1] if value else "?")


def unordered_matchup(r1: str, r2: str) -> str:
    return "".join(sorted([r1, r2]))


def parse_assigned_matchup(data: bytes) -> str:
    archive = mpyq.MPQArchive(io.BytesIO(data)).extract()
    meta = json.loads(archive[b"replay.gamemetadata.json"].decode("utf-8"))
    players = sorted(meta.get("Players", []), key=lambda p: p.get("PlayerID", 0))
    if len(players) < 2:
        raise ValueError(f"expected 2 players, got {len(players)}")
    r1 = race_code(players[0].get("AssignedRace") or players[0].get("SelectedRace"))
    r2 = race_code(players[1].get("AssignedRace") or players[1].get("SelectedRace"))
    key = unordered_matchup(r1, r2)
    if key not in MATCHUP_NAME:
        raise ValueError(f"unsupported matchup {key} from {r1}/{r2}")
    return MATCHUP_NAME[key]


def iter_nonempty_zips(zip_dir: Path) -> list[Path]:
    zips = sorted(zip_dir.glob("*.zip"))
    out = []
    for path in zips:
        if path.stat().st_size <= 22:
            continue
        out.append(path)
    return out


def extract_and_organize(
    zip_dir: Path,
    out_dir: Path,
    staging_dir: Path,
    limit_per_zip: int | None = None,
) -> dict:
    matchup_dir = out_dir / "by_matchup"
    for name in MATCHUP_NAME.values():
        (matchup_dir / name).mkdir(parents=True, exist_ok=True)
    staging_dir.mkdir(parents=True, exist_ok=True)

    stats = {
        "source_zip_dir": str(zip_dir),
        "output_dir": str(out_dir),
        "started_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "zips": [],
        "matchup_counts": Counter(),
        "duplicate_skipped": 0,
        "parse_errors": 0,
        "written": 0,
        "error_samples": [],
    }

    zips = iter_nonempty_zips(zip_dir)
    print(f"Non-empty ZIPs: {len(zips)}", flush=True)

    seen_names: set[str] = set()
    # Resume support: preexisting files count as seen.
    for name in MATCHUP_NAME.values():
        for existing in (matchup_dir / name).glob("*.SC2Replay"):
            seen_names.add(existing.name)

    for zi, zip_path in enumerate(zips, 1):
        zip_stat = {
            "zip": zip_path.name,
            "size_bytes": zip_path.stat().st_size,
            "members": 0,
            "written": 0,
            "duplicate_skipped": 0,
            "parse_errors": 0,
            "matchups": Counter(),
        }
        print(f"[{zi}/{len(zips)}] {zip_path.name}", flush=True)

        with zipfile.ZipFile(zip_path) as zf:
            members = [
                info
                for info in zf.infolist()
                if (not info.is_dir()) and info.filename.lower().endswith(".sc2replay")
            ]
            zip_stat["members"] = len(members)
            if limit_per_zip is not None:
                members = members[:limit_per_zip]

            for mi, info in enumerate(members, 1):
                base = Path(info.filename).name
                if base in seen_names:
                    zip_stat["duplicate_skipped"] += 1
                    stats["duplicate_skipped"] += 1
                    continue
                try:
                    data = zf.read(info.filename, pwd=ZIP_PASSWORD)
                    matchup = parse_assigned_matchup(data)
                    dest = matchup_dir / matchup / base
                    with open(dest, "wb") as fout:
                        fout.write(data)
                    seen_names.add(base)
                    zip_stat["written"] += 1
                    zip_stat["matchups"][matchup] += 1
                    stats["written"] += 1
                    stats["matchup_counts"][matchup] += 1
                except Exception as exc:  # noqa: BLE001 - batch robustness
                    zip_stat["parse_errors"] += 1
                    stats["parse_errors"] += 1
                    if len(stats["error_samples"]) < 20:
                        stats["error_samples"].append(
                            {
                                "zip": zip_path.name,
                                "file": base,
                                "error": f"{type(exc).__name__}: {exc}",
                            }
                        )
                if mi % 500 == 0 or mi == len(members):
                    print(
                        f"  {mi}/{len(members)} written={zip_stat['written']} "
                        f"dup={zip_stat['duplicate_skipped']} err={zip_stat['parse_errors']}",
                        flush=True,
                    )

        zip_stat["matchups"] = dict(zip_stat["matchups"])
        stats["zips"].append(zip_stat)

    stats["finished_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
    stats["matchup_counts"] = dict(stats["matchup_counts"])
    stats["unique_replays"] = len(seen_names)
    return stats


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--zip-dir",
        default="/data2/wyq/2026_02/mini-AlphaStar/scripts/download_replay/third/download",
    )
    parser.add_argument(
        "--out-dir",
        default="/data2/shy_2608/SC2trace2nl/raw_data",
    )
    parser.add_argument("--limit-per-zip", type=int, default=None)
    args = parser.parse_args()

    zip_dir = Path(args.zip_dir)
    out_dir = Path(args.out_dir)
    staging_dir = out_dir / "_staging"
    out_dir.mkdir(parents=True, exist_ok=True)

    if not zip_dir.is_dir():
        print(f"ZIP dir not found: {zip_dir}", file=sys.stderr)
        return 1

    t0 = time.time()
    stats = extract_and_organize(
        zip_dir=zip_dir,
        out_dir=out_dir,
        staging_dir=staging_dir,
        limit_per_zip=args.limit_per_zip,
    )
    stats["elapsed_sec"] = round(time.time() - t0, 1)

    manifest_path = out_dir / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(stats, f, ensure_ascii=False, indent=2)

    # cleanup staging if empty
    if staging_dir.exists() and not any(staging_dir.iterdir()):
        staging_dir.rmdir()
    elif staging_dir.exists():
        shutil.rmtree(staging_dir, ignore_errors=True)

    print(json.dumps({k: stats[k] for k in ("written", "duplicate_skipped", "parse_errors", "matchup_counts", "elapsed_sec")}, ensure_ascii=False, indent=2))
    print(f"Wrote {manifest_path}")
    return 0 if stats["parse_errors"] == 0 else 2


if __name__ == "__main__":
    raise SystemExit(main())
