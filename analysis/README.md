# analysis：Adaptive Skill Mining v2

完整 Adaptive Skill Mining 见 [`skill_mining_v2/README.md`](skill_mining_v2/README.md)：

```bash
conda activate sc2replay
# Pilot：归档当前 V2 产物后干净运行
python analysis/skill_mining_v2/run_pipeline.py \
  --fresh --matchup TvP --limit 2000 --skip-llm

# 全量 9 directional matchups + DeepSeek-V4-flash nothinking
python analysis/skill_mining_v2/run_pipeline.py --fresh --full-windows
```

产出：`analysis/outputs_skill_v2/` + `SKILL_MINING_V2/`。

## 数据放置

| 路径 | 角色 |
|---|---|
| `raw_data/by_matchup/<matchup>/` | 全量原始 `.SC2Replay`（约 103,787） |
| `data/action_json/<matchup>/` | 宏观指令 JSON（分析输入） |
| `analysis/skill_mining_v2/` | Stage 00–14 当前实现 |
| `analysis/outputs_skill_v2/` | 当前运行的统计产出 |
| `SKILL_MINING_V2/` | Full + Ablation Skill |

解析命令（无 tracker 批次）：

```bash
conda activate sc2replay
sc2mine parse-actions-dir raw_data/by_matchup/TvZ \
  --json-out data/action_json/TvZ --workers 4
```

## 目录结构

```text
analysis/
  README.md
  skill_mining_v2/
    run_pipeline.py
    stage00_manifest.py ... stage14_validation.py
    common/
  outputs_skill_v2/
```

## 设计约束

- 聚类只用己方开局特征，不用胜负/时长/对手策略/整局 statistics。
- 指标命名为 ordered / first_order，不用 completion 语义。
- 命名禁止 Proxy/Rush 等位置依赖措辞。
- 优势表述为调整后关联，不做因果宣称。
- `preferred` / `harmful` 只由 Stage 08 统计估计产生。
- 旧 Phase 1–8、plan2 与 pilot Skill 已归档至
  [`archive/pre_v2/`](../archive/pre_v2/README.md)。
