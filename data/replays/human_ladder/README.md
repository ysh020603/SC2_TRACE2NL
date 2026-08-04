# Human Ladder — `replays/human_ladder`

## Role in the data layout

- Tree: `data/replays/`
- Category: `human_ladder`
- Tree purpose: Pending input `.SC2Replay` files only. Do not put parquet/JSON outputs here.

## What belongs here

Human vs human ladder (matchmaking) StarCraft II replays.

## Provenance

Drop ladder `.SC2Replay` files here manually (for example from Battle.net replay folders or rsync from a player machine). This category starts empty in the repo skeleton.

## Mirrored sibling folders

Use the **same category name** across all three trees:

| Tree | Path |
|------|------|
| Pending replays | `data/replays/human_ladder/` |
| Parse artifacts | `data/artifacts/human_ladder/` |
| Full match JSON | `data/full_json/human_ladder/` |

## Typical commands

```bash
# Parse this category
sc2mine parse-dir --category human_ladder

# Or explicit paths
sc2mine parse-dir data/replays/human_ladder \
  --artifacts data/artifacts/human_ladder \
  --json-out data/full_json/human_ladder
```

## Policy

- Human vs human games only in the active pipeline.
- Local AI / agent combat logs are out of scope; see `archive/local_ai_logs/`.
