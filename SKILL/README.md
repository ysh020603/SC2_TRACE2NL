# SC2 Adaptive Skills（plan_2 pilot）

按 `plan_2.md` 第一轮范围生成的 **9 个分种族 pilot Skill**。

## 布局

```text
SKILL/<race>/<strategy>/
  skill.json           # 机器可读政策
  evidence.json        # 样本与胜率证据
  Top_agent.md         # naive Agent 用 Summary
  validation_report.json
```

## Pilot 列表

| 种族 | Skill | 主 Matchup | 目录 |
|---|---|---|---|
| Terran | bio | TvP | `terran/bio` |
| Terran | two_base_matrix_tanks | TvZ | `terran/two_base_matrix_tanks` |
| Terran | marine_rush | TvT | `terran/marine_rush` |
| Protoss | robo | PvT | `protoss/robo` |
| Protoss | voidray | PvZ | `protoss/voidray` |
| Protoss | four_gate | PvP | `protoss/four_gate` |
| Zerg | macro_roach | ZvT | `zerg/macro_roach` |
| Zerg | roach_hydra | ZvP | `zerg/roach_hydra` |
| Zerg | mutalisk | ZvZ | `zerg/mutalisk` |

## 复现

```bash
conda activate sc2replay
python analysis/plan2/run_plan2_pilot.py
```

报告：`analysis/outputs/15_skills/plan2_pilot_report.md`

## 注意

- 对手风格标签目前由完整对手 BO 派生（oracle）；上线需映射到可侦察 intel。
- 胜率为关联证据，不是因果。
- `Top_agent.md` 仅 `# Summary` 段供 naive Agent 读取。
