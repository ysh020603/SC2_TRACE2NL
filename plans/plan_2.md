# SC2 Replay 开局策略挖掘后续计划

## 从静态聚类到可指导 naive LLM Agent 的自适应 Skill

---

# 一、下一阶段的最终目标

下一阶段不再只是回答：

> Terran、Protoss、Zerg 分别有哪些开局？

而是构建下面这种可执行知识：

> 当我方采用某个基础开局时，如果在某个阶段观察到对手呈现某种经济、产能、科技或兵种倾向，应如何修改接下来 1–2 个决策周期的宏观生产、科技、扩张和兵种组合，并且这种响应在历史数据中具有怎样的样本支持和调整后胜率关联？

最终每一个 Skill 应当包含：

1. 一个基础开局原型；
2. 默认宏观发展路线；
3. 对手风格的可观察判据；
4. 面对不同对手变化时的响应分支；
5. 放弃原计划或转型的条件；
6. 优先级和冲突处理规则；
7. 可输出的 canonical macro actions；
8. 每条规则对应的历史样本、收益和置信度；
9. 与当前 `strategy_tools.py` 自动攻击、防守和侦察机制的一致性。

最终形成：

```text
Replay trajectories
        ↓
Opening archetypes
        ↓
Opponent style states
        ↓
Conditional response transitions
        ↓
Adjusted response value
        ↓
Structured Skill JSON
        ↓
Compiled Top_agent.md
        ↓
naive Agent decision
```

---

# 二、当前分析结果中需要先解决的问题

## 2.1 当前 10 个全局簇不能直接作为 Skill

Protoss、Terran、Zerg 的主流簇分别占约 95.0%、96.8% 和 93.5%。

这说明当前 HDBSCAN 主要完成的是：

* 分离主流行为与极端变体；
* 识别 Cannon、超高产能、极端快扩等异常或特殊行为。

但它没有充分拆开主流开局中的关键分支，例如：

```text
Terran:
Reaper Expand
2-1-1
1-1-1
3-Rax
Fast Factory
Fast Third
Tank Push
Air Tech

Protoss:
Gate Expand
Robo
Stargate
Twilight
Blink
Charge
Fast Third
Multi-Gate Pressure

Zerg:
Hatch First
Pool First
Ling Pressure
Roach
Fast Lair
Mutalisk
Fast Third
Queen-heavy Defense
```

因此，当前 10 个簇适合作为**一级策略族或异常类型**，不适合作为最终 Skill 粒度。

## 2.2 Matchup 变体目前只是标签，不是真正的 Matchup 策略

目前 `{SID}-{Matchup}-A` 只是把全局簇按 matchup 重命名，并没有在：

```text
PvT / PvZ / PvP
TvP / TvZ / TvT
ZvP / ZvT / ZvZ
```

内部重新进行策略发现。

因此当前 30 个变体不能回答：

* TvP 中 Terran 有哪些开局；
* 同一个 Terran 主流簇在 TvP 和 TvZ 中是否实际对应不同科技分支；
* Protoss 面对 Zerg 和 Terran 时是否采用了不同的二矿与科技节奏。

后续必须执行真正的定向 matchup 内二次聚类。

## 2.3 Strategy Catalog 可能存在特征关联或生成错误

从当前报告表面看，需要重点复核：

* P-G04 的 medoid 接近标准 Gateway–CyberneticsCore–二矿路线，但名称和富集特征却高度指向 Forge/Cannon；
* P-G04 的画像中静态防御为 low，但 `first_static_defense_observed` 却为 94%；
* P-G04 和 P-G05 的富集特征数值完全相同；
* T-G01 和 T-G02 的富集特征数值完全相同；
* Z-G02 和 Z-G03 的富集特征也完全相同。

这可能来自：

1. 富集特征表错误地按种族复用；
2. cluster ID 与特征行 join 错位；
3. n-gram 名称字典错位；
4. medoid、画像和富集特征使用了不同版本的 cluster assignment；
5. 自动命名使用了错误的 top-feature row。

在修复这些问题前，不应让 LLM 根据现有 Catalog 自动生成 Skill。

## 2.4 当前优势结果还不足以直接形成响应规则

例如：

```text
T-G02 vs P-G04：q ≈ 0.086
P-G02 vs T-G01：q ≈ 0.082
```

均未通过严格的 FDR 0.05。

而：

```text
P-G04 vs T-G01：lift ≈ +0.3pp
```

虽然在大样本下显著，但实际效应非常小。

因此需要同时区分：

```text
统计显著性
实际效应大小
样本覆盖
跨玩家稳定性
跨地图稳定性
跨 MMR 稳定性
```

不能因为 q 值较小，就把 +0.3pp 写成一个 Agent 响应规则。

---

# 三、必须遵守的 naive Agent 运行约束

当前仓库中，Skill 文件位于：

