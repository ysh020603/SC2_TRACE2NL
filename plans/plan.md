# SC2 Replay 开局策略发现与对局优势分析方案

## 1. 项目目标

从约 10 万场 SC2 1v1 Replay 的 Build Order 数据中，自动发现三个种族各自常见的宏观开局策略，并回答以下问题：

1. Terran、Protoss、Zerg 分别存在哪些高频开局策略？
2. 同一种族面对不同对手种族时，策略是否发生系统性变化？
3. 每个策略的典型建造顺序、经济倾向、科技路线、产能投入和兵种方向是什么？
4. 某个己方策略面对某个对方策略时，是否具有统计意义上的胜率优势？
5. 这种优势在不同 MMR、地图、版本、地区和时期下是否稳定？
6. 哪些策略属于稳定通用型，哪些策略属于针对特定对手策略的 Counter？
7. 开局选择与最终胜负、比赛时长、快速胜利和快速失败之间存在什么关系？

最终输出不只是一个聚类结果，而是一套可解释的：

> **种族开局策略库 + 策略特征卡 + 策略对抗矩阵 + 调整后优势估计 + 稳定性报告。**

---

# 2. 核心分析原则

## 2.1 分析单位

建立两个层级的数据表。

### Replay-level 对局表

每场比赛一行：

* `replay_id`
* 地图
* 版本与 `base_build`
* 比赛日期
* 地区
* 对局种族组合
* 游戏时长
* 胜者
* 两名玩家的 MMR
* 数据质量信息

### Player-opening 玩家开局表

每名玩家每场比赛一行：

* `replay_id`
* `player_id`
* `race`
* `opponent_race`
* `result`
* `mmr`
* `opponent_mmr`
* `mmr_diff`
* 自己的开局事件序列
* 对手的开局事件序列
* 自己的策略标签
* 对手的策略标签

一场非镜像对局产生两条玩家记录。统计模型必须按 `replay_id` 聚类计算标准误，防止把同一场比赛的两个视角当作完全独立样本。

---

## 2.2 策略发现与效果评估必须分开

聚类阶段只能使用玩家自己的开局信息。

以下字段不得进入开局聚类：

* 最终胜负；
* 比赛时长；
* 对手最终策略；
* 整局单位和建筑统计；
* 6—8 分钟之后的信息；
* 任何只能在比赛结束后得到的信息。

否则会发生标签泄漏，得到的不是“开局策略”，而是“根据结果划分出来的对局类型”。

正确流程是：

1. 仅根据己方开局动作发现策略；
2. 为每名玩家分配策略标签；
3. 再把己方策略、对手策略与最终结果进行关联分析。

---

## 2.3 “优势”默认指统计关联，不直接声称因果关系

Replay 是观察数据，玩家并不是随机选择开局。高水平玩家可能更喜欢某些策略，不同版本和地图也可能影响策略选择。

因此报告中应使用：

* “调整后的胜率优势”；
* “与胜利正相关”；
* “在相同 MMR、地图和版本条件下表现更好”。

避免直接写成：

* “该开局使胜率提高 8%”；
* “该策略导致胜利”。

除非后续有随机实验或 Agent 对战实验进行因果验证。

---

# 3. 数据质量审计

在开始聚类之前，Agent 必须首先生成数据质量报告。

## 3.1 基础合法性检查

检查：

1. `replay_id` 是否唯一；
2. 每场比赛是否恰好有两名有效玩家；
3. 是否为 1v1；
4. 种族是否属于 Terran、Protoss、Zerg；
5. 胜负结果是否互斥；
6. 是否存在双方都 Win、双方都 Loss 或结果缺失；
7. `build_order` 是否为空；
8. 时间是否单调；
9. `frame`、`second`、`time` 是否基本一致；
10. `standard_result_name` 是否缺失；
11. `standard_mapping_confidence` 是否过低；
12. 是否有大量 unmapped ability；
13. MMR 是否存在和是否处于合理范围。

输出：

* 总 Replay 数；
* 有效 Replay 数；
* 删除数量及原因；
* 各种族、各 Matchup、各版本、各地区的样本量；
* MMR 缺失率；
* BO 为空或异常的比例；
* 映射成功率。

---

## 3.2 统一时间尺度

样例中：

* `duration_seconds = 386`
* Build Order 最后可出现约 `534 second`

两者比例约为 1.38，说明比赛时长与 BO 事件时间可能分别采用真实时间和游戏时间。

分析开局时必须统一使用：

* `build_order.second`，或
* `frame / 固定帧率`

