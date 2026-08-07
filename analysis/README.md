# analysis：SC2 开局策略发现流水线

按 [`plans/plan.md`](../plans/plan.md) Phase 1–8 对 `raw_data` / `data/action_json` 进行分析。  
**全量已完成**：`data/action_json` = **103,787** 局；终报本地生成于 `outputs/08_final/final_report.md`（`outputs/` 不入库，见 [`outputs/README.md`](outputs/README.md)）。

## 数据放置

| 路径 | 角色 |
|---|---|
| `raw_data/by_matchup/<matchup>/` | 全量原始 `.SC2Replay`（约 103,787） |
| `data/action_json/<matchup>/` | 宏观指令 JSON（分析输入） |
| `analysis/` | 统计脚本与全部产出 |

解析命令（无 tracker 批次）：

```bash
conda activate sc2replay
sc2mine parse-actions-dir raw_data/by_matchup/TvZ \
  --json-out data/action_json/TvZ --workers 4
```

## 一键复现 Phase 1–8

```bash
conda activate sc2replay
cd /data2/shy_2608/SC2trace2nl

# 仅 Phase 1
python analysis/phase1_audit/run_audit.py

# Phase 2–8（可加 --with-phase1）
python analysis/run_pipeline.py
```

## 目录结构

```text
analysis/
  README.md
  run_pipeline.py                 # Phase 2–8 编排
  phase1_audit/run_audit.py
  pipeline/
    taxonomy.py                   # 宏观事件分类 / 关键序列
    io_utils.py
    phase02_openings.py
    phase03_features.py
    phase04_clusters.py
    phase05_catalog.py
    phase06_matchups.py
    phase07_robustness.py
    phase08_report.py
  outputs/
    00_audit/ ... 01_tables/
    02_openings/ ... 08_final/
```

## 阶段产出与阅读顺序

| Phase | 说明 | 主文档/表 |
|---|---|---|
| 1 | 数据质量审计 | [`outputs/00_audit/data_quality_report.md`](outputs/00_audit/data_quality_report.md) |
| 2 | 开局截取 210/300/420 | `outputs/02_openings/` |
| 3 | 特征工程 | `outputs/03_features/feature_dictionary.json` |
| 4 | 种族全局 + Matchup 聚类 | `outputs/04_clusters/` |
| 5 | 策略目录 / 特征卡 | [`outputs/05_catalog/strategy_catalog.md`](outputs/05_catalog/strategy_catalog.md) |
| 6 | 对抗矩阵与调整胜率 | `outputs/06_matchups/` |
| 7 | MMR/地图/版本稳健性 | [`outputs/07_robustness/robustness_report.md`](outputs/07_robustness/robustness_report.md) |
| 8 | 最终报告 + Agent KB | [`outputs/08_final/final_report.md`](outputs/08_final/final_report.md) |

## 全量结果（摘要）

1. **质量**：映射率 ≈ 99.97%；时间尺度中位数 ≈ 1.375。
2. **策略**：10 个全局簇（P5/T2/Z3）；各族主流簇约占 93%–97%，另有少数高稳定变体。
3. **对抗**：98 单元格；A/B/C/D = 13/12/26/47；主流对主流接近均势。
4. **窗口一致性**：经济/科技指数跨 210–300–420 高相关（≈0.93–0.97）。
5. **限制**：命令意图 ≠ 完成；无位置；自动命名需对照 Medoid 序列解读。

## 设计约束（与 plan 对齐）

- 聚类只用己方开局特征，不用胜负/时长/对手策略/整局 statistics。
- 指标命名为 ordered / first_order，不用 completion 语义。
- 命名禁止 Proxy/Rush 等位置依赖措辞。
- 优势表述为调整后关联，不做因果宣称。
- 全量使用 `min_cluster_size ≈ max(100, 0.5%·n)`。

## Agent 检索库

```text
analysis/outputs/05_catalog/strategy_catalog.json
analysis/outputs/04_clusters/representative_build_orders.json
analysis/outputs/06_matchups/adjusted_counter_matrix.csv
analysis/outputs/08_final/agent_strategy_kb.json
analysis/outputs/08_final/strategy_value_metrics.csv
```