```text
SKILL/<race>/<strategy>/Top_agent.md
```

运行开始时通过 `--force-strategy` 固定选择一个 Skill；`top_agent.py` 只提取 `# Summary` 下的内容，同一份 Summary 会在每次决策中重复提供。

naive Agent 的决策具有以下特点：

1. 初始时决策一次；
2. 默认每 60 游戏秒重新决策；
3. 队列被完全消耗时可能提前决策；
4. 每次只看到当前观测和未提交任务；
5. 上一轮的 reason、完整输出和历史队列不会保留；
6. 新队列完整替换旧的未提交队列；
7. 已经提交给游戏引擎的动作不能撤回；
8. LLM 不选择建筑位置、生产建筑、工人、攻击目标或微操。

因此生成的 Skill 必须满足：

* 不依赖隐藏的内部状态；
* 不使用“记住上一轮选择了什么”一类规则；
* 当前策略阶段必须能够从时间、Completed、Under Construction、Active Queues 和当前单位结构中重新推断；
* 响应规则只能引用 Agent 实际能看到的观测字段；
* 每条响应应指导未来约 60–120 秒的宏观动作，而不是输出完整整局 BO；
* 不要求 LLM发出攻击、撤退、侦察、施法、集结或位置指令；
* 所有最终动作都必须能映射到 exact canonical names。

当前观测已经包含 Enemy Intelligence、Threat Flags、Army/Income Advantage、损失、地图控制、已完成单位与科技等内容，可作为条件化 Skill 的运行时证据。

---

# 四、总体采用双路线建设 Skill

## 路线 A：现有 15 个可执行 Skill 的数据驱动重构

这是第一优先级，也是最容易产生真实性能提升的路线。

当前每个种族已有 5 个启用策略：

```text
Terran:
marine_rush
bio
blueflame_locks
two_base_matrix_tanks
yamato_rust_fleet

Protoss:
four_gate
dark_templar_rush
robo
voidray
macro_stalkers

Zerg:
twelve_pool
macro_roach
roach_hydra
lurkers
mutalisk
```

这些策略已经绑定相应的 `strategy_tools.py` 和 `AUTOMATION_PROFILE`。

推荐先完成：

> 将 replay 中的玩家轨迹映射到这 15 个已有策略原型，分析真实玩家在这些策略下如何根据对手变化进行调整，然后重写现有 `Top_agent.md`。

优势：

* 不需要立即新增战术控制代码；
* Skill 和现有攻击阈值、防守、侦察脚本更容易保持一致；
* 可以直接与当前手写 Summary 做 A/B 对比；
* 可以使用已有批量实验工具进行验证。

## 路线 B：发现新的数据驱动 Skill

当某个数据簇：

* 样本量充足；
* 跨玩家稳定；
* 与现有 15 个 Skill 都明显不同；
* 具有明确的宏观组成；
* 能够配置合理的自动攻击阈值和战术行为；

再新增：

```text
SKILL/<race>/<new_skill>/
    Top_agent.md
    skill.json
    evidence.json
    strategy_tools.py
```

新 Skill 不能只新增 Summary。必须同步提供与其目标一致的 `AUTOMATION_PROFILE`。

例如，一个希望积累较大部队再推进的 Skill，不能绑定过低的自动攻击阈值。仓库中的 Marine Rush 自动化配置固定了攻击阈值和自动行为，这类执行约束不能仅靠 Summary 改写。

---

# 五、Phase 9：修复与验证当前策略目录

## 5.1 建立 Catalog 一致性测试

对每个 cluster 检查：

```text
cluster assignment
cluster size
medoid replay
profile summary
top enriched features
top depleted features
key sequence
strategy name
```

必须全部来自相同的：

```text
race
cluster_id
window
feature_version
clustering_run_id
```

新增字段：

```text
run_id
feature_hash
cluster_assignment_hash
taxonomy_version
catalog_generation_version
```

## 5.2 自动执行逻辑一致性校验

例如：

```text
若 static_defense_profile == low
则 first_static_defense_observed 不应接近 100%

若名称含 Fast Expand
则 second_base timing 应显著早于种族基准

若名称含 Multi-Gateway
则 Gateway count 应显著高于基准

若名称含 One-base
则 300s 内 second base intent 不应高频出现
```

## 5.3 检查 Base 语义

当前 `Base`、`Base2`、`Base3` 必须明确表示：

* 第一次新建基地命令；
* 第二次新建基地命令；
* 还是包括初始基地。

建议改成不会产生歧义的名称：

```text
ExpansionOrder1
ExpansionOrder2
ExpansionOrder3
```

或：

```text
TownHallOrderedCountBy300
first_expansion_order_time
second_expansion_order_time
```

## 5.4 输出