作为游戏内时间。

不得把 `duration_seconds` 直接与 `build_order.second` 混合比较。

为每场 Replay 计算：

```text
time_scale_ratio =
    max_valid_build_order_second / duration_seconds
```

检查比例分布。若大部分集中在约 1.38—1.40，则将其记录为时间制式差异，而不是错误。

最终产生：

* `duration_real_seconds`
* `duration_game_seconds`
* `time_scale_ratio`

---

## 3.3 指令意图与真实完成的区别

当前数据表达的是：

> 玩家下达了生产、建造或研究命令。

而不是：

> 单位、建筑或升级已经可靠完成。

因此：

* 不能把 `estimated_completion_second` 当作真实完成时间；
* 不能确定某条命令是否被取消；
* 不能完全确定生产是否成功；
* 不适合精确计算某时刻真实兵力；
* 可以分析玩家的宏观投入意图和技术路线。

建议将所有指标命名为：

* `first_order_time`
* `ordered_count`
* `ordered_by_time_t`

不要命名为：

* `completion_time`
* `completed_count`
* `army_at_time_t`

---

## 3.4 异常和重复命令处理

对以下情况进行标记：

* 同一玩家在同一 frame 下达完全相同命令；
* 相同 `standard_action_name` 在极短时间内异常重复；
* 时间倒序；
* `occurrence_index` 不连续；
* mapping confidence 低；
* 单局宏观动作数量异常高或异常低。

不要贸然删除所有短时间重复生产命令，因为它们可能是合法的多生产建筑并行生产。

仅自动删除：

* 完全相同 frame；
* 完全相同玩家；
* 完全相同 ability；
* 完全相同 result；
* 完全相同 occurrence index

的严格重复记录。

其他疑似重复只打质量标签。

---

# 4. 开局时间范围定义

不能只使用一个任意的“前 8 分钟”，建议进行多尺度分析。

## 4.1 三层开局表示

### 阶段 A：初始承诺期

```text
0—210 游戏秒，即 0:00—3:30
```

主要观察：

* 第一生产建筑；
* 第一气矿时间；
* 是否早扩张；
* 是否早静态防御；
* 第一科技分支；
* 第一批作战单位。

这一阶段适合识别最早的经济、科技和极端投入倾向。

### 阶段 B：开局成型期

```text
0—300 游戏秒，即 0:00—5:00
```

作为主要分析窗口。

主要观察：

* 一矿还是二矿；
* 生产建筑规模；
* 主科技路线；
* 第一轮兵种构成；
* 升级方向；
* 是否存在明显高投入路线。

### 阶段 C：开局转型期

```text
0—420 游戏秒，即 0:00—7:00
```

观察：

* 开局向中期的转型；
* 第二科技分支；
* 第二基地；
* 产能扩张；
* 兵种组合成型。

三个阶段分别聚类或至少分别提取特征，用于分析：

> 同一个 3:30 开局承诺，之后会分化成哪些 5:00 和 7:00 策略。

---

## 4.2 处理提前结束的比赛

固定 5 分钟窗口会产生右删失问题：

* 如果比赛在 4 分钟结束；
* 5 分钟没有出现某建筑；
* 不能解释为玩家主动选择“不建”。

应增加字段：

```text
opening_observed_to_210
opening_observed_to_300
opening_observed_to_420
```

对于在截止时间前结束的比赛：

1. 可以参加更早窗口分析；
2. 不直接参加对应较晚窗口的无删失聚类；
3. 单独标记为 `early_terminated`；
4. 使用早期序列分类器预测其最可能策略；
5. 预测结果必须带置信度，不能与完整观察标签完全等价。

主要策略发现建议使用 5 分钟前仍在进行的比赛；快速结束对局另做敏感性分析。

---

# 5. 宏观事件抽象

原始 BO 中存在大量 Worker 和 Supply 操作。如果直接对完整动作字符串聚类，结果可能主要反映操作频率，而不是战略。

需要同时构建“关键序列”和“统计向量”。

## 5.1 事件分类

把事件映射到以下宏观类别：

### 经济类

* Worker production；
* 第一、第二、第三基地；
* 气矿建筑；
* 主基地升级，如 Orbital Command；
* 经济相关升级。

### 供给类

* Supply Depot；
* Pylon；
* Overlord。

供给动作保留计数和时间密度，但不在关键战略序列中逐条展开。

### 基础产能类

* Barracks、Factory、Starport；
* Gateway、Robotics、Stargate；
* Spawning Pool、Roach Warren、Baneling Nest 等。

