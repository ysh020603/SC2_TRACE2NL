# SC2 Human Trace → Adaptive Skill Mining
## 面向 Code Agent 的完整执行方案

> **归档状态：已完成（2026-08-10）**
> 本文档已完成从方案到 V2 统计挖掘产物的落地，现作为历史设计与数据口径说明
> 归档。后续 Readable Skill、Agent runtime、Full-v2 和 SC2 对局实验由各自文档
> 与代码负责。

### 最终落地状态

- V2 opening/state/transition/value/signed graph 产物已生成并提交于
  `SKILL_MINING_V2/`；
- 实际数据规模包含 207,574 行 opening assignments、1,247,812 行 state
  assignments 和 50,122 行 edge values；
- stage10–14 的原始统计产物在 Readable Skill 开发中保持冻结，未被覆盖；
- Readable 后处理已在 `analysis/readable_skill_v1/` 完成，并生成
  `SKILL_MINING_V2_READABLE/`；
- 342/342 方法 Skill 均使用 LLM annotation，且无 reasoning content、API error、
  fallback 或 validation failure；
- V2 产物提交为 `f2a0ee1`，Readable 编译提交为 `6ba2890`，Full-v2 guarded
  annotation/skill 提交为 `50f199e`；
- Agent 消费端已随 human-skill 最终代码树提交至 `SC2-Agent-knowlegde` 的
  `SC2-Agent-trace2skill` 分支（`5a60b71`）。

### 范围说明

本文档最初明确排除 Agent runtime 与在线 SC2 对局，这一边界保持不变。相关
实现与运行时问题分别见 Readable/Agent 计划归档和 Agent 仓库的
`docs/SC2_HIGH_CONCURRENCY_TIMEOUT_AND_EXIT_INCIDENT.md`。

---

# 1. 项目目标

本阶段的唯一目标是：

> 从大规模 Human StarCraft II Replay 中，自动发现不同 matchup 下的开局策略、策略状态及其随对手变化产生的演化路径，并将这些统计规律转换成结构化、可复用的 Skill。

本阶段**不考虑**：

- Skill 如何接入具体 LLM Agent；
- Agent runtime retrieval；
- Prompt 注入；
- `SC2-Agent-knowlegde` 中 naive Agent 的修改；
- 在线 SC2 对战；
- scheduler 或 execution harness 修改。

最终只要求生成：

```text
Human Replay
    ↓
Data Analysis
    ↓
Opening Strategy Discovery
    ↓
Dynamic Strategy State Mining
    ↓
Opponent-conditioned Evolution Mining
    ↓
Positive / Negative Transition Analysis
    ↓
Strategy Graph
    ↓
LLM Annotation
    ↓
Structured Skill
```

最终产物必须可以独立存在。

---

# 2. 核心研究问题

整个 Skill Mining Pipeline 需要回答四个问题。

## RQ1：Human Replay 中有哪些稳定的开局策略？

例如：

```text
Terran vs Protoss
├── Reaper Expand-like
├── Fast Factory-like
├── Multi-Barracks Pressure-like
└── Fast Tech-like
```

这些名字最终由 LLM 根据数据特征进行语义标注。

策略发现阶段只使用数据，不使用人工预定义策略名称。

---

## RQ2：开局策略应该观察到什么时候？

不能预先固定：

```text
210s = Opening
```

需要比较多个候选时间窗口，例如：

```text
180s
210s
240s
270s
300s
330s
360s
```

分析：

- 太短时是否还无法区分科技路线；
- 太长时是否已经混入大量针对对手的响应；
- 哪个时间窗口最适合表示 initial opening strategy；
- 是否不同种族 / matchup 应采用不同时间窗口。

最终 Opening Window 应由数据分析确定，而不是直接人为指定。

---

## RQ3：相同 Opening 面对不同对手行为时，人类如何继续演化？

将比赛表示成：

```text
Opening
    ↓
Own Strategic State_t
+
Opponent Strategic State_t
    ↓
Human Response
    ↓
Own Strategic State_t+Δ
```

分析：

```text
相同 Opening
+
不同 Opponent State
```

是否导致不同的：

```text
technology transition
production transition
composition transition
expansion transition
defensive transition
```

---

## RQ4：哪些演化路径值得保留为 Skill？

不能简单地：

```text
Win Replay = Good Skill
Loss Replay = Bad Skill
```

需要在相近 Context 下比较不同 response。

最终将 transition 分为：

```text
preferred
default
harmful
uncertain
```

其中：

```text
preferred
```

表示在类似上下文中与更高获胜概率稳定相关。

```text
harmful
```

表示在类似上下文中与较差结果稳定相关。

最终 Skill 同时保留：

```text
应该怎么走
+
什么方向应该避免
```

---

# 3. 整体实验结构

整个项目划分为两个主要部分：

```text
Part A — Data Analysis
Part B — Skill Mining
```

然后独立生成：

```text
Part C — Ablation Skill Variants
```

总体：

```text
Raw Replay
   │
   ▼
────────────────────────
Part A: Data Analysis
────────────────────────
   │
   ├── trajectory normalization
   ├── semantic enrichment
   ├── opening-window analysis
   ├── opening clustering
   ├── temporal state construction
   ├── transition statistics
   └── visualization
   │
   ▼
────────────────────────
Part B: Skill Mining
────────────────────────
   │
   ├── response mining
   ├── transition value estimation
   ├── signed graph construction
   ├── LLM annotation
   ├── Skill compilation
   └── validation
   │
   ▼
Full Adaptive Graph Skill

同时：

Full Pipeline
   ├── Single-Trace Baseline
   ├── Static Population Skill
   ├── Flat Adaptive Skill
   ├── Positive-only Graph Skill
   └── Signed Graph Skill
```