```text
09_validation/
    catalog_consistency_report.md
    suspicious_clusters.csv
    feature_join_audit.csv
    cluster_medoid_audit.json
    taxonomy_unit_tests.json
```

## 5.5 验收标准

* 不再出现画像和富集特征直接矛盾；
* 每个 cluster 可回溯到具体 replay；
* 随机抽取 100 个 cluster–replay 对，关键序列正确率达到 95% 以上；
* 同一 cluster 的所有输出共享同一个 run ID。

---

# 六、Phase 10：将 replay 映射到已有 15 个 Skill

## 6.1 为什么需要 Skill Anchor

已有 Skill 是当前 Agent 的真实执行单位。

聚类簇只表示数据相似性，并不天然对应：

```text
marine_rush
bio
robo
voidray
macro_roach
lurkers
```

因此首先要为每个现有 Skill 建立一个 anchor signature。

## 6.2 Anchor 来源

按照优先级使用：

1. 原始 dummy build 中的资源投入动作；
2. 当前 Top_agent Summary 中的核心组成；
3. 专家手工定义的必要结构和禁用结构；
4. replay medoid；
5. 已有 Agent 对局日志中成功执行的宏观轨迹。

例如一个 Skill Anchor 可以包括：

```json
{
  "required_core": [
    "Barracks",
    "Factory",
    "Starport"
  ],
  "preferred_units": [
    "Marine",
    "SiegeTank",
    "Medivac"
  ],
  "preferred_upgrades": [
    "Stimpack"
  ],
  "expansion_profile": "two_base",
  "production_profile": "bio_heavy",
  "forbidden_early": [
    "FusionCore"
  ]
}
```

## 6.3 轨迹到 Skill 的匹配

计算：

[
Similarity(\tau, k)
===================

w_1 S_{\text{core sequence}}
+w_2 S_{\text{timing}}
+w_3 S_{\text{composition}}
+w_4 S_{\text{economy}}
+w_5 S_{\text{technology}}
]

输出：

```text
replay_player_id
candidate_skill
similarity
assignment_confidence
unmatched_reason
```

只使用高置信匹配样本学习 Skill：

```text
high confidence: ≥ 0.8
medium confidence: 0.6–0.8
unmatched: < 0.6
```

具体阈值通过人工抽查校准。

## 6.4 弱监督分类器

在初始高置信 anchor 样本上训练分类器：

```text
输入：300s / 420s opening features
输出：15 个 Skill + Other
```

推荐：

* LightGBM；
* XGBoost；
* multinomial logistic；
* calibrated random forest。

输出必须提供：

```text
skill probability
top competing skill
feature attribution
```

## 6.5 验收标准

每个现有 Skill 至少满足：

* 200 个以上高置信 replay，或标记为数据不足；
* 来自至少 20 名不同玩家；
* top discriminative features 与 Skill 目标一致；
* 专家抽查准确率达到 80% 以上。

---

# 七、Phase 11：主流簇内的真正 Matchup 二次聚类

## 7.1 分析空间

必须使用九个定向空间：

```text
PvP PvT PvZ
TvP TvT TvZ
ZvP ZvT ZvZ
```

虽然一场对局通常写成 PvT，但从玩家视角：

```text
Protoss vs Terran
Terran vs Protoss
```

是两个不同建模任务。

## 7.2 分层聚类结构

推荐：

```text
Race
  └── Matchup
       └── Existing Skill Anchor / Global Family
            └── Opening Subtype
                 └── Response Variant
```

例如：

```text
Terran
  └── TvP
       └── bio
            ├── Reaper Expand
            ├── 3-Rax Pressure
            ├── Fast Tank
            └── Fast Medivac
```

## 7.3 时间窗口

将策略拆成三个阶段：

```text
0–210s：Opening Commitment
210–420s：Opponent-conditioned Response
420–720s：Transition
```

当前只有 210/300/420 特征，下一步应增加：

```text
480s
540s
600s
720s
```

使用 Landmark Analysis 处理短局右删失。

## 7.4 聚类特征

开局聚类重点使用：

```text
first gas timing
first expansion timing
second/third production timing
first tech structure
production structure counts
key unit first order
key unit counts
upgrade timing
worker production continuity
static defense count
air/ground technology commitment
```

对主流簇内部，减少以下特征的权重：

```text
第一 Supply
第一基础生产建筑
种族固定动作
几乎人人都会执行的动作
```

## 7.5 算法

不建议继续只用一次 HDBSCAN。

推荐：

```text
1. MiniBatchKMeans / BIRCH 做大规模粗分
2. K-medoids 提取真实代表 BO
3. HDBSCAN 识别噪声和小众变体
4. Bootstrap 验证稳定性
```

聚类数量不能只根据 silhouette 决定，还应要求：

* 策略语义可解释；
* medoid 明显不同；
* 关键 timing 有显著差异；
* 在 holdout 数据上可重现；
* 对后续动作或结果具有区分度。

