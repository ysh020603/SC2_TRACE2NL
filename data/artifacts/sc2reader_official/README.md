# sc2reader Official Test Replays — `artifacts/sc2reader_official`

## Role in the data layout

- Tree: `data/artifacts/`
- Category: `sc2reader_official`
- Tree purpose: Parse intermediates and non-full-JSON outputs: parquet tables, summary reports, unknown_names, parse_errors, previews, markdown samples.

## What belongs here

Official human test replays from the ggtracker/sc2reader upstream branch (`test_replays/5.0.15`). Used for parser smoke tests and MMR coverage checks.

## Provenance

Downloaded via `scripts/download_test_replays.sh` using the GitHub Contents API (not a full repo clone).

## Mirrored sibling folders

Use the **same category name** across all three trees:

| Tree | Path |
|------|------|
| Pending replays | `data/replays/sc2reader_official/` |
| Parse artifacts | `data/artifacts/sc2reader_official/` |
| Full match JSON | `data/full_json/sc2reader_official/` |

## Typical commands

```bash
# Parse this category
sc2mine parse-dir --category sc2reader_official

# Or explicit paths
sc2mine parse-dir data/replays/sc2reader_official \
  --artifacts data/artifacts/sc2reader_official \
  --json-out data/full_json/sc2reader_official
```

## Policy

- Human vs human games only in the active pipeline.
- Local AI / agent combat logs are out of scope; see `archive/local_ai_logs/`.