---

# 4. 推荐代码目录

新建独立流水线：

```text
analysis/skill_mining_v2/
│
├── README.md
├── config.py
├── run_pipeline.py
│
├── common/
│   ├── io.py
│   ├── taxonomy.py
│   ├── plotting.py
│   ├── statistics.py
│   ├── clustering.py
│   └── validation.py
│
├── stage00_manifest.py
├── stage01_trajectories.py
├── stage02_semantics.py
├── stage03_opening_windows.py
├── stage04_opening_discovery.py
├── stage05_state_snapshots.py
├── stage06_state_discovery.py
├── stage07_transition_mining.py
├── stage08_transition_value.py
├── stage09_graph_builder.py
├── stage10_annotation_packets.py
├── stage11_llm_annotation.py
├── stage12_skill_compile.py
├── stage13_ablation_generation.py
└── stage14_validation.py
```

---

# 5. 输出目录

所有输出不要混入目前 Phase 1–8 的结果。

新建：

```text
analysis/outputs_skill_v2/
│
├── 00_manifest/
├── 01_trajectories/
├── 02_semantics/
├── 03_opening_windows/
├── 04_openings/
├── 05_snapshots/
├── 06_states/
├── 07_transitions/
├── 08_transition_value/
├── 09_graphs/
├── 10_annotation_packets/
├── 11_annotations/
├── 12_skills/
├── 13_ablations/
├── 14_validation/
└── figures/
```

---

# 6. 最终 Skill 目录

完整方法和消融方法必须严格分目录保存。

```text
SKILL_MINING_V2/
│
├── full_signed_graph/
│
├── ablation_single_trace/
│
├── ablation_static_population/
│
├── ablation_flat_adaptive/
│
├── ablation_positive_only/
│
└── ablation_frequency_only/
```

每个方法内部：

```text
<method>/
├── terran/
│   ├── TvP/
│   ├── TvT/
│   └── TvZ/
│
├── protoss/
│   ├── PvT/
│   ├── PvP/
│   └── PvZ/
│
└── zerg/
    ├── ZvT/
    ├── ZvP/
    └── ZvZ/
```

具体 Skill：

```text
TVP_O03/
├── skill.json
├── evidence.json
├── strategy_graph.json
├── annotation.json
└── validation_report.json
```

---

# 7. Stage 00 — 实验 Manifest

生成：

```text
00_manifest/run_manifest.json
```

包括：

```json
{
  "run_id": "",
  "git_commit": "",
  "dataset_version": "",
  "dataset_hash": "",
  "sc2_knowledge_hash": "",
  "taxonomy_version": "",
  "random_seed": 42,
  "opening_window_candidates": [
    180,
    210,
    240,
    270,
    300,
    330,
    360
  ],
  "snapshot_times": [
    180,
    240,
    300,
    360,
    420,
    480,
    540,
    600,
    720
  ]
}
```

所有输出都记录：

```text
run_id
```

确保实验可复现。

---

# 8. Stage 01 — 构建标准 Player Trajectory

输入：

```text
data/action_json/
```

继续使用已有 macro action：

```text
production
construction
tech_morph
upgrade_research
```

忽略：

```text
move
attack
camera
selection
control group
micro
position
```

---

# 9. 数据语义限制

必须始终记住：

```text
action_json
=
player command intent
```

不是：

```text
confirmed game state
```

因此统一使用：

```text
ordered_count
first_order_time
ordered_by_t
```

禁止使用：

```text
completed_count
actual_army_count
actual_resource_state
```

---

# 10. 每场 Replay 转成两个 Directional Samples

例如一场 PvT：

生成：

```text
Protoss → Terran
Terran → Protoss
```

最终九个空间：

```text
PvP
PvT
PvZ

TvP
TvT
TvZ

ZvP
ZvT
ZvZ
```

输出：

```text
01_trajectories/player_trajectories.parquet
```

字段：

```text
replay_id
player_id

race
opponent_race
directional_matchup

result

mmr
opponent_mmr
mmr_diff

map
patch
base_build
region

duration

own_actions
opponent_actions

data_quality
```

---

# 11. Stage 02 — SC2 Semantic Enrichment

读取：

```text
data_sc2_260701/
```

构建：

```text
02_semantics/entity_index.json
02_semantics/action_semantic_index.json
```

重点利用：

```text
action_result
ability_requires_unit
ability_requires_upgrade

produces
researches

counters
synergizes_with

enables_morph
grants_stat_bonus
SubOntology
```

---

# 12. Action Semantic Representation

例如：

```text
SIEGETANK
```

除了 Unit 名，还可以拥有：

```text
race
entity_type

producer
prerequisite

ground/air
combat category
technology tier

counter relation
synergy relation
```

这些信息主要用于：

```text
strategy feature construction
LLM annotation grounding
```

而不是直接决定胜负价值。

---

# 13. Stage 03 — Opening Window Analysis

这是新版方案中必须新增的重要步骤。

不能直接规定：

```text
Opening = 0–210s
```

Code Agent 必须比较：

```text
180
210
240
270
300
330
360
```

秒。

如果计算压力较大，第一轮可以：

```text
180
210
240
300
360
```

跑完后，再对最佳区域细化。

---

# 14. 为什么需要多时间窗

存在两个相反问题。

## 太短

例如：

```text
180s
```

很多玩家可能都只完成：

```text
Supply
Barracks / Gateway / Pool
Gas
Expansion preparation
```

此时：

```text
Fast Factory
Robo
Stargate
Twilight
2-1-1
```

