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
- Independent action parser: `load_level=4` for macro commands when tracker events are absent.
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
  action_json/              # command-derived macro JSON (generated)
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

## Macro action parser (`game.events`)

The original tracker parser remains unchanged. For Blizzard AI/ML replay packs that
do not contain `replay.tracker.events`, use the independent action parser:

```bash
# One replay
sc2mine parse-actions-file path/to/game.SC2Replay \
  --json-out data/action_json \
  --action-database data_sc2_260701/data_base_sc2_260701.json

# A directory
sc2mine parse-actions-dir raw_data/by_matchup/TvZ \
  --json-out data/action_json/TvZ \
  --workers 4

# Deterministic sample
sc2mine parse-actions-dir raw_data/by_matchup/TvZ \
  --json-out raw_data/logs/action_sample/TvZ \
  --limit 40 --seed 42 --workers 4
```

This parser retains only player-issued macro commands:

- production: workers and army units
- construction: buildings and add-ons
- tech morphs: Lair/Hive, Orbital Command, Warp Gate, and similar
- upgrade/research commands

It excludes attack, move, right-click, selection, control-group, camera, and other
micro actions. Target coordinates and unit locations are not exported.

The result is command intent, not observed game state. Every item uses
`action: "ordered"`, `source: "game_events"`, and `observed_completed: false`.
The original replay name remains in `ability`; `standard_action_name` is the
canonical `Ability.name` from `data_sc2_260701/data_base_sc2_260701.json`
(for example, `BuildSupplyDepot` maps to `TERRANBUILD_SUPPLYDEPOT`).
Unresolved database gaps are returned as `null` and listed in
`unmapped_abilities`; they are never silently replaced with a guessed name.
Estimated completion time uses sc2reader balance build time and does not prove that
the command completed. See each JSON's `data_quality` block.

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
5. Action JSON cannot confirm completion, deaths, resources, supply, or reliably
   associate cancel commands; very short games may have an empty build order.

## Project map

```text
configs/                 # taxonomy + parser defaults
scripts/                 # bootstrap / download / batch helpers
src/sc2_replay_miner/    # parser, BO, exporters, CLI
tests/                   # pytest suite
data/replays/            # pending human replays by category
data/artifacts/          # parse intermediates by category
data/full_json/          # complete match JSON by category
data/action_json/        # generated macro-command JSON
archive/local_ai_logs/   # out-of-scope AI log samples
vendor/                  # optional external references (not required at runtime)
```

## Related repositories

Knowledge-backed SC2 agent lives **outside** this repo (sibling checkout), not under `vendor/`.

| Local path | Remote | Branch |
|------------|--------|--------|
| `../SC2-Agent-knowlegde` | [ysh020603/SC2-Agent-260510](https://github.com/ysh020603/SC2-Agent-260510/tree/SC2-Agent-knowlegde) | `SC2-Agent-knowlegde` |

Clone / refresh next to this repository:

```bash
# from parent of SC2trace2nl, e.g. /data2/shy_2608
git clone --branch SC2-Agent-knowlegde \
  git@github.com:ysh020603/SC2-Agent-260510.git SC2-Agent-knowlegde
git -C SC2-Agent-knowlegde pull --ff-only origin SC2-Agent-knowlegde
```