## 7.6 Skill 粒度标准

一个候选开局分支至少满足：

```text
样本量 ≥ 300
不同玩家 ≥ 30
matchup 内占比 ≥ 1%
bootstrap retention ≥ 0.70
至少一个关键宏观特征 RR ≥ 1.5
```

低频但稳定的特殊策略可以保留为 niche candidate，但不直接加入 naive Skill。

---

# 八、Phase 12：建立对手风格模型

需要区分两类“对手风格”。

## 8.1 玩家历史风格

从某个玩家过去的比赛中统计：

```text
early aggression frequency
fast expansion frequency
technology preference
air preference
ground preference
static defense tendency
strategy diversity
opening repetition rate
```

得到：

```text
PlayerStylePrior
```

只能使用当前比赛之前的历史记录计算，不能使用未来比赛。

这一部分适用于：

* 已知职业选手；
* 固定对手；
* 长期联赛；
* Agent 重复对战。

对匿名天梯或内置 AI，其作用有限。

## 8.2 当前对局中的动态风格

这是 Skill 最重要的部分。

在每个时间点 (t) 定义对手风格向量：

[
S_t =
[
Econ_t,
Production_t,
Tech_t,
Defense_t,
Air_t,
Ground_t,
AllInRisk_t
]
]

其中：

### Economy

```text
基地数量与 timing
worker production
gas/矿投入比例
第三基地倾向
```

### Production

```text
基础产能数量
高级产能数量
生产密度
```

### Technology

```text
科技层级
科技建筑 timing
升级投入
```

### Defense

```text
静态防御数量
防御建筑 timing
```

### Composition

```text
air / ground
bio / mech
gateway / robotics / stargate
ling-bane / roach / hydra / mutalisk
```

### All-in Risk

```text
单基地
过量早期产能
工人生产停滞
扩张缺失
大量早期战斗单位
```

## 8.3 连续分数和离散标签同时保留

连续风格分数用于统计模型：

```text
economy_score = 0.73
aggression_score = 0.18
tech_score = 0.52
```

离散标签用于 LLM Skill：

```text
Greedy Expansion
One-base Production Pressure
Fast Air Technology
Ground Technology
Defensive Macro
Balanced Standard
```

## 8.4 Oracle Style 与 Observable Style

这是科学性和可执行性的关键区别。

Replay 中能看到对手完整 BO，但在线 Agent 只能看到已经侦察到的 Enemy Intelligence 和 Threat Flags。

因此必须建立两套标签：

### Oracle Style

由对手真实完整动作计算，用于离线统计和上界分析。

### Observable Style

只由当前 Agent 可以获得的证据描述：

```text
observed enemy structures
observed enemy units
remembered enemy counts
threat flags
army advantage
income advantage
map control
```

最终 Skill 只能使用 Observable Style。

不能在 Skill 中写：

```text
如果对手属于 P-G03
```

而必须写成：

```text
如果 Enemy Intelligence 已经显示多个早期 Gateway，
并且未观察到对手二矿，应视为高产能一矿压力风险。
```

如果 replay 数据无法还原当时是否侦察到某个动作，则该规则只能标记为：

```text
oracle-supported
runtime translation requires validation
```

---

# 九、Phase 13：分析双方策略如何演化

## 9.1 从单一标签转向策略轨迹

每个玩家不再只有一个 opening cluster，而表示为：

```text
Opening O
→ Response R
→ Transition T
```

例如：

```text
Gate Expand
→ Defensive Robotics
→ Colossus Transition
```

或：

```text
Reaper Expand
→ Extra Barracks Response
→ Bio-Medivac Scaling
```

## 9.2 每 60 秒建立策略状态

建议在：

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

游戏秒生成状态。

每个状态包含：

```text
economy state
production state
technology state
composition state
defense state
army commitment
```

## 9.3 构建状态转移图

每条边：

```text
OwnState_t
+ OpponentStyle_t
→ OwnState_t+60
```

统计：

```text
support
transition probability
conditional lift
median action delay
win rate
adjusted win probability
player coverage
```

## 9.4 条件序列规则

使用 PrefixSpan 或序列规则挖掘：

```text
Own opening = O
Opponent evidence = S
⇒ Own next response = R
```

例如结构上表示为：

```text
Gate Expand
+ observed early air technology
⇒ add anti-air technology and appropriate unit production
```

每条规则需要报告：

[
Confidence(O,S\rightarrow R)
]

[
Lift(O,S\rightarrow R)
]

以及采用该响应后的调整结果。

## 9.5 区分真实响应与共同时间趋势

必须满足：

1. 对手风格证据先于己方响应；
2. 己方响应在合理时间差内出现；
3. 同一阶段的普通发展动作不能误认为响应；
4. 与没有该对手证据的同开局对局比较；
5. 控制 matchup、地图、版本和玩家实力。

