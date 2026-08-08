# Skill Mining v2 — Human Trace → Adaptive Skill

按仓库根目录方案文档 `SC2 Human Trace → Adaptive Skill Mining.md` 实现的完整流水线。

## 产物

| 路径 | 内容 |
|---|---|
| `analysis/outputs_skill_v2/` | Stage 00–14 分析产出与 figures |
| `SKILL_MINING_V2/` | Full / Ablation Skill 工件 |

## 环境

```bash
conda activate sc2replay
cd /data2/shy_2608/SC2trace2nl
```

LLM 调用复用 `API_Tools/llm_caller.py`，默认模型 key：

```text
DeepSeek-V4-flash   # API_config/config.json 中 nothinking 配置
```

## 一键运行

```bash
# TvP pilot（推荐先跑通）
python analysis/skill_mining_v2/run_pipeline.py \
  --matchup TvP --limit 2000 --seed 42 --skip-llm

# 带 LLM 标注
python analysis/skill_mining_v2/run_pipeline.py \
  --matchup TvP --limit 2000 --llm-model-key DeepSeek-V4-flash

# 分阶段
python analysis/skill_mining_v2/run_pipeline.py --from-stage 3 --to-stage 8

# 全 9 个 directional matchup
python analysis/skill_mining_v2/run_pipeline.py
```

## Stage 一览

| Stage | 模块 | 输出 |
|---|---|---|
| 00 | `stage00_manifest.py` | `00_manifest/run_manifest.json` |
| 01 | `stage01_trajectories.py` | `01_trajectories/player_trajectories.parquet` |
| 02 | `stage02_semantics.py` | `02_semantics/*` |
| 03 | `stage03_opening_windows.py` | `03_opening_windows/*` |
| 04 | `stage04_opening_discovery.py` | `04_openings/*` |
| 05 | `stage05_state_snapshots.py` | `05_snapshots/*` |
| 06 | `stage06_state_discovery.py` | `06_states/*` |
| 07 | `stage07_transition_mining.py` | `07_transitions/*` |
| 08 | `stage08_transition_value.py` | `08_transition_value/*` |
| 09 | `stage09_graph_builder.py` | `09_graphs/*` |
| 10 | `stage10_annotation_packets.py` | `10_annotation_packets/*` |
| 11 | `stage11_llm_annotation.py` | `11_annotations/*` |
| 12 | `stage12_skill_compile.py` | `12_skills/*` + `SKILL_MINING_V2/full_signed_graph/` |
| 13 | `stage13_ablation_generation.py` | `SKILL_MINING_V2/ablation_*` |
| 14 | `stage14_validation.py` | `14_validation/*` |

## 关键设计约束

- `action_json` = 命令意图（ordered），不是完成态。
- Opening / State / Response 严格按时间截断，胜负只进入 Stage 08。
- `preferred` / `harmful` 仅由 Stage 08 统计决定；LLM 只做语义翻译。
- Opponent state 标注 `visibility = oracle_trace`。
- Directional matchup：一场 PvT 会生成 `PvT` 与 `TvP` 两条样本。

## Ablation Methods

```text
M0 ablation_single_trace
M1 ablation_static_population
M2 ablation_flat_adaptive
M3 ablation_positive_only
M4 full_signed_graph
M5 ablation_frequency_only
```