等重要分支可能尚未形成。

因此 clustering 会出现：

```text
所有人都很像
```

---

## 太长

例如：

```text
360s
```

玩家可能已经：

```text
侦察到对手
开始针对性防守
改变产能
改变兵种
改变科技
```

此时聚类得到的不再只是：

```text
Initial Opening Strategy
```

而是：

```text
Opening + Early Adaptation
```

这会污染后续 Strategy Evolution Mining。

---

# 15. Opening Window 的选择原则

需要寻找一个：

> 信息已经足以区分不同 Opening，但对手条件响应尚未过度混入的时间点。

因此从三个方面评估。

---

# 16. 指标 A — Cluster Separability

每个 window 对九个 matchup 分别 clustering。

计算：

```text
Silhouette Score
Calinski-Harabasz
Davies-Bouldin
```

同时：

```text
cluster prevalence
noise ratio
largest-cluster ratio
```

希望：

```text
largest cluster
```

不要继续达到：

```text
90%+
```

---

# 17. 指标 B — Cluster Stability

Bootstrap：

```text
bootstrap sample
→ re-cluster
→ compare cluster assignment
```

指标：

```text
Adjusted Rand Index
Normalized Mutual Information
cluster retention
```

一个好的 Opening Window 应该产生：

```text
可重复的 strategy groups
```

而不是随着抽样剧烈变化。

---

# 18. 指标 C — Strategy Information Gain

分析增加时间窗：

```text
180 → 210
210 → 240
240 → 300
300 → 360
```

增加了多少新的有效策略信息。

例如：

```text
I(Cluster_210 ; Cluster_240)
```

以及新增的：

```text
technology differentiation
composition differentiation
expansion differentiation
```

如果：

```text
300 → 360
```

增加的信息已经主要来自 opponent-conditioned behavior，而不是 opening structure，则不应继续扩大 Opening Window。

---

# 19. 指标 D — Opponent Leakage Proxy

虽然不能完全知道玩家何时侦察到对手，但可以用统计相关性估计：

对于 Opening Cluster：

```text
Opponent early actions
→ 能否过强预测 Own Opening Cluster?
```

如果 Window 越长：

```text
Opponent State
```

对 Own Opening Cluster 的预测能力突然大幅增加，

说明：

> clustering 开始混入大量针对对手行为的响应。

可以训练一个简单 classifier：

```text
Opponent features before t
→ Own cluster
```

记录：

```text
Opponent-conditioned predictability
```

---

# 20. 推荐 Opening Window Selection Score

综合：

```text
OpeningScore(t)
=
α × Separability
+
β × Stability
+
γ × SemanticDistinctiveness
-
δ × LargestClusterPenalty
-
η × OpponentLeakage
```

不用绝对依赖一个公式，但必须把这些指标全部输出。

最终选择：

```text
global recommended window
```

以及：

```text
per-matchup recommended window
```

---

# 21. 是否允许不同 Matchup 使用不同 Window

需要输出两套结果。

## Global Window

例如：

```text
300s
```

优点：

```text
实验控制统一
论文更容易解释
```

## Matchup-specific Window

例如：

```text
TvP = 300
TvZ = 240
PvT = 300
PvZ = 270
...
```

优点：

```text
更符合真实策略形成速度
```

最终主实验优先使用：

```text
Global Window
```

如果 matchup-specific 明显更好，再作为 supplementary analysis。

这样论文设计更干净。

---

# 22. Stage 03 输出

```text
03_opening_windows/
├── window_metrics.csv
├── matchup_window_metrics.csv
├── window_selection.json
├── cluster_stability.csv
├── leakage_proxy.csv
└── opening_window_report.md
```

---

# 23. Opening Window 可视化

必须生成：

```text
figures/opening_windows/
```

至少：

## Figure A

```text
x-axis: opening window
y-axis: silhouette / stability / leakage
```

九个 matchup 可以：

```text
单独小图
```

或者：

```text
mean ± std
```

---

## Figure B — Largest Cluster Ratio

```text
180
210
240
300
360
```

对应：

```text
largest cluster prevalence
```

用于观察：

> 多长时间后主流大簇开始被有效拆开。

---

## Figure C — Window Similarity Heatmap

展示：

```text
Cluster_180
Cluster_210
Cluster_240
Cluster_300
Cluster_360
```

之间的：

```text
NMI / ARI
```

可以清楚展示：

> 哪个时间点之后 Opening taxonomy 开始稳定。

---

# 24. Stage 04 — Opening Strategy Discovery

选择确定的 Opening Window 后重新正式聚类。

不能直接沿用旧 cluster。

---

# 25. Opening Features

包含：

## Timing

```text
first gas
first expansion
first production
second production
first tech
first combat unit
first upgrade
first static defense
```

## Counts

```text
worker ordered
production buildings
tech structures
combat units
upgrades
expansions
```

## Strategic investment

```text
economy
production
technology
ground
air
defense
upgrade
```

## Sequence

```text
macro unigram
macro bigram
macro trigram
```

---

# 26. Opening Clustering

每个 directional matchup 独立运行。

建议：

```text
standardization
↓
PCA / TruncatedSVD
↓
coarse clustering
↓
recursive split
↓
medoid extraction
↓
stability validation
```

不要继续：

```text
一次 HDBSCAN
→ 最大簇 95%
→ 结束
```

---

# 27. Recursive Split

如果：

```text
largest cluster prevalence > 60%
```

继续对最大簇进行：

```text
K = 2–8
```

的细分实验。

候选：

```text
MiniBatchKMeans
K-Medoids
BIRCH
HDBSCAN
```