建议响应时间窗口：

```text
证据出现后 30–120 游戏秒
```

## 9.6 反应延迟

对每个响应计算：

```text
response_delay
```

分析：

* 快速响应是否关联更好；
* 过早盲目转型是否损害经济；
* 某些响应是否只有在明确证据后才有效。

---

# 十、Phase 14：估计响应分支的条件价值

## 10.1 分析单位

每条样本构造成：

```text
own opening
opponent style at t
own state at t
candidate response during t→t+Δ
map
patch
MMR difference
player identity
opponent identity
outcome
```

## 10.2 核心价值定义

对某个响应 (r)：

[
\Delta V(r\mid o,s,c)
=====================

## P(\text{win}\mid r,o,s,c)

P(\text{win}\mid r_0,o,s,c)
]

其中：

* (o)：我方基础开局；
* (s)：对手风格；
* (c)：当前经济、科技、兵力上下文；
* (r_0)：该场景下最常见的默认响应。

## 10.3 层级模型

推荐模型：

[
\text{logit},P(Y=1)
===================

\alpha
+\beta_o
+\gamma_s
+\eta_r
+\delta_{o,s,r}
+\theta^\top X
+u_{\text{player}}
-u_{\text{opponent}}
+v_{\text{map}}
+w_{\text{patch}}
]

当前 L2 Logistic 控制了 MMR、地图、Patch 和 Region，但下一版必须进一步处理：

```text
同一玩家重复出现
同一对手重复出现
玩家具有稳定策略偏好
```

可选实现：

* PyMC crossed random-effects logistic；
* statsmodels mixed model 的近似方案；
* player/opponent fixed effects；
* 按 player pair 或 player 聚类的 bootstrap；
* 使用赛前 Elo/Glicko 替代或补充 MMR。

## 10.4 Propensity 与重叠

一个响应不是随机选择的。

例如高手可能更容易：

* 正确侦察；
* 及时转型；
* 选择更复杂的科技路线。

因此估计：

[
P(R=r\mid O,S,C,X)
]

并使用：

* overlap weighting；
* doubly robust estimation；
* generalized propensity score。

当不同响应之间没有足够特征重叠时，不输出比较结论。

## 10.5 Skill 规则准入标准

建议只有同时满足以下条件的规则才能进入正式 Skill：

```text
样本量 ≥ 300
不同玩家 ≥ 30
有效样本量 ≥ 200
|adjusted lift| ≥ 3pp
posterior P(lift > 0) ≥ 0.90
或 FDR q < 0.05
player-balanced 方向一致
至少两个 MMR 层方向一致
至少三张地图方向一致
```

其他规则分为：

```text
candidate
exploratory
unsupported
```

当前 T-G02 vs P-G04 等结果最多应进入 candidate hypothesis，不能直接作为正式决策规则。

## 10.6 需要额外分析的结果

除了最终胜率，还应分析：

```text
5–8 分钟存活率
10 分钟经济差
10 分钟军队价值差
对局时长
早期获胜概率
早期失败概率
供应阻塞
资源积压
科技响应延迟
```

某种响应可能不提高最终胜率，但显著降低早期崩盘风险，这仍然可能是有价值的 Skill 规则。

---

# 十一、Phase 15：构建结构化 Skill

## 11.1 Skill 不直接以 Markdown 为唯一源文件

推荐建立：

```text
skill.json       机器可读的策略政策
evidence.json    统计证据和来源
Top_agent.md     编译后供 naive Agent 使用
strategy_tools.py
```

`Top_agent.md` 是编译产物，不是唯一真值。

## 11.2 skill.json Schema

```json
{
  "skill_id": "terran_bio_tvp_v1",
  "race": "terran",
  "opponent_race": "protoss",
  "base_family": "bio",
  "opening_archetype": "reaper_expand_bio",
  "version": "1.0",
  "automation_profile": "bio",
  "applicability": {
    "patch_groups": [],
    "mmr_range": [],
    "maps": []
  },
  "objective": "",
  "default_policy": [],
  "phase_targets": [],
  "response_rules": [],
  "transition_rules": [],
  "invariants": [],
  "abandon_conditions": [],
  "fallback_policy": [],
  "evidence_refs": []
}
```

## 11.3 Response Rule Schema

```json
{
  "rule_id": "R_TVP_04",
  "priority": 20,
  "phase": {
    "start": 240,
    "end": 480
  },
  "condition": {
    "all": [
      {
        "field": "enemy_intelligence",
        "predicate": "contains_any",
        "values": ["observable_air_tech", "observable_air_unit"]
      }
    ]
  },
  "interpretation": "Opponent has shown credible air commitment.",
  "response_package": {
    "composition_adjustment": [],
    "technology_adjustment": [],
    "production_adjustment": [],
    "economy_adjustment": []
  },
  "do_not": [],
  "fallback_rule": "R_TVP_DEFAULT",
  "evidence": {
    "support": 0,
    "unique_players": 0,
    "adjusted_lift": 0.0,
    "interval": [],
    "confidence": "A"
  }
}
```

