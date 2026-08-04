# SC2 TRACE2NL / sc2-replay-miner

Extract bilateral macro facts and approximate build orders from human vs human `.SC2Replay` files.

This repository is intended for agents and humans who need a clear, repeatable data layout:

1. put pending replays under `data/replays/<category>/`
2. run `sc2mine parse-dir --category <category>`
3. read artifacts under `data/artifacts/<category>/`
4. read complete match JSON under `data/full_json/<category>/`

## Hard constraints

- Do **not** install StarCraft II, PySC2, or play replays in a game client.
- Main parser: `sc2reader==1.9.0` with `load_level=3` (metadata + players + tracker events).
- Active dataset scope: **human vs human** games only.
- Local AI / agent combat logs are out of scope. See [`archive/local_ai_logs/README.md`](archive/local_ai_logs/README.md).

## Environment setup

Recommended: Conda + Python 3.11.

```bash
conda create -n sc2replay python=3.11 -y
conda activate sc2replay

# Optional China mirror for pip
export PIP_INDEX_URL=https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
export PIP_DEFAULT_TIMEOUT=120

bash scripts/bootstrap.sh
```

`scripts/bootstrap.sh` installs the package in editable mode (`pip install -e ".[dev]"`) and writes `requirements.lock.txt` / `environment.txt`.

Verify:

```bash
python -c "import sc2reader; print(sc2reader.__version__)"
sc2mine version
```

## Data layout contract

Category names are mirrored across three trees. Always use the same `snake_case` category folder name.

```text
data/
  replays/<category>/       # pending .SC2Replay inputs
  artifacts/<category>/     # parquet, reports, errors, previews (NOT full JSON)
  full_json/<category>/     # complete match JSON only
archive/
  local_ai_logs/            # archived non-human samples
```

### Built-in categories

| Category | Meaning |
|----------|---------|
| `human_ladder` | Human ladder / matchmaking replays |
| `human_tournament` | Human tournament / pro series replays |
| `sc2reader_official` | Official sc2reader `test_replays/5.0.15` human samples |

Each category folder contains a `README.md` describing provenance and sibling paths.

Binary replays and generated outputs are gitignored. Directory skeletons (`README.md`, `.gitkeep`) are tracked.

## How agents should process new data

1. Drop `.SC2Replay` files into `data/replays/<category>/`.
2. Parse:

```bash
sc2mine parse-dir --category <category> --workers 4
```

3. Optional report copy / sample markdown inside artifacts:

```bash
sc2mine report data/artifacts/<category>
```

4. Consume:
   - tabular / ops outputs: `data/artifacts/<category>/`
   - full per-game JSON: `data/full_json/<category>/<replay_id>.json`
   - combined JSON array: `data/full_json/<category>/full_matches.json`

Equivalent explicit form:

```bash
sc2mine parse-dir data/replays/<category> \
  --artifacts data/artifacts/<category> \
  --json-out data/full_json/<category>
```

### Useful commands

```bash
# Inspect raw tracker fields for one file
sc2mine inspect data/replays/sc2reader_official/95435_0.SC2Replay

# Parse one file into a category
sc2mine parse-file path/to/game.SC2Replay --category human_ladder

# Show readable BO
sc2mine show-bo data/replays/human_tournament/some.SC2Replay --type strategy_8m

# Download official sc2reader test replays
bash scripts/download_test_replays.sh

# Small batch helper
bash scripts/run_small_batch.sh sc2reader_official
```

## Output meanings

### Artifacts (`data/artifacts/<category>/`)

| File | Meaning |
|------|---------|
| `replays.parquet` | One row per replay: version, map, duration, parse status |
| `players.parquet` | Players, races, results, MMR (`null` when missing) |
| `macro_events.parquet` | Full-game macro event timeline |
| `build_orders.parquet` | `core_6m` / `strategy_8m` / `all_macro` |
| `summary_report.json` | Batch success rate, matchups, unknown names |
| `unknown_names.json` | Unknown unit/building names |
| `parse_errors.jsonl` | Per-file failures (only when present) |
| `preview.json` | Single-file debug preview (parse-file) |
| `sample_build_orders.md` | Human-readable BO samples from `report` |

### Full JSON (`data/full_json/<category>/`)

Each `<replay_id>.json` is a self-contained match document containing:

- map / version / duration / matchup
- `winner` (1v1) and `winners` (team games)
- per-player race, result, MMR
- full-game BO timeline (`timeline`)
- per-player `build_order`, `build_order_core_6m`, `build_order_strategy_8m`

## Build-order definitions

- `core_6m`: first 6 minutes of building starts, tech morphs, upgrades
- `strategy_8m`: core plus early key/basic unit births
- `all_macro`: whole-game macro events used to regenerate other BO views

Taxonomy and morph whitelist live in `configs/`. Do not hardcode full unit lists in `parser.py`.

## Tests

```bash
pytest -q
ruff check .
```

## Known limitations

1. Tracker events give unit completion times, not click/command times.
2. Tournament rooms may have `mmr = null`.
3. `UnitTypeChangeEvent` keeps tech morphs only (whitelist).
4. Local AI/agent replays are archived and not part of the active pipeline.

## Project map

```text
configs/                 # taxonomy + parser defaults
scripts/                 # bootstrap / download / batch helpers
src/sc2_replay_miner/    # parser, BO, exporters, CLI
tests/                   # pytest suite
data/replays/            # pending human replays by category
data/artifacts/          # parse intermediates by category
data/full_json/          # complete match JSON by category
archive/local_ai_logs/   # out-of-scope AI log samples
vendor/                  # optional external references (not required at runtime)
```
