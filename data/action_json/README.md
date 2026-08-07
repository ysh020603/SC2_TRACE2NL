# data/action_json

Generated JSON from the independent `replay.game.events` macro-action parser.

The parser keeps production, construction, tech morph, and upgrade/research
commands. It excludes micro actions and all position fields.

```bash
sc2mine parse-actions-file path/to/replay.SC2Replay \
  --json-out data/action_json/<category> \
  --action-database data_sc2_260701/data_base_sc2_260701.json

sc2mine parse-actions-dir path/to/replays \
  --json-out data/action_json/<category> \
  --workers 4
```

Generated `.json` and `.jsonl` files are gitignored. Keep only this README and
optional `.gitkeep` files in Git.

These records describe commands ordered by players. They do not confirm unit
birth, building or research completion, deaths, resources, supply, or command
cancellation outcomes. Inspect the `data_quality` object in every output file.

Each timeline item contains both naming systems:

- `ability`: original replay/sc2reader name, such as `BuildSupplyDepot`;
- `standard_action_name`: canonical `Ability.name` from the structured database,
  such as `TERRANBUILD_SUPPLYDEPOT`;
- `standard_result_name` / `standard_result_type`: canonical action result;
- `standard_mapping_status` / `standard_mapping_confidence`: mapping audit fields.

If the database has no corresponding Ability, `standard_action_name` is `null`;
the raw name remains available and is listed under `unmapped_abilities`.