综合：

```text
stability
separability
semantic difference
cluster size
```

选取最终 partition。

---

# 28. Strategy Admission

每个 Opening 至少：

```text
support ≥ 300
```

如果存在可靠全局玩家 ID：

```text
unique players ≥ 30
```

同时：

```text
matchup prevalence ≥ 1%
bootstrap retention ≥ 0.70
```

至少存在两个明显的：

```text
timing
technology
composition
economy
```

差异特征。

---

# 29. Opening 输出

```text
04_openings/
├── opening_assignments.parquet
├── opening_catalog.json
├── opening_medoid.json
├── opening_features.parquet
├── opening_stability.csv
└── opening_report.md
```

---

# 30. Opening 数据空间图

生成：

```text
figures/opening_clusters/
```

## UMAP / PCA Scatter

每个 matchup：

```text
PvT
TvP
...
```

分别绘制二维 embedding：

```text
point = player opening
color = cluster
```

目的：

> 从数据空间观察 Opening 是否形成真实的局部分布。

---

# 31. Cluster Prototype Heatmap

行：

```text
Opening Cluster
```

列：

```text
economy
gas timing
expansion timing
production
tech
air
ground
defense
```

展示标准化均值。

非常适合论文展示。

---

# 32. Timing Distribution Figure

对每个 major opening：

```text
first gas
first expansion
first tech
```

绘制：

```text
boxplot / violin
```

帮助解释：

> 两个 cluster 到底为什么不同。

---

# 33. Sequence Sankey

可选生成：

```text
Opening Macro Sequence
```

例如：

```text
Barracks
 → Gas
 → Expand
 → Factory
```

不同 cluster 使用不同 Sankey。

注意控制复杂度，只画 Top 3–5 Opening。

---

# 34. Stage 05 — Temporal Snapshot Construction

比赛后续不能再只用一个 final strategy label。

在：

```text
180
240
300
360
420
480
540
600
720
```

生成 snapshot。

如果 Opening Window 最终确定为 300：

则主要 evolution 从：

```text
300
```

开始。

---

# 35. 每个 Snapshot 保存两类信息

## Cumulative State

```text
0 → t
```

用于表示：

> 到当前为止玩家已经形成什么。

## Recent Delta

```text
t-60 → t
```

用于表示：

> 最近 60 秒玩家正在向哪里投入。

---

# 36. Own State

```text
OwnState_t =
{
  economy,
  expansion,
  production,
  technology,
  composition,
  defense,
  upgrade,
  recent_commitment
}
```

---

# 37. Opponent State

同样：

```text
OpponentState_t =
{
  economy,
  expansion,
  production,
  technology,
  composition,
  defense,
  recent_commitment
}
```

这里是：

```text
oracle replay state
```

因为使用完整 replay 数据。

必须记录：

```text
visibility = oracle_trace
```

---

# 38. Stage 06 — Strategy State Discovery

不要人工先定义：

```text
Fast Air
Greedy Macro
One-base Pressure
```

先用数据聚类。

针对：

```text
matchup
× opening
× time phase
```

聚类：

```text
Own State
Opponent State
```

分别得到：

```text
OWN_S01
OWN_S02
...

OPP_S01
OPP_S02
...
```

名称最后由 LLM 标注。

---

# 39. State Cluster 数量

建议：

```text
3–10
```

主要依据：

```text
sample size
stability
semantic distinctiveness
```

不要过度细分。

---

# 40. Strategy State Visualization

生成：

```text
figures/state_space/
```

至少包括：

## State UMAP

例如：

```text
TvP + Opening O03 + t=360
```

画：

```text
OwnState clusters
OpponentState clusters
```

---

## State Centroid Radar / Heatmap

推荐论文中优先用 Heatmap。

展示：

```text
Economy
Production
Technology
Air
Ground
Defense
Expansion
```

---

# 41. Stage 07 — Conditional Transition Mining

核心对象：

```text
Context_t
=
Opening
+
OwnState_t
+
OpponentState_t
```

然后观察：

```text
Response_t→t+60
```

和：

```text
OwnState_t+60
```

最终：

```text
Opening
+
OwnState
+
OpponentState
→
Response
→
Next OwnState
```

---

# 42. Response Representation

不能只记录：

```text
State 3 → State 7
```

必须记录中间动作。

例如：

```text
+ Factory
+ Starport
+ Anti-air unit
- Expansion investment
+ Defense
```

实际保存：

```text
canonical action delta
semantic investment delta
technology delta
composition delta
production delta
expansion delta
```

---

# 43. Response Clustering

把：

```text
t → t+60
```

所有 action delta 聚类。

得到：

```text
R01
R02
R03
...
```

每个 Response：

```text
medoid action set
top actions
production direction
tech direction
economy direction
composition direction
```

---

# 44. Default vs Conditional Response

必须先计算：

```text
P(R | Opening, OwnState)
```

再计算：

```text
P(R | Opening, OwnState, OpponentState)
```

如果两者接近：

```text
R = Default Evolution
```

如果对特定 opponent state 明显富集：

```text
R = Conditional Response
```

这是区分：

```text
正常发展
```

和：

```text
针对对手变化
```

的关键。

---

# 45. Transition Mining 输出

```text
07_transitions/
├── contexts.parquet
├── responses.parquet
├── response_clusters.json
├── transition_table.parquet
├── conditional_response_table.parquet
└── transition_report.md
```

---

# 46. Transition Visualization

生成：

```text
figures/transitions/
```

---

# 47. Transition Sankey

例如固定：

```text
TvP
Opening O03
```

绘制：