### 科技类

* 高级科技建筑；
* 科技升级；
* 关键能力研究。

### 作战单位类

按兵种族系归并，例如：

* Terran：Bio、Factory ground、Air；
* Protoss：Gateway、Robotics、Stargate；
* Zerg：Ling/Bane、Roach/Ravager、Hydra、Muta 等。

同时保留具体单位名称。

### 静态防御类

* Bunker；
* Photon Cannon；
* Spine Crawler；
* Missile Turret；
* Spore Crawler。

由于没有位置，不能判断是主基地防守、前置建筑还是进攻性 Proxy。

因此名称应使用：

* “早期静态防御投入”；
* “早 Forge-Cannon 路线”。

不要仅凭当前数据命名为：

* “Cannon Rush”；
* “Proxy Bunker”；
* “前置兵营”。

---

## 5.2 关键序列

为每名玩家构建简化后的关键序列，例如：

```text
Gas1
ProductionBase1
StaticDefense1
TechFactory1
Expansion2
CombatUnit_WidowMine1
CombatUnit_Tank1
EngineeringBay1
```

序列中：

* Worker 连续生产被压缩为 Worker-production-rate；
* 供给建筑被压缩为分时间段计数；
* 同类单位连续生产可压缩为 `Zealot×3`；
* 保留首次出现时间；
* 保留关键动作先后关系；
* 保留生产建筑和科技建筑数量变化。

---

# 6. 特征工程

建议构建五组特征。

## 6.1 Milestone Timing 里程碑时间

每种族建立专属里程碑集合。

通用特征包括：

* 第一气矿时间；
* 第二气矿时间；
* 第一基础生产建筑时间；
* 第二、第三生产建筑时间；
* 第二基地时间；
* 第三基地时间；
* 第一科技建筑时间；
* 第二科技建筑时间；
* 第一作战单位时间；
* 第一高级单位时间；
* 第一攻击或防御升级时间；
* 第一静态防御时间。

未出现的事件不能简单填写为 9999。

建议使用：

```text
event_observed = 0/1
event_time_if_observed
```

或者将时间截断为窗口上限，同时增加是否出现的二值特征。

---

## 6.2 Count-at-Horizon 截止时间计数

分别在 210、300、420 秒统计：

* Worker 指令数；
* 基地数量指令数；
* 气矿数量；
* 各生产建筑数量；
* 各科技建筑数量；
* 静态防御数量；
* 各兵种族系生产数量；
* 升级数量；
* 宏观动作总数。

由于是 ordered actions，字段统一命名为：

```text
ordered_gateway_count_by_300
ordered_tank_count_by_420
```

---

## 6.3 Tech-path 科技路线

构建离散科技路线特征，例如：

### Terran

* Barracks → CC；
* Barracks → Factory；
* Factory → Starport；
* 多 Barracks；
* 多 Factory；
* 快速 Engineering Bay；
* 早 Armory；
* 一矿高科技；
* 二矿后产能扩张。

### Protoss

* Gateway → Nexus；
* Gateway → Cybernetics；
* Forge opening；
* Twilight branch；
* Robotics branch；
* Stargate branch；
* Dark Shrine branch；
* 多 Gateway；
* 一矿高科技；
* 二矿科技。

### Zerg

* Hatch first；
* Pool first；
* Gas first；
* Roach Warren；
* Baneling Nest；
* Lair；
* Spire；
* 多 Hatch economy；
* 一矿或低经济高单位投入。

路线应由事件相对顺序生成，而不仅仅根据建筑是否出现。

---

## 6.4 战略维度特征

为每个开局计算可解释的连续指标。

### 经济扩张指数

由以下因素构成：

* 第二基地时间；
* Worker 生产密度；
* 早期生产建筑投入的反向指标；
* 第二气矿时间；
* 早期科技投入。

### 产能投入指数

* 基础生产建筑数量；
* 生产建筑增长速度；
* 前 5 分钟单位生产指令数。

### 科技投入指数

* 第一科技建筑时间；
* 科技层级；
* 高级科技建筑数量；
* 升级研究时间。

### Gas Commitment 气矿投入指数

* 第一气矿时间；
* 第二气矿时间；
* 气矿数量；
* 高耗气单位和科技出现时间。

### 静态防御指数

* 前 3:30 和 5:00 静态防御数量；
* 第一静态防御时间。

### One-base Commitment 一矿投入指数

* 延迟扩张；
* 一矿阶段生产建筑数量；
* 一矿阶段科技深度；
* 一矿阶段单位生产密度。

