# Readable Skill V1

This compiler turns the existing Skill Mining V2 statistical outputs into observation-compatible hierarchical Markdown. It is additive: `analysis/skill_mining_v2`, `analysis/outputs_skill_v2`, and `SKILL_MINING_V2` remain read-only.

The information boundary is applied before projection and annotation for each of six methods. Agent-facing files never expose action lists, replay state/cluster identifiers, exact hidden counts, or provenance. Statistical signs are immutable. Opponent prose uses partial `Enemy Intelligence` language; exact runtime actions remain the Agent's responsibility.

## Runtime

Use Python 3.10+ with `pandas`, `pyarrow`, and the repository's API client dependencies. On the current server:

```bash
/data2/shy_2608/envs/shy_verl/bin/python -m analysis.readable_skill_v1.run_pipeline \
  --openings PvP_O01,TvZ_O01,ZvT_O01
```

Annotation is hard-pinned to the `API_config/config.json` entry `DeepSeek-V4-flash`. The compiler verifies `is_reasoning=false`, explicitly disables reasoning on every request, rejects returned reasoning content, and refuses `DeepSeek-V4-flash_think`.

After reviewing the three-matchup pilot, run all openings and methods:

```bash
/data2/shy_2608/envs/shy_verl/bin/python -m analysis.readable_skill_v1.run_pipeline --no-resume
```

Resume is enabled by default. `--skip-llm` exists only for deterministic unit tests and dry runs; its provenance is clearly marked and it must not be used for experiment artifacts.

Outputs:

- `analysis/outputs_readable_skill_v1/`: per-stage internal artifacts and catalog.
- `SKILL_MINING_V2_READABLE/`: Agent-facing `SKILL.md`, `index.json`, and `nodes/*.md`, plus runtime-inaccessible provenance.
- `READABLE_SKILL_BASELINE_MANIFEST.json`: frozen mining and Agent baseline identities.

Validation is fail-closed for action/oracle/count leakage, navigation, badges, and all ablation boundaries.

## Agent consumer and live-match policy

The versioned consumer is the `SC2-Agent-human-skill/` submodule on branch
`codex/human-skill-agent`. Generated Skill Markdown is experiment data and must
not be edited to carry runtime instructions. Native SC2 launch, clean-result
acceptance, retry, and match-local cleanup are defined only in the Agent
submodule's `docs/SC2_BATCH_EXPERIMENT_POLICY.md`.