```text
OwnState_300
    ↓
OpponentState
    ↓
Response
    ↓
OwnState_360
```

这张图非常适合作为论文中的：

> Strategy Evolution Visualization

---

# 48. Transition Matrix

横轴：

```text
Opponent State
```

纵轴：

```text
Response
```

颜色：

```text
P(Response | Context)
```

直观展示：

> 不同对手状态是否诱发不同策略响应。

---

# 49. Response Embedding

将：

```text
response delta
```

画 UMAP/PCA。

颜色：

```text
response cluster
```

形状或边框：

```text
Win/Loss
```

先观察成功失败轨迹在 response space 是否存在结构差异。

---

# 50. Stage 08 — Transition Value Estimation

必须同时分析：

```text
successful trajectories
failed trajectories
```

但不能简单给整个 win trace 正标签。

---

# 51. 第一层 — Win/Loss Contrast

对于相同 Context：

```text
C =
Opening
+
OwnState
+
OpponentState
+
time
```

计算：

```text
P(R | C, Win)
P(R | C, Loss)
```

进一步：

```text
win_enrichment
loss_enrichment
```

作为候选 evidence。

---

# 52. 第二层 — Adjusted Response Value

最终核心：

```text
ΔV(R | C)
=
P(Win | R, C)
-
P(Win | default R, C)
```

控制：

```text
MMR difference
map
patch
base_build
region
time
opening
own state
opponent state
```

---

# 53. 推荐估计方法

主版本：

```text
Propensity Model
+
Outcome Model
+
AIPW / Doubly Robust Estimation
```

使用：

```text
5-fold cross-fitting
```

---

# 54. Propensity

估计：

```text
P(Response | Context)
```

推荐：

```text
LightGBM
```

或：

```text
multinomial logistic
```

---

# 55. Outcome Model

估计：

```text
P(Win | Context, Response)
```

推荐：

```text
LightGBM
```

同时可以用：

```text
regularized logistic regression
```

做 robustness check。

---

# 56. Edge Categories

## Preferred

```text
support ≥ 300

effective sample size ≥ 200

adjusted lift ≥ +3 percentage points

并满足：
q < 0.05
或
bootstrap P(lift > 0) ≥ 0.90
```

再检查：

```text
MMR robustness
map robustness
patch robustness
```

---

## Harmful

对称：

```text
adjusted lift ≤ -3pp
```

---

## Default

```text
高频
且
|adjusted lift| < 1.5pp
```

---

## Uncertain

全部其他 response。

---

# 57. Early Failure

同时建立：

```text
early_loss_6m
early_loss_8m
early_loss_10m
```

因为某些防守 response：

```text
最终胜率提升不强
```

但可能：

```text
显著降低早期崩盘率
```

这种 transition 也有价值。

---

# 58. Transition Value Visualization

生成：

```text
figures/value/
```

---

# 59. Win/Loss Response Heatmap

行：

```text
Context
```

列：

```text
Response
```

颜色：

```text
adjusted win lift
```

使用：

```text
negative → harmful
near zero → neutral
positive → preferred
```

论文中可以非常直观地展示不同演化方向。

---

# 60. Forest Plot

对 Top Response：

```text
Response R01
Response R02
...
```

画：

```text
Adjusted Lift ± CI
```

这类图非常适合证明：

> 某些分支不仅高频，而且 outcome association 稳定。

---

# 61. Positive / Negative Path Visualization

针对一个 Opening：

```text
Opening
   ↓
State
   ├── Preferred Edge
   │       ↓
   │    State
   │
   └── Harmful Edge
           ↓
        State
```

每条边标：

```text
support
adjusted lift
```

这应该成为最终论文最核心的 qualitative figure 之一。

---

# 62. Stage 09 — Strategy Evolution Graph

每个：

```text
race
× opponent race
× opening
```

生成独立 Graph。

---

# 63. Graph 必须是 Temporal DAG

不能任意形成循环。

例如：

```text
T300
→
T360
→
T420
→
T480
```

因此：

```text
target_time > source_time
```

---

# 64. Node

节点表示：

```text
Own Strategic State
```

同时带：

```text
time
support
state profile
representative traces
```

---

# 65. Edge

边包含：

```text
Opponent Condition
Response
Next State

support
transition probability

win enrichment
loss enrichment

adjusted value
confidence interval

edge label
```

---

# 66. Full Graph 与 Pruned Graph

生成：

```text
strategy_graph_full.json
strategy_graph_pruned.json
```

完整 Graph 用于分析。

最终 Skill 用：

```text
pruned graph
```

---

# 67. Graph Pruning

每个 state 最多保留：

```text
2 preferred
1 default
2 harmful
```

并要求：

```text
minimum support
```

避免最后 Skill 过于复杂。

---

# 68. Graph Visualization

生成：

```text
figures/graphs/
```

每个主流 Opening 至少一张：

```text
strategy_graph_<skill>.pdf/png
```

视觉结构：

```text
时间从左到右

Node:
Own Strategy State

Condition Label:
Opponent State

Edge:
Response

Edge annotation:
transition probability
adjusted lift
```

---

# 69. Stage 10 — Annotation Packet

到这里之前：

```text
不要调用 LLM
```

LLM 不负责发现统计规律。

生成：

```text
10_annotation_packets/
```

---

# 70. Annotation Packet 内容

```text
Opening Medoid
Opening Statistics

State Profiles

Preferred Edges
Default Edges
Harmful Edges

Positive Paths
Negative Paths

Relevant SC2 Knowledge
```

---

# 71. SC2 Knowledge Retrieval

只从：

```text
data_sc2_260701
```

取 Graph 中出现实体的：

```text
1–2 hop neighborhood
```