## 11.4 规则优先级

推荐固定为：

```text
0  生存危机与硬性反制
1  供应、前置条件和可执行性
2  对手明确科技或兵种响应
3  对手经济与产能风格响应
4  默认开局和组成目标
5  长期扩张和升级
```

当多个规则同时触发：

* 高优先级覆盖低优先级；
* 同级规则只允许合并不冲突的 macro package；
* 每个决策周期最多激活 2 个主要响应包；
* 避免把 10 个条件同时写入同一队列。

## 11.5 规则必须无状态或可重建

错误形式：

```text
上一轮已经选择防空分支，所以继续执行。
```

正确形式：

```text
如果已经完成防空科技，但当前防空单位数量仍不足，
继续生产相应单位；如果科技尚未开始，则优先补齐前置科技。
```

因为 naive Agent不会保留上一轮 reason，只能从当前观测重建策略状态。

---

# 十二、Top_agent.md 编译格式

当前 parser 只提取 `# Summary` 内容，因此可以在 Summary 内使用二级标题。

推荐格式：

```markdown
# Summary

## Applicability
This skill is designed for Terran against Protoss.

## Core Objective
一句话说明基础开局、经济规模、核心组成与取胜方式。

## Default Opening Policy
- 0–180s 的经济、产能和科技目标。
- 180–300s 的默认发展方向。
- 不输出完整整局 BO，只说明未来一个决策窗口的优先目标。

## Phase Identification
- 根据游戏时间、Completed、Under Construction 和 Active Queues
  判断当前处于 opening、response 或 transition 阶段。

## Observable Opponent Responses
1. 如果观察到明确的一矿高产能压力……
   - 优先……
   - 暂缓……
2. 如果观察到快速空军科技或空军单位……
   - 增加……
   - 保留……
3. 如果对手快速扩张且当前没有直接威胁……
   - 加速……
   - 不要过量投入静态防御。

## Composition Transition
- 默认组成达到什么条件后转向什么。
- 哪些敌方兵种或科技会改变组成。

## Economy And Production Scaling
- 何时扩张。
- 当前资源积压时优先增加什么产能。
- 哪些情况下停止继续扩张。

## Abandon Conditions
- 哪些证据意味着原来的科技路线已经不合适。
- 哪些未提交任务应该从下一轮替换队列中移除。

## Invariants
- 必须保持的核心组成。
- 不允许的无关科技。
- 不重复已经 Under Construction 或 Active Queues 的动作。
```

## 12.1 Summary 长度

建议每个 matchup Skill：

```text
600–1,000 英文 tokens
5–8 条主要响应规则
最多 3 个组成转型
```

不能把整个统计报告放入 Summary。

## 12.2 不能写入 Summary 的内容

```text
详细回归系数
所有样本表格
长篇解释
完整 Build Order
不可观察的 opponent cluster ID
攻击目标
建筑坐标
微操要求
隐藏的思维链
```

统计证据保存在 `evidence.json`。

---

# 十三、LLM 描述与标注流程

LLM 不能直接读取聚类 ID 后自由命名。

应采用四步流水线。

## 13.1 Step A：事实摘要

输入：

```text
medoid sequence
top discriminative features
timing median/IQR
composition counts
expansion profile
transition probabilities
response value
support
```

LLM 只输出结构化事实描述。

## 13.2 Step B：策略命名

要求 LLM 生成：

```text
professional_name
data_driven_name
macro_family
opening_commitment
transition_direction
```

名称必须由至少两个稳定特征支持。

## 13.3 Step C：Skill 编译

将结构化规则转换为符合 naive Agent 的 Summary。

约束：

* 只能引用观测字段；
* 只能描述 macro spending；
* 每个响应都必须有明确条件；
* 不得隐含不可执行位置行为；
* 不得要求取消已提交动作；
* 不得生成超出 canonical allowlist 的名称；
* 不得要求 LLM 控制脚本拥有的行为。

## 13.4 Step D：LLM Critic + 程序验证

Critic 检查：

```text
统计证据是否支持
是否把关联写成因果
条件是否在线可观察
是否与基础策略矛盾
是否与 automation profile 矛盾
canonical names 是否合法
前置建筑是否缺失
响应规则是否冲突
Summary 是否过长
```

最终必须经过程序校验，而不是只依赖另一个 LLM。

---

# 十四、Skill 与 strategy_tools.py 的一致性

每个 Skill 都需要生成一份兼容性报告：

```text
skill objective
desired army size
desired attack timing
desired composition
automation attack threshold
automation attack gate
automatic scouting
automatic defense
special behaviors
```