该指标比“侵略性”更可靠，因为没有位置和攻击事件，无法确认玩家是否真正发动进攻。

---

## 6.5 序列模式特征

使用关键动作序列提取：

* Unigram；
* Bigram；
* Trigram；
* Prefix；
* Frequent subsequence。

例如：

```text
Forge → Cannon
Gateway → Cybernetics → Twilight
Barracks → Factory → WidowMine
Hatchery → Gas → Pool
```

使用 TF-IDF 对高频序列模式加权，避免常见供给行为支配聚类。

可使用 PrefixSpan 或 SPADE 提取频繁子序列。

---

# 7. 分层策略发现框架

## 7.1 第一层：种族全局策略

分别对 Terran、Protoss、Zerg 聚类。

聚类输入不包含 `opponent_race`，用于发现跨 Matchup 的全局开局原型。

输出例如：

```text
P-G01
P-G02
...
T-G01
...
Z-G01
...
```

回答：

* Protoss 总体有哪些主要开局家族？
* Terran 总体有哪些主要科技和经济路线？
* Zerg 总体有哪些经济与单位投入模式？

---

## 7.2 第二层：Matchup 专属变体

分别处理：

* PvT、PvZ、PvP；
* TvP、TvZ、TvT；
* ZvP、ZvT、ZvZ。

在每个全局策略内部检查是否存在明显的 Matchup 子结构。

例如，同样属于“早二矿科技型”，在 PvT 中可能偏 Robotics，而在 PvZ 中可能偏 Stargate。

输出：

```text
P-G02-PvT-A
P-G02-PvZ-A
P-G02-PvZ-B
```

这样既有统一的种族策略体系，也保留对手种族导致的具体变体。

---

# 8. 聚类方法

## 8.1 推荐主方法

使用以下特征拼接：

1. 标准化后的里程碑时间；
2. 截止时间计数；
3. 科技路线 One-hot；
4. 战略维度指标；
5. 序列 N-gram 经 Truncated SVD 降维后的表示。

连续时间建议在相同：

* 种族；
* Matchup；
* Balance Patch

内部进行 Median/IQR 标准化，降低版本节奏差异。

主聚类算法使用：

> **HDBSCAN**

原因：

* 不要求预先指定策略数量；
* 能识别不同密度的策略簇；
* 能将极少见和异常 BO 标记为 Noise；
* 适合 10 万规模数据；
* 可以输出成员概率。

参数搜索范围：

```text
min_cluster_size:
    max(100, 样本量的 0.3%—1%)

min_samples:
    10、20、30、50

cluster_selection_method:
    eom
```

---

## 8.2 序列相似性验证

对关键事件序列另外计算：

* Weighted Levenshtein Distance；
* Jaccard distance of frequent subsequences；
* Soft-DTW 或时间感知编辑距离。

权重示例：

```text
基地、核心科技建筑、第一生产建筑：3.0
生产建筑数量变化：2.0
关键升级、关键兵种：2.0
气矿：1.5
静态防御：1.5
Worker、Supply：0.2—0.5
```

检查同一聚类中的 BO 在序列层面是否也相似。

不要仅使用 UMAP 图上的视觉分离作为聚类正确性的证据。UMAP 主要用于展示，不应作为唯一聚类依据。

---

## 8.3 聚类数量与质量评估

至少报告：

* HDBSCAN DBCV；
* Silhouette score；
* Cluster coverage；
* Noise ratio；
* 每个簇样本量；
* 簇内平均距离；
* 簇间距离；
* Bootstrap stability；
* Adjusted Rand Index；
* Variation of Information。

Bootstrap 流程：

1. 从 Replay 中有放回抽样；
2. 重复聚类 20—50 次；
3. 将新聚类与原聚类对齐；
4. 计算各策略的成员稳定率；
5. 不稳定簇合并为 Other 或重新聚类。

一个可发布的常用策略建议满足：

```text
样本量 >= 100
占对应 Race-Matchup 的比例 >= 0.5%
Bootstrap 成员稳定率 >= 0.70
```

具体阈值根据每个 Matchup 样本量调整。

---

# 9. 策略解释与命名

## 9.1 代表性 BO

每个策略选择：

* 距离簇中心最近的 Medoid；
* 5—10 条高置信度代表 BO；
* 5 条边界 BO；
* 该策略的高频子序列；
* 各里程碑的中位时间和 IQR。

不要用随机样本代替 Medoid。

---

## 9.2 特征富集分析

对策略 (s) 中每个特征计算：