包括：

```text
requires
produces
researches
counters
synergizes
upgrade effects
```

禁止把全部 SC2 knowledge 塞给模型。

---

# 72. Stage 11 — LLM Annotation

必须使用仓库已有：

```text
API_config/
API_Tools/
```

Code Agent 需要：

```text
先检查当前 API_Tools 使用方式
```

然后复用。

不要重新建立独立 API 框架。

---

# 73. LLM Pass A — Strategy Naming

输入：

```text
opening medoid
timing
features
representative states
```

输出：

```text
professional_name
data_driven_name
macro_family
strategic_intent
```

命名必须至少由两个数据事实支撑。

---

# 74. LLM Pass B — State Naming

例如从：

```text
high production
low expansion
early factory
```

生成类似：

```text
One-base Factory Commitment
```

这里只负责解释。

Cluster 本身仍来自数据。

---

# 75. LLM Pass C — Edge Interpretation

对于：

```text
Opponent State
+
Response Delta
```

生成：

```text
opponent condition
response interpretation
strategic meaning
```

---

# 76. LLM 不决定 Prefer / Avoid

这是硬约束。

```text
preferred / harmful
```

必须完全来自 Stage 08。

LLM 只翻译：

```text
data evidence
→
human-readable skill
```

---

# 77. Stage 12 — Skill Compilation

完整方法输出：

```text
SKILL_MINING_V2/full_signed_graph/
```

Skill Schema：

```json
{
  "skill_id": "",

  "race": "",
  "opponent_race": "",

  "opening": {
    "id": "",
    "name": "",
    "objective": "",
    "prototype": []
  },

  "default_evolution": [],

  "preferred_rules": [],

  "avoid_rules": [],

  "strategy_graph": "",

  "evidence": ""
}
```

---

# 78. Preferred Rule

```json
{
  "rule_id": "",

  "phase": [],

  "own_state": "",

  "opponent_condition": "",

  "response": "",

  "canonical_actions": [],

  "next_state": "",

  "evidence_id": ""
}
```

---

# 79. Avoid Rule

```json
{
  "rule_id": "",

  "phase": [],

  "own_state": "",

  "opponent_condition": "",

  "avoid_response": "",

  "risk_description": "",

  "evidence_id": ""
}
```

---

# 80. Ablation 设计原则

消融不是之后人工临时制作。

Code Agent 必须在同一 Pipeline 自动生成所有 Variant。

所有 Variant 保存到不同目录。

---

# 81. Method M0 — Single Trace Skill

目录：

```text
SKILL_MINING_V2/ablation_single_trace/
```

目标：

> 测试不进行 population-level data mining，只直接从单条 human trajectory 生成 Skill。

---

# 82. Single Trace 选择

为了公平：

在同一个 Opening Cluster 内选择：

```text
距离 cluster medoid 最近的 winning trajectory
```

不要人工挑。

建议每个 Opening：

```text
3–5 个不同 trace seeds
```

分别生成 Skill。

最终 Agent 实验时可以对 seed 平均，但当前阶段只需要全部生成。

---

# 83. Single Trace 输入

LLM 只看到：

```text
single human trace
+
相关 SC2 knowledge
```

不看到：

```text
population statistics
cluster statistics
transition frequencies
negative trajectories
response values
```

输出：

```text
single_trace_skill.json
```

---

# 84. Method M1 — Static Population Skill

目录：

```text
SKILL_MINING_V2/ablation_static_population/
```

使用：

```text
Opening cluster
+
population statistics
```

但是不使用：

```text
Opponent State
Conditional Response
Evolution Graph
```

最终只生成：

```text
Opening
+
Default Development
```

用于验证：

```text
Population Analysis
```

相对于：

```text
Single Trace
```

是否有价值。

---

# 85. Method M2 — Flat Adaptive Skill

目录：

```text
SKILL_MINING_V2/ablation_flat_adaptive/
```

使用完整：

```text
Opening
Opponent Condition
Preferred Response
Harmful Response
```

但去掉 Graph Relationship。

表现形式：

```text
Rule 1
Rule 2
Rule 3
...
```

---

# 86. Flat 与 Graph 必须信息等价

这是非常关键的实验控制。

Flat 和 Graph：

```text
相同规则
相同 evidence
相同 positive / negative information
```

唯一差异：

```text
是否显式保留：
State
Transition
Next State
Path
```

尽可能控制：

```text
token budget
```

后续才能 argue：

> Graph Management 本身有效。

---

# 87. Method M3 — Positive-only Graph

目录：

```text
SKILL_MINING_V2/ablation_positive_only/
```

保留：

```text
default
preferred
```

删除：

```text
harmful
avoid rules
negative paths
```

---

# 88. Method M4 — Full Signed Graph

目录：

```text
SKILL_MINING_V2/full_signed_graph/
```

包含：

```text
default
preferred
harmful
```

用于验证：

> 是否同时利用成功和失败 trajectories 更好。

---

# 89. Method M5 — Frequency-only

建议同时实现。

目录：

```text
SKILL_MINING_V2/ablation_frequency_only/
```

只依据：

```text
high-frequency transition
```

选择规则。

不经过：

```text
adjusted outcome value filtering
```

这样可以验证：

> 高频 Human Behavior ≠ 高价值 Human Behavior。

这是非常好的额外消融。

---

# 90. 最终 Method Ladder

```text
M0 SingleTrace
        ↓
M1 StaticPopulation
        ↓
M2 FlatAdaptive
        ↓
M3 GraphPositive
        ↓
M4 GraphSigned
```

另外：

```text
M5 FrequencyOnly
```