例如，如果 Skill 描述：

```text
积累两基地坦克与生化部队后再进行主要推进
```

但 automation profile 在很低的 combat-power threshold 就自动攻击，则两者不一致。

当前 `strategy_tools.py` 负责攻击阈值、防守、侦察、集结和种族自动行为，而不是第二个宏观规划器。

建议输出：

```text
automation_alignment = pass / warning / fail
```

只有 pass 的 Skill 才加入 registry。

---

# 十五、Phase 16：仓库集成方案

## 15.1 推荐目录

```text
analysis/
  outputs/
    09_validation/
    10_skill_alignment/
    11_matchup_clusters/
    12_opponent_styles/
    13_strategy_evolution/
    14_response_value/
    15_skill_candidates/
    16_skill_evaluation/

skill_compiler/
  schema/
    skill.schema.json
  build_skill.py
  compile_top_agent.py
  validate_skill.py
  validate_canonical_names.py
  validate_automation_alignment.py
```

每个 Skill：

```text
SKILL/terran/bio/
    skill.json
    evidence.json
    Top_agent.md
    strategy_tools.py
```

## 15.2 第一版不修改 naive 决策接口

继续保持：

```json
{
  "reason": "...",
  "ordered_names": []
}
```

不添加新的 Agent，不添加 Skill Retrieval Agent，不修改 scheduler。

只修改：

* Skill 的 Summary；
* Skill 的证据文件；
* 必要时修改对应 automation profile；
* registry 中启用的 Skill。

这样可以确保性能变化主要来自 Skill，而不是 harness 变化。

## 15.3 Matchup Skill 的组织方式

有两种方案。

### 方案 A：每个基础 Skill 内包含三个 matchup 分支

例如：

```text
bio
  Against Terran
  Against Protoss
  Against Zerg
```

优点是兼容当前目录结构。

缺点是 Summary 更长，LLM 可能混淆不同 matchup。

### 方案 B：每个 matchup 独立 Skill

例如：

```text
bio_tvt
bio_tvp
bio_tvz
```

更推荐方案 B。

因为敌方种族在开局前已经已知，独立 Skill：

* Prompt 更短；
* 响应规则更专一；
* 统计证据更清晰；
* 更容易做 A/B 测试。

可在 registry 中增加：

```json
{
  "name": "bio_tvp",
  "allowed_enemy_races": ["protoss"],
  "automation_profile": "bio"
}
```

这是一个较小的确定性改动，不改变 naive 每轮决策机制。

---

# 十六、Phase 17：离线评估

## 16.1 策略分类评估

使用：

```text
player-disjoint split
time-disjoint split
map-disjoint split
```

报告：

```text
Skill assignment accuracy
macro-F1
calibration
Other rejection accuracy
```

## 16.2 下一阶段动作预测

给定：

```text
当前状态
对手可观察风格
当前 Skill
```

预测玩家接下来 60 秒执行的宏观动作。

指标：

```text
top-k next action accuracy
action-set F1
sequence edit distance
technology branch accuracy
expansion decision accuracy
composition transition accuracy
```

这能够验证 Skill 是否真正概括了人类策略演化，而不是只与最终胜负相关。

## 16.3 规则覆盖

每个 Skill 报告：

```text
多少决策状态命中默认路线
多少命中响应规则
多少同时命中冲突规则
多少没有任何适用规则
```

推荐：

```text
规则覆盖率 ≥ 80%
冲突率 ≤ 5%
无规则状态 ≤ 15%
```

## 16.4 Shadow Agent 测试

将历史状态转成 naive Agent 可读的 observation，运行：

```text
现有 Summary
数据驱动静态 Summary
数据驱动自适应 Summary
```

比较：

* 输出是否合法；
* 是否符合对应响应规则；
* 是否重复已提交任务；
* 是否缺少前置建筑；
* 是否产生过长队列；
* 是否与专家后续动作一致。

由于 replay 数据没有完整的历史侦察视角，Shadow 测试必须区分：

```text
oracle observation
runtime-like observable observation
```

---

# 十七、Phase 18：在线 SC2 对战实验

## 17.1 主要实验组

对每个 Skill 比较：

```text
A. 当前手写 Top_agent Summary
B. 数据驱动默认路线，无响应规则
C. 数据驱动默认路线 + 对手响应规则
D. C，但删除效果过滤，保留所有高频响应
E. 无具体 Skill 的通用宏观 Summary
```

其中：

```text
B vs C
```

直接检验“对手变化响应”是否有价值。

```text
C vs D
```

检验统计收益过滤是否有价值。

## 17.2 控制变量

保持一致：

```text
LLM model
reasoning mode
temperature
decision interval
map set
enemy race
enemy difficulty
automation profile
scheduler
game version
```

## 17.3 实验矩阵