```text
该策略中的出现率
同 Race-Matchup 基线出现率
Risk Ratio
Log Odds Ratio
标准化均值差 SMD
```

例如：

```text
Twilight 在该簇出现率：82%
PvT 总体出现率：29%
Risk Ratio：2.83
```

只有显著富集且效应量较大的特征才进入策略描述。

---

## 9.3 命名规则

建议使用结构化名称：

```text
[经济状态] + [核心科技] + [主要产能或兵种] + [投入程度]
```

例如：

* 一矿早 Forge—多静态防御—多 Gateway；
* 二矿 Robotics—Gateway 过渡；
* 一矿 Factory—Mine/Tank 高投入；
* 快速二矿—Bio 产能扩张；
* Hatch First—Ling/Bane 压力；
* 低经济 Roach 高投入。

LLM 可以根据结构化统计生成自然语言名称和说明，但不得让 LLM 直接凭几条 BO 决定聚类。

每个名称必须由规则检查器确认：

* 名称中的关键建筑确实富集；
* 名称中的时间描述符合统计分位数；
* 不出现位置数据无法支持的“Proxy”；
* 不出现攻击记录无法支持的“Rush”；
* 不把 ordered action 描述为完成结果。

---

# 10. 策略特征卡

每个策略输出一张统一格式的 Strategy Card。

```json
{
  "strategy_id": "P-G03-PvT-A",
  "race": "Protoss",
  "opponent_race": "Terran",
  "strategy_name": "一矿早Forge-静态防御-多Gateway投入",
  "sample_size": 1842,
  "prevalence": 0.087,
  "cluster_confidence_mean": 0.91,
  "opening_horizon": 300,
  "core_sequence": [
    "Pylon",
    "Forge",
    "PhotonCannon",
    "Assimilator",
    "Gateway",
    "CyberneticsCore"
  ],
  "milestone_median": {
    "first_forge": 58,
    "first_cannon": 108,
    "first_gateway": 151,
    "second_base": null
  },
  "strategic_profile": {
    "economy": "low",
    "tech": "medium",
    "production_commitment": "high",
    "gas_commitment": "medium",
    "static_defense": "high",
    "one_base_commitment": "high"
  },
  "representative_replays": [],
  "data_limitations": [
    "building positions unavailable",
    "commands are ordered rather than confirmed completed"
  ]
}
```

---

# 11. 对手策略联合分析

完成双方策略标签后，建立：

```text
Own Strategy × Opponent Strategy
```

矩阵。

分别在每个 Race-Matchup 中计算：

* 对局数；
* 原始胜率；
* Wilson 95% 置信区间；
* 调整后胜率；
* 相对 Matchup 基线的胜率提升；
* Odds Ratio；
* 统计显著性；
* 结果可靠性等级。

示例：

| 己方策略 | 对方策略 |    N |  原始胜率 | 调整后胜率 |   相对基线 |
| ---- | ---: | ---: | ----: | ----: | -----: |
| P03  |  T02 | 1240 | 57.1% | 55.8% | +5.6pp |
| P03  |  T05 |  181 | 41.4% | 44.7% | -5.5pp |

其中 `pp` 表示百分点。

---

# 12. 胜率模型

## 12.1 基础模型

在每个 Race-Matchup 内建立 Logistic Regression：

```text
logit(P(Win)) =
    OwnStrategy
  + OpponentStrategy
  + OwnStrategy × OpponentStrategy
  + spline(MMR difference)
  + Map
  + Patch
  + Region
  + Time period
```

核心是交互项：

```text
OwnStrategy × OpponentStrategy
```

它表示某个己方策略面对某个对方策略时，是否具有额外优势。

---

## 12.2 推荐模型：层次贝叶斯 Logistic Model

由于部分策略对抗组合样本较少，推荐最终使用部分池化模型：

```text
logit(P(Win_i)) =
    α_matchup
  + β_own_strategy
  + γ_opponent_strategy
  + δ_own×opponent
  + f(MMR_diff)
  + u_map
  + v_patch
  + w_region
```

其中：

* `β`：己方策略总体强度；
* `γ`：对手策略总体难度；
* `δ`：特定 Counter 效应；
* `u_map`：地图随机效应；
* `v_patch`：版本随机效应；
* `w_region`：地区效应。

对稀疏策略组合使用零中心收缩先验，避免小样本出现 80%—100% 的虚假高胜率。

输出：

* 后验平均调整胜率；
* 95% credible interval；
* `P(win_rate > 0.5)`；
* `P(lift > 0.05)`；
* Counter 效应后验分布。