作为 value filtering 消融。

---

# 91. 对应实验问题

```text
M0 vs M1
```

验证：

> Population-level data analysis 是否优于单轨迹总结。

---

```text
M1 vs M2
```

验证：

> 是否需要 opponent-conditioned adaptive knowledge。

---

```text
M2 vs M3
```

验证：

> Graph organization 是否比 flat rules 更有效。

---

```text
M3 vs M4
```

验证：

> Failure trajectory / negative knowledge 是否提供额外价值。

---

```text
M5 vs M4
```

验证：

> Outcome-aware filtering 是否比单纯模仿高频 human behavior 更有效。

---

# 92. Ablation 本阶段只生成 Skill

注意：

目前只生成：

```text
Skill artifacts
```

不运行 Agent。

因此 Ablation 输出重点检查：

```text
rule count
token size
graph size
evidence coverage
canonical validity
information overlap
```

---

# 93. Ablation Metadata

每个 Skill 都额外生成：

```text
ablation_metadata.json
```

记录：

```json
{
  "source_opening": "",
  "shared_rules": [],
  "removed_information": [],
  "source_trace_ids": [],
  "token_estimate": 0,
  "rule_count": 0
}
```

确保未来实验可以证明不同方法之间控制公平。

---

# 94. Stage 14 — Validation

需要分三类。

---

# 95. Data Leakage Validation

自动测试：

```text
Opening feature:
只能使用 action.second <= opening_window
```

```text
State_t:
只能使用 action.second <= t
```

```text
Response:
只能使用 t < action.second <= t+Δ
```

```text
Outcome:
只能进入 Stage 08
```

---

# 96. Graph Validation

检查：

```text
all nodes exist
all edges exist
no orphan nodes
no backward temporal edge
all response references valid
all evidence references valid
```

---

# 97. Skill Grounding Validation

所有：

```text
preferred rule
```

必须对应：

```text
preferred edge
```

所有：

```text
avoid rule
```

必须对应：

```text
harmful edge
```

---

# 98. Canonical Entity Validation

所有：

```text
Unit
Structure
Upgrade
Ability
```

必须可以在：

```text
data_sc2_260701
```

解析。

不能让 LLM 自己创造 SC2 名称。

---

# 99. LLM Annotation Validation

检测：

```text
causal language
unsupported statement
fabricated unit
fabricated upgrade
missing evidence
direction mismatch
```

例如禁止：

```text
This strategy increases win rate by 8%.
```

应使用：

```text
This transition is associated with better outcomes in comparable historical states.
```

---

# 100. 最终分析报告

Code Agent 必须生成：

```text
analysis/outputs_skill_v2/
```

中的几个总报告。

---

# 101. Report A — Opening Window Report

```text
03_opening_windows/opening_window_report.md
```

回答：

```text
210 是否太短？
300 是否更合理？
360 是否开始混入 response？
最终为什么选某个 window？
不同 matchup 是否一致？
```

---

# 102. Report B — Opening Strategy Report

```text
04_openings/opening_report.md
```

包括：

```text
9 matchup 的 opening 数量
样本量
主要特征
稳定性
medoid
```

---

# 103. Report C — Strategy Evolution Report

```text
07_transitions/transition_report.md
```

回答：

```text
相同 opening 是否出现多个 evolution branch？
哪些 branch 对 opponent state 敏感？
哪些只是 default progression？
```

---

# 104. Report D — Transition Value Report

```text
08_transition_value/value_report.md
```

包括：

```text
preferred edges
harmful edges
default edges
uncertain edges
```

及：

```text
support
adjusted lift
CI
robustness
```

---

# 105. Report E — Skill Catalog

```text
12_skills/skill_catalog.md
```

每个 Skill：

```text
Opening
Default Path
Preferred Branches
Avoid Branches
Graph Size
Evidence Coverage
```

---

# 106. Report F — Ablation Catalog

```text
13_ablations/ablation_catalog.md
```

列出：

| Method | Population | Opponent-adaptive | Graph | Negative Path | Value Filtering |
|---|---:|---:|---:|---:|---:|
| Single Trace | No | Limited | No | No | No |
| Static Population | Yes | No | No | No | No |
| Flat Adaptive | Yes | Yes | No | Yes | Yes |
| Graph Positive | Yes | Yes | Yes | No | Yes |
| Graph Signed | Yes | Yes | Yes | Yes | Yes |
| Frequency Only | Yes | Yes | Yes | Optional | No |

---

# 107. 推荐最终生成的论文级图片

Code Agent 至少生成以下图片。

---

## Figure 1 — Opening Window Selection

```text
window
vs
cluster stability
separability
opponent leakage
```

用于说明：

> 为什么最终选择某个 Opening Window。

---

## Figure 2 — Opening Strategy Space

UMAP/PCA：

```text
Human Opening Trajectories
```

颜色：

```text
Opening Cluster
```

分别选择：

```text
Terran
Protoss
Zerg
```

代表 matchup。

---

## Figure 3 — Opening Feature Heatmap

```text
Opening Cluster × Strategic Features
```

用于解释不同 Opening。

---

## Figure 4 — Dynamic Strategy State Space

例如：

```text
同一个 Opening
```

在：

```text
300
420
540
```

秒的 state distribution。

可以展示：

> 一种 Opening 后续并不会只有一条路线。

---

## Figure 5 — Conditional Response Matrix

```text
Opponent State
×
Human Response
```

颜色：

```text
conditional response probability
```

展示：

> Human strategy adaptation。

---

## Figure 6 — Transition Value Heatmap

```text
Context
×
Response
```

颜色：

```text
adjusted win lift
```

---

