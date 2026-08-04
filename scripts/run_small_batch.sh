#!/usr/bin/env bash
set -euo pipefail
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

CATEGORY="${1:-sc2reader_official}"
WORKERS="${WORKERS:-4}"

sc2mine parse-dir --category "$CATEGORY" --workers "$WORKERS"
sc2mine report "data/artifacts/$CATEGORY"
echo "Batch complete -> data/artifacts/$CATEGORY and data/full_json/$CATEGORY"