---

## 12.3 多重比较

策略矩阵可能产生大量两两比较。

频率学派检验必须使用：

> Benjamini–Hochberg FDR 校正。

不要直接根据未校正的 `p < 0.05` 宣布某个策略存在优势。

贝叶斯结果则可使用：

```text
P(adjusted lift > 5 percentage points) > 0.95
```

作为强优势标准。

---

# 13. 可靠性等级

为每个策略对抗结果分级。

### A：高可靠

* 样本量 ≥ 500；
* 调整后区间较窄；
* 至少三个 Patch 方向一致；
* 至少三个地图方向一致；
* MMR 分层方向一致。

### B：中等可靠

* 样本量 ≥ 200；
* 总体显著；
* 部分子组样本不足。

### C：探索性

* 样本量 50—199；
* 存在较大不确定性；
* 只能作为待验证假设。

### D：不报告优势

* 样本量 < 50；
* 只展示样本量，不给出强结论。

阈值应根据数据分布调整，但必须在分析前固定，避免看到结果后选择阈值。

---

# 14. MMR 分层

策略表现可能随玩家水平显著变化。

按数据分位数或游戏段位划分 MMR 层级，例如：

```text
Low
Lower-middle
Upper-middle
High
Elite
```

每层尽量保持足够样本量。

分析：

1. 策略使用率是否随 MMR 变化；
2. 策略胜率是否随 MMR 变化；
3. 某策略是否只在低分段有效；
4. 高水平玩家是否使用更稳定或更复杂的 BO；
5. Counter 关系是否跨 MMR 稳定。

模型中加入：

```text
OwnStrategy × MMR tier
```

避免将“高手偏好某策略”误判为“该策略本身更强”。

---

# 15. Patch 与时间漂移

样例来自特定 `version` 和 `base_build`。如果 10 万场跨越多个年份，不能直接混合所有版本。

处理方法：

1. 按 `base_build` 或 Balance Patch 划分版本区间；
2. 统计各策略在不同 Patch 的使用率；
3. 检查策略中心是否发生漂移；
4. 对旧策略和新策略分别聚类；
5. 对策略进行跨版本对齐；
6. 胜率模型加入 Patch 效应。

输出：

* 策略流行度时间曲线；
* 策略出现和消失时间；
* Patch 前后策略胜率变化；
* 稳定策略与版本依赖策略。

如果某策略仅存在于一个旧版本，不应将其描述为当前普遍策略。

---

# 16. 地图与地区控制

当前数据有 `map_name` 和 `region`，但没有建筑位置、出生点、地图路径长度。

至少需要：

* 地图固定效应或随机效应；
* 地区效应；
* 地图样本量过滤；
* 地图与策略交互的探索性分析。

若能补充地图元数据，可加入：

* 地图尺寸；
* Rush distance；
* 主矿口宽度；
* 空中距离；
* 天然位置；
* 地图资源结构。

没有地图元数据时，不要对“为什么该策略适合某地图”作过强机制解释。

---

# 17. 比赛时长与结果类型

除胜负外，增加：

* 快速胜利；
* 快速失败；
* 中等时长胜利；
* 中等时长失败；
* 长局胜利；
* 长局失败。

时间阈值建议使用全数据分位数，而不是主观指定：

```text
Fast：前 25%
Medium：25%—75%
Long：后 25%
```

或者按 Matchup 单独计算。

分析每个策略的：

* 平均比赛时长；
* 中位比赛时长；
* 快速胜利率；
* 快速失败率；
* 进入长局的概率；
* 胜利条件下时长；
* 失败条件下时长。

这能区分：

* 高风险高回报策略；
* 容易快速失败的一矿投入；
* 稳定进入中后期的经济策略；
* 快速结束比赛但总体胜率一般的策略。

比赛时长属于结果变量，不能用于开局策略聚类。

---

# 18. 稳健性分析

正式结论至少经过以下检查。

## 18.1 不同开局窗口

比较：

* 3:30；
* 5:00；
* 7:00。

检查主要策略是否稳定。

## 18.2 不同聚类算法

比较：

* HDBSCAN；
* K-Means 或 GMM；
* 层次聚类；
* 序列距离聚类。

若结论只存在于一个算法中，应降低可信度。

## 18.3 不同样本过滤

分别运行：

* 所有有效 Replay；
* 仅 MMR 完整；
* 仅较高 MMR；
* 仅主要 Patch；
* 删除极短比赛；
* 删除低映射置信度记录。