## Figure 7 — Signed Strategy Evolution Graph

核心图。

包含：

```text
Opening
State
Opponent Condition
Preferred Edge
Harmful Edge
Next State
```

用于展示：

> Skill 如何从 human traces 得到。

---

## Figure 8 — Positive vs Negative Path Statistics

统计：

```text
support
adjusted lift
path length
```

展示：

```text
preferred
harmful
default
```

三类 edge 的整体分布。

---

# 108. Plotting 要求

所有图同时保存：

```text
PNG
PDF
```

推荐：

```text
dpi = 300
```

同时保存画图源数据：

```text
figures/data/
```

例如：

```text
opening_window_plot.csv
transition_value_plot.csv
graph_plot_nodes.csv
graph_plot_edges.csv
```

这样后期论文作图可以重新调整，而不需要重新跑分析。

---

# 109. Code Agent 运行入口

最终必须支持：

```bash
python analysis/skill_mining_v2/run_pipeline.py
```

---

# 110. 分阶段执行

支持：

```bash
python analysis/skill_mining_v2/run_pipeline.py \
    --from-stage 3 \
    --to-stage 8
```

---

# 111. Pilot 模式

支持：

```bash
python analysis/skill_mining_v2/run_pipeline.py \
    --matchup TvP \
    --limit 5000 \
    --seed 42
```

---

# 112. LLM 控制

支持：

```text
--skip-llm
```

只跑统计。

以及：

```text
--resume
```

避免重复调用 API。

---

# 113. 推荐实际执行顺序

不要一上来跑 10 万局全部 Stage。

---

## Phase A — TvP Pilot

只跑：

```text
TvP
```

先完成：

```text
Opening Window
Opening Discovery
State Mining
Transition Mining
Value
Graph
Skill
Ablations
Figures
```

确保 end-to-end 跑通。

---

## Phase B — 三个代表性 Matchup

建议：

```text
TvP
PvZ
ZvT
```

覆盖三个 race。

验证参数是否跨种族稳定。

---

## Phase C — 全部 9 Directional Matchup

最终跑：

```text
PvP PvT PvZ
TvP TvT TvZ
ZvP ZvT ZvZ
```

---

# 114. 最终验收标准

整个 Pipeline 完成后必须满足：

---

## Opening

```text
完成 opening-window comparison
```

并给出明确选择依据。

---

## Opening Clustering

大多数 major cluster：

```text
support 足够
stability 足够
medoid 可解释
```

不能继续出现：

```text
一个 cluster 占 95%
```

却直接被当作最终策略。

---

## Strategy Evolution

至少在部分 major Opening 中观察到：

```text
multiple stable evolution branches
```

否则 Graph Skill 的研究假设不成立，需要重新调整 state granularity。

---

## Conditional Adaptation

至少部分 response：

```text
P(R | OwnState, OpponentState)
```

明显区别于：

```text
P(R | OwnState)
```

否则说明数据中没有足够 evidence 支撑 opponent-conditioned Skill。

---

## Signed Transition

如果存在稳定：

```text
preferred
harmful
```

则保留。

如果某些 Opening 找不到 harmful edge：

```text
不允许人为制造。
```

---

## Skill

所有 Skill：

```text
100% JSON valid
100% graph link valid
100% evidence traceable
100% canonical entity valid
```

---

## Ablation

对于每个 Full Skill，至少同时生成：

```text
Single Trace
Static Population
Flat Adaptive
Graph Positive
Graph Signed
```

如果数据充足，再生成：

```text
Frequency Only
```

---

# 115. 最终预期产物

完成后仓库应该拥有：

```text
analysis/outputs_skill_v2/
```

用于：

> 数据分析和论文证据。

以及：

```text
SKILL_MINING_V2/
```

用于：

> 不同 Skill generation 方法的最终产物。

---

# 116. 最终方法主线

最终可以把完整方法压缩成：

```text
Multi-window Opening Analysis
        ↓
Opening Strategy Discovery
        ↓
Temporal Strategic State Modeling
        ↓
Opponent-conditioned Response Mining
        ↓
Contrastive Win/Loss Analysis
        ↓
Adjusted Transition Value Estimation
        ↓
Signed Strategy Evolution Graph
        ↓
SC2 Knowledge Grounding
        ↓
LLM Semantic Annotation
        ↓
Adaptive Skill
```

---

# 117. 与消融对应的完整研究逻辑

最终你的实验结构可以非常清楚地回答四层问题：

```text
Single Trace
    ↓
Population Analysis
```

回答：

> 大量 human trajectories 的统计挖掘是否比直接总结一个成功玩家的轨迹更好？

```text
Static Population
    ↓
Adaptive Population
```

回答：

> 对动态对手行为进行建模是否有必要？

```text
Flat Adaptive
    ↓
Graph Adaptive
```

回答：

> 将策略表示为显式 evolution graph 是否比 flat rules 更有效？

```text
Positive Graph
    ↓
Signed Graph
```

回答：

> 除了学习“应该怎么做”，学习失败轨迹中的“不要怎么做”是否具有额外价值？

最终论文的方法主张就会从一个简单的：

> Replay → Skill

变成一个更完整的：

> We mine reusable adaptive skills from large-scale human trajectories by identifying stable opening strategies, modeling opponent-conditioned strategic evolution, estimating the value of alternative transitions, and organizing both beneficial and harmful evolution paths into signed strategy graphs.

这一版的实现重点是：**先把 Skill Mining 和所有 Ablation Skill 完整生成出来，并形成可审计的数据分析、统计结果、图和 Skill 文件；之后再单独进行 Agent Integration 与在线效果实验。**
