#!/usr/bin/env bash
# Download official sc2reader test_replays into data/replays/sc2reader_official.
set -euo pipefail

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

VERSION="${1:-5.0.15}"
OUTPUT_DIR="${2:-data/replays/sc2reader_official}"
mkdir -p "$OUTPUT_DIR" vendor

python - "$VERSION" "$OUTPUT_DIR" <<'PY'
import base64
import json
import pathlib
import sys
import time
import urllib.request

version, output_dir = sys.argv[1], pathlib.Path(sys.argv[2])
repo = "ggtracker/sc2reader"
ref = "upstream"
api_root = f"https://api.github.com/repos/{repo}"
headers = {
    "Accept": "application/vnd.github+json",
    "User-Agent": "sc2-replay-miner",
    "X-GitHub-Api-Version": "2022-11-28",
}


def get_json(url: str, attempts: int = 5) -> object:
    for attempt in range(attempts):
        try:
            request = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(request, timeout=180) as response:
                return json.load(response)
        except (OSError, TimeoutError):
            if attempt + 1 == attempts:
                raise
            time.sleep(2 * (attempt + 1))
    raise RuntimeError("unreachable")


directory_url = f"{api_root}/contents/test_replays/{version}?ref={ref}"
entries = get_json(directory_url)
if not isinstance(entries, list):
    raise RuntimeError(f"Unexpected GitHub response for {directory_url}")

count = 0
for entry in entries:
    if (
        not isinstance(entry, dict)
        or entry.get("type") != "file"
        or not str(entry.get("name", "")).lower().endswith(".sc2replay")
    ):
        continue
    metadata = get_json(str(entry["url"]))
    if not isinstance(metadata, dict) or metadata.get("encoding") != "base64":
        raise RuntimeError(f"Missing base64 content for {entry['name']}")
    payload = base64.b64decode(str(metadata["content"]).replace("\n", ""))
    expected_size = int(entry["size"])
    if len(payload) != expected_size:
        raise RuntimeError(
            f"Size mismatch for {entry['name']}: {len(payload)} != {expected_size}"
        )
    target = output_dir / str(entry["name"])
    target.write_bytes(payload)
    print(f"downloaded {target}: {len(payload)} bytes")
    count += 1

commit = get_json(f"{api_root}/commits/{ref}")
if not isinstance(commit, dict) or "sha" not in commit:
    raise RuntimeError("Could not resolve upstream commit")
pathlib.Path("vendor/sc2reader.commit.txt").write_text(
    str(commit["sha"]) + "\n", encoding="utf-8"
)
print(f"Downloaded {count} replay(s); upstream commit={commit['sha']}")
PY