## 18.4 玩家重复问题

如果存在可跨 Replay 识别的匿名玩家 ID：

* 按玩家进行 Cluster Bootstrap；
* 在模型中加入玩家随机效应；
* 限制单个高频玩家的最大权重。

如果没有持久玩家 ID，应明确这是一个限制。

## 18.5 镜像对局

PvP、TvT、ZvZ 中双方同种族。

应避免重复统计造成偏差：

* 标准误按 replay 聚类；
* Counter 矩阵按无序或有序策略对处理；
* 对称组合单独检查；
* 不把 A 对 B 和 B 对 A 当作两场不同比赛。

---

# 19. 样例记录的正确解释方式

样例中的 Protoss 在较早阶段依次出现：

* Forge；
* 多个 Photon Cannon；
* 延后的 Gateway；
* 多 Gateway；
* Twilight Council；
* Charge；
* 后续 Robotics Facility 和 Dark Shrine；
* Nexus 指令较晚。

因此，它可以被描述为：

> “早 Forge 和静态防御投入、扩张较晚、随后转多 Gateway 与 Twilight/Charge 的一矿高投入路线。”

但不能仅凭这份数据称为：

> “Cannon Rush”。

因为当前记录没有建筑位置，无法确认 Photon Cannon 位于己方基地还是对方区域。

Terran 一方则表现出：

* 双气；
* Bunker；
* Factory；
* Widow Mine；
* Siege Tank；
* Engineering Bay 和 Missile Turret；
* 扩张相对较晚。

可以描述为：

> “一矿 Factory 地面机械化与防御投入路线。”

不能从单场样例判断哪种策略总体占优；该 Replay 只能作为未来某个聚类的候选代表样本。

---

# 20. 最终结果展示

## 20.1 总览表

每个 Race-Matchup 一张策略总表：

| Strategy |             名称 | 样本量 | 使用率 | 原始胜率 | 调整胜率 | 稳定性 | 主要特点 |
| -------- | -------------: | --: | --: | ---: | ---: | --: | ---- |
| P01      | Gateway Expand |     |     |      |      |     |      |
| P02      |    一矿 Twilight |     |     |      |      |     |      |
| P03      |    早 Forge 高投入 |     |     |      |      |     |      |

## 20.2 图表

至少生成：

1. 各种族策略使用率柱状图；
2. 策略 UMAP 可视化，仅用于展示；
3. 关键里程碑时间箱线图；
4. 科技路线 Sankey 图；
5. Own strategy × Opponent strategy 胜率热图；
6. 调整后胜率及置信区间图；
7. 策略在不同 MMR 的表现；
8. 策略在不同 Patch 的流行度曲线；
9. 策略快速胜利和快速失败率；
10. 聚类稳定性图。

热图格子必须同时显示：

* 调整后胜率；
* 样本量；
* 可靠性等级。

避免只展示胜率而隐藏样本量。

---

# 21. Agent 执行步骤

## Phase 1：数据审计

1. 遍历全部 JSON；
2. 验证 Schema；
3. 去重；
4. 过滤非 1v1；
5. 生成 Replay-level 表；
6. 生成 Player-level 表；
7. 统一游戏时间；
8. 输出数据质量报告。

输出：

```text
outputs/00_audit/data_quality_report.md
outputs/00_audit/invalid_replays.csv
outputs/00_audit/dataset_summary.json
outputs/01_tables/replays.parquet
outputs/01_tables/player_games.parquet
```

## Phase 2：开局截取

1. 分别截取 210、300、420 秒序列；
2. 标记右删失；
3. 生成关键动作序列；
4. 生成宏观事件类别；
5. 不使用整局 statistics 作为开局特征。

输出：

```text
outputs/02_openings/opening_events.parquet
outputs/02_openings/opening_sequences.jsonl
```

## Phase 3：特征工程

1. 生成里程碑时间；
2. 生成截止时间计数；
3. 生成 Tech-path；
4. 生成战略维度；
5. 生成 N-gram 和频繁序列；
6. 在 Race、Matchup、Patch 内标准化。

输出：

```text
outputs/03_features/features_210.parquet
outputs/03_features/features_300.parquet
outputs/03_features/features_420.parquet
outputs/03_features/feature_dictionary.json
```

## Phase 4：策略发现

1. 按种族训练全局 HDBSCAN；
2. 搜索参数；
3. 进行 Bootstrap Stability；
4. 对 Noise 和小簇处理；
5. 进行 Matchup 子聚类；
6. 选择 Medoid；
7. 生成策略标签和特征富集统计。