Pilot：

```text
每个 Skill × enemy race × 30 局
```

正式实验：

```text
每个核心 cell 至少 50–100 局
```

优先选择：

* 当前表现较差的 matchup；
* 有明确响应规则的 Skill；
* 历史数据支持最大的场景；
* 当前自动化 profile 与 Skill 一致的策略。

## 17.4 主要指标

### Outcome

```text
win rate
Wilson interval
game duration
early loss rate
```

### Macro Quality

```text
worker saturation
resource bank AUC
supply block duration
army supply
production utilization
expansion timing
upgrade timing
```

### Response Quality

```text
opponent evidence time
first correct response time
response delay
incorrect blind response rate
technology abandonment rate
```

### LLM Decision Quality

```text
valid JSON rate
canonical mapping rate
queue acceptance rate
average queue length
missing prerequisite rate
discarded important carry-over rate
```

### Efficiency

```text
tokens per decision
latency
decisions per game
```

## 17.5 轨迹级分析

每局生成：

```text
evidence detected
active rule
generated queue
accepted actions
completed/committed actions
next observation
rule outcome
```

这样可以进一步积累：

> Skill 规则在 Agent 实际运行中的执行轨迹。

这些轨迹可以回流到下一轮 Skill evolution。

---

# 十八、建议的第一轮实施范围

不要一开始生成几十个新 Skill。

推荐第一轮只做：

## Terran

```text
bio
two_base_matrix_tanks
marine_rush
```

## Protoss

```text
robo
voidray
four_gate
```

## Zerg

```text
macro_roach
roach_hydra
mutalisk
```

每个策略优先只选择一个样本量最大的 matchup。

形成 9 个 pilot Skill。

每个 Skill：

```text
1 个默认路线
3–5 个对手响应规则
1–2 个组成转型
1 个 fallback
```

第一轮重点验证：

* Summary 是否能被 naive Agent 正确执行；
* 条件响应是否真的改变队列；
* 是否比当前长段落式 Summary 更稳定；
* 是否与 automation profile 对齐；
* 是否降低宏观错误。

---

# 十九、具体执行顺序

## Stage 1：修复当前输出

```text
Phase 9
Catalog 一致性与特征 join 审计
```

## Stage 2：与现有 Agent 策略对齐

```text
Phase 10
构建现有 15 个 Skill Anchor
将 replay 映射到 Skill
```

## Stage 3：发现细粒度 matchup 路线

```text
Phase 11
主流簇内二次聚类
```

## Stage 4：学习对手风格和策略演化

```text
Phase 12
Opponent Style

Phase 13
Opening → Response → Transition
```

## Stage 5：筛选有价值的响应

```text
Phase 14
条件价值与稳健性模型
```

## Stage 6：生成 Skill

```text
Phase 15
skill.json + evidence.json + Top_agent.md
```

## Stage 7：集成和验证

```text
Phase 16
仓库集成

Phase 17
离线 Shadow Evaluation

Phase 18
在线 SC2 A/B Test
```

---

# 二十、最终产物

```text
adaptive_skill_catalog.json
skill_assignment_model/
opponent_style_model/
strategy_transition_graph.json
response_value_table.parquet
observable_response_rules.json
```

每个 Skill：

```text
skill.json
evidence.json
Top_agent.md
strategy_tools.py
validation_report.json
```

全局报告：

```text
skill_coverage_report.md
skill_value_report.md
automation_alignment_report.md
offline_imitation_report.md
online_ablation_report.md
```

---

# 二十一、最终验收标准

一个 Skill 可以正式用于 naive Agent，必须满足：

1. 基础策略与现有 automation profile 一致；
2. 使用 exact canonical macro names；
3. 不要求控制位置、攻击、微操或侦察；
4. 每个条件均可从当前 observation 判断；
5. 不依赖上一轮 reason 或隐藏记忆；
6. 默认路线和响应路线不存在明显冲突；
7. 每条正式响应具有足够样本和调整后收益证据；
8. 玩家隔离、时间隔离测试方向稳定；
9. Shadow 测试中 canonical mapping rate 不低于 99%；
10. 在线对战中合法决策率不下降；
11. 对手风格响应延迟显著低于静态 Summary；
12. 至少在部分 matchup 上提高胜率或降低早期失败率。

---

# 二十二、核心研究表述

这一工作的研究主线可以概括为：

> We mine hierarchical opening archetypes and opponent-conditioned strategy transitions from large-scale StarCraft II replays, estimate the context-dependent value of alternative responses, and compile statistically supported transition policies into executable skills for periodically replanned LLM agents.

它不再只是：

> 从 replay 中总结几个常见 BO。

而是：

> 从大规模轨迹中挖掘“策略—观察—响应—结果”的条件化知识，并将其编译为能够适配动态对手的 LLM Agent Skill。
