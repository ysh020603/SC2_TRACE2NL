# Human Tournament / Pro — `full_json/human_tournament`

## Role in the data layout

- Tree: `data/full_json/`
- Category: `human_tournament`
- Tree purpose: Complete per-match JSON exports only (`<replay_id>.json` and optional `full_matches.json`).

## What belongs here

Human vs human tournament or professional match replays.

## Provenance

Seeded from local python-sc2 test fixtures (ESL / pro series 2022 games). Add more Spawning Tool or event packs under this same category name.

## Mirrored sibling folders

Use the **same category name** across all three trees:

| Tree | Path |
|------|------|
| Pending replays | `data/replays/human_tournament/` |
| Parse artifacts | `data/artifacts/human_tournament/` |
| Full match JSON | `data/full_json/human_tournament/` |

## Typical commands

```bash
# Parse this category
sc2mine parse-dir --category human_tournament

# Or explicit paths
sc2mine parse-dir data/replays/human_tournament \
  --artifacts data/artifacts/human_tournament \
  --json-out data/full_json/human_tournament
```

## Policy

- Human vs human games only in the active pipeline.
- Local AI / agent combat logs are out of scope; see `archive/local_ai_logs/`.