输出：

```text
outputs/04_clusters/global_clusters.parquet
outputs/04_clusters/matchup_clusters.parquet
outputs/04_clusters/cluster_stability.csv
outputs/04_clusters/representative_build_orders.json
```

## Phase 5：策略解释

1. 根据富集特征生成结构化标签；
2. 生成 Strategy Card；
3. LLM 生成自然语言说明；
4. 规则程序验证说明是否被数据支持；
5. 人工抽查每个策略至少 20 场。

输出：

```text
outputs/05_catalog/strategy_catalog.json
outputs/05_catalog/strategy_catalog.md
outputs/05_catalog/manual_review_samples/
```

## Phase 6：对抗与胜率分析

1. 关联双方策略；
2. 构建 Counter Matrix；
3. 计算原始胜率和 Wilson 区间；
4. 拟合 Logistic Regression；
5. 拟合层次贝叶斯模型；
6. 计算调整后胜率和 Counter effect；
7. 做 FDR 校正；
8. 给出可靠性等级。

输出：

```text
outputs/06_matchups/raw_counter_matrix.csv
outputs/06_matchups/adjusted_counter_matrix.csv
outputs/06_matchups/model_coefficients.csv
outputs/06_matchups/posterior_summary.csv
```

## Phase 7：稳健性和分层分析

1. MMR 分层；
2. Patch 分层；
3. 地图分层；
4. 地区分层；
5. 不同窗口；
6. 不同聚类算法；
7. 不同过滤条件；
8. 快速结束对局敏感性分析。

输出：

```text
outputs/07_robustness/mmr_analysis.csv
outputs/07_robustness/patch_analysis.csv
outputs/07_robustness/map_analysis.csv
outputs/07_robustness/horizon_consistency.csv
outputs/07_robustness/robustness_report.md
```

## Phase 8：生成最终报告

报告结构：

1. 数据集概况；
2. 数据质量与限制；
3. 三个种族的全局策略体系；
4. 九个 Race-Matchup 的策略变体；
5. 策略特征卡；
6. 策略对抗矩阵；
7. 调整后优势；
8. MMR、地图和版本差异；
9. 稳健性分析；
10. 可用于 Agent 的开局策略知识库。

---

# 22. 推荐初始配置

```yaml
primary_horizon_game_seconds: 300
additional_horizons_game_seconds:
  - 210
  - 420

min_mapping_confidence: 0.90

cluster_method: hdbscan
min_cluster_size:
  minimum_absolute: 100
  fraction_of_group: 0.005

min_strategy_prevalence: 0.005

counter_reporting:
  exploratory_min_n: 50
  medium_reliability_min_n: 200
  high_reliability_min_n: 500

bootstrap:
  repeats: 30
  sampling_unit: replay_id

statistical_model:
  primary: hierarchical_bayesian_logistic
  controls:
    - mmr_difference
    - map_name
    - base_build
    - region
    - played_at_period

multiple_testing:
  method: benjamini_hochberg
  fdr: 0.05
```

---

# 23. 验收标准

Agent 完成任务后必须满足：

1. 所有策略仅根据开局动作发现；
2. 聚类过程没有使用胜负；
3. 没有使用整局统计污染开局特征；
4. 明确区分 ordered 与 completed；
5. 明确处理短局右删失；
6. 分开分析三个种族；
7. 同时提供全局策略和 Matchup 变体；
8. 每个策略有 Medoid 和代表 BO；
9. 每个优势结论同时报告样本量和区间；
10. 胜率模型控制 MMR、地图和 Patch；
11. 稀疏组合使用部分池化或不做强结论；
12. 所有大规模比较经过多重检验校正；
13. 对位置不可见导致的 Proxy/Rush 判断限制进行说明；
14. 至少完成一次人工专家抽查；
15. 输出结果可以直接转化为 SC2 Agent 的策略检索库。

---

# 24. 最终策略价值指标

建议为每个策略总结六个指标：

```text
Popularity：使用频率
Adjusted Strength：调整后总体胜率
Counter Advantage：面对特定策略的额外优势
Robustness：跨 MMR、地图、Patch 的稳定性
Risk：快速失败率和结果方差
Coverage：能够有效应对的对手策略范围
```

最终不要简单给出“最强策略排名”，而应形成：

> 某策略在什么版本、什么 MMR、什么 Matchup、面对什么对方策略时更有效，以及该结论有多可靠。

这才是从 BO 数据中提取可用于决策的开局策略知识。
