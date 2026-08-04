# archive/local_ai_logs

Archived local AI / agent SC2 combat logs and mixed batches used during early parser failure testing.

## Why archived

- These replays often fail in `sc2reader` (empty `cache_handles` / corrupt metadata).
- The active project pipeline targets **human vs human** replays only.
- There is no dedicated AI-log parser in `src/`; failures were data/format issues, not a separate code path.

## Contents

- `corrupt_samples/` — unreadable agent `replay.SC2Replay` copies from local Qwen/SC2 experiment logs.
- `batch_mix/` — mixed batch used to verify parse-error isolation.

## Policy

Do **not** place these files under `data/replays/`.
Do **not** treat this archive as part of the production dataset.
