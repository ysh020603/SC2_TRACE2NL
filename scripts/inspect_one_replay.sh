#!/usr/bin/env bash
set -euo pipefail
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

REPLAY="${1:-}"
if [[ -z "$REPLAY" ]]; then
  REPLAY="$(find data/replays/sc2reader_official data/replays/human_tournament \
    -iname '*.SC2Replay' 2>/dev/null | sort | head -n 1 || true)"
fi
if [[ -z "$REPLAY" ]]; then
  echo "No replay found under data/replays/"
  exit 1
fi
sc2mine inspect "$REPLAY"
