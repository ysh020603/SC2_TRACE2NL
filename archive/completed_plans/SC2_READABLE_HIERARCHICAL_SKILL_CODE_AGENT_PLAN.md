# SC2 Human Trace → Readable Hierarchical Skill + Interactive Skill Agent
## 给 Code Agent 的完整执行方案

> **归档状态：已完成（2026-08-10）**
> 本文档保留为 Readable Skill 编译器和交互式 Skill Agent 的设计/验收依据，
> 不再作为待执行计划。最终 Agent 代码已进入 `SC2-Agent-knowlegde` 的
> `SC2-Agent-trace2skill` 分支，替换提交为 `5a60b71`；Readable 产物和编译流水线
> 位于本 outer repo 的已提交代码中。

### 最终实现与产物

- `analysis/readable_skill_v1/` 已实现六方法独立证据 IR、观测语义投影、LLM
  标注、分层编译、验证和 provenance；
- `SKILL_MINING_V2_READABLE/` 已生成 57 个 opening × 6 个方法，共 342 个
  Skill、342 个 method IR、342 个 projection、342 个独立 LLM annotation 和
  2,975 个节点 Markdown；
- 六方法均为每方法 57 个 Skill，最终 annotation source 全部为 LLM，
  `reasoning_present=0`、`api_errors=0`、`fallback=0`、validation failure 为 0；
- Readable pipeline 的关键 outer repo 提交为 `6ba2890`，Full-v2 guarded skill
  更新提交为 `50f199e`；
- Agent 侧实现了 Full、Single Trace、Static Population、Flat Adaptive、
  Positive Only、Frequency Only 六个独立 pinned package，并增加
  `full_guarded_graph_v2`；
- runtime 支持受限 `READ_SKILL`/`FINAL_DECISION` 多轮协议、match-scoped memory、
  schema v5 trace、node-read 记录、路径与 provenance 校验；
- DeepSeek-V4-flash 和 qwen3-32b 均通过 non-thinking 门禁；跨模型完整对局结果
  与高并发稳定性属于后续实验记录，不再修改本计划正文。

### 后续运行时记录

SC2 高并发 observation timeout 与 Python 异常退出问题单独记录在 Agent 仓库
`docs/SC2_HIGH_CONCURRENCY_TIMEOUT_AND_EXIT_INCIDENT.md`。该问题不影响 342 个
Readable Skill 均已完成 LLM 标注、编译和静态验证的事实。

> 目标仓库：`/data2/shy_2608/SC2trace2nl/SC2_TRACE2NL`（以实际本地目录为准）
> Agent 基线：`/data2/shy_2608/SC2trace2nl/SC2-Agent-knowlegde`
> 原始 Skill 产物：`SKILL_MINING_V2/`
> 核心要求：**保留现有 V2 统计挖掘与原 Agent，不覆盖、不原地修改；新增 Readable Skill 编译流水线，并为 full + 5 个 ablation 建立各自独立的 Agent 版本。**

---

# 0. 最简执行版

整个任务分为两部分。

## Part A — 把 V2 统计产物编译成 Agent 可直接阅读的分层 Skill

保留已有：

```text
Human Replay
→ Opening Discovery
→ State Mining
→ Transition Mining
→ Transition Value
→ Signed Strategy Graph
```

新增：

```text
V2 Statistical Evidence
        ↓
Method-specific Evidence IR
        ↓
Observation-Compatible Semantic Projection
        ↓
LLM Semantic Annotation
        ↓
Hierarchical Skill Compilation
        ↓
Readable Markdown Skill
```

最终每个 Skill 对应一个 **Opening Strategy**。

第一层 `SKILL.md` 必须包含：

1. 这个 Skill 对应的开局策略；
2. 开局的核心战略意图；
3. 经济 / 科技 / 产能 / 兵力方向上的主要特点；
4. 所有下级节点摘要；
5. 每个节点的：
   - 触发态势；
   - 简单决策方向；
   - 节点性质，例如 `POSITIVE / NEGATIVE / DEFAULT`；
6. 不出现 action list；
7. 不出现敌方 replay action list；
8. 不要求 Agent 精确匹配 cluster ID。

模型需要更多知识时，再继续读取某个节点的完整 Markdown。

## Part B — 新建独立 Skill Agent

不要修改原始 naive Agent。

新建独立工作目录，例如：

```text
/data2/shy_2608/SC2trace2nl/SC2-Agent-human-skill/
```

建立六个明确独立的 Agent 版本：

```text
human-skill-full
human-skill-single-trace
human-skill-static-population
human-skill-flat-adaptive
human-skill-positive-only
human-skill-frequency-only
```

运行时：

```text
Current OBS
+
Opening Skill Root
+
Previously Read Skill Nodes
+
Available Node Summaries
        ↓
LLM
        ├── READ_SKILL(node_id)
        ├── READ_SKILL(node_id)
        └── FINAL_DECISION
                ↓
        {reason, ordered_names}
                ↓
        原 ExecutionScheduler
```

已完整读取过的节点进入该场比赛的 `Skill Read Memory`，以后每次决策都重新出现在 context 中。

---

# 1. 非协商约束

## 1.1 不覆盖旧实验产物

以下作为只读输入：

```text
analysis/skill_mining_v2/
analysis/outputs_skill_v2/
SKILL_MINING_V2/
```

不要原地改写已有：

```text
stage10_annotation_packets.py
stage11_llm_annotation.py
stage12_skill_compile.py
stage13_ablation_generation.py
stage14_validation.py
```

原 V2 必须继续可复现。

## 1.2 不修改原 Agent baseline

原目录：

```text
/data2/shy_2608/SC2trace2nl/SC2-Agent-knowlegde
```

不直接修改。

优先：

```bash
git worktree add ../SC2-Agent-human-skill <new-branch>
```

如果本地结构不允许 worktree，再复制成独立目录。

生成：

```text
READABLE_SKILL_BASELINE_MANIFEST.json
```

至少记录：

```text
baseline_repo
baseline_branch
baseline_commit
skill_mining_repo_commit
new_agent_repo
new_agent_branch
created_at
```

## 1.3 Agent-facing Skill 禁止 action list

最终给 Agent 阅读的 Markdown 禁止出现：

```text
canonical_actions
ordered action sequence
response action list
enemy action list
raw replay action list
```

允许在自然语言态势描述中出现单位名，例如：

```text
Enemy Intelligence is mainly consistent with Stalkers and Immortals,
with little evidence of Phoenix or Void Ray presence.
```

单位名是态势线索，不是执行顺序。

## 1.4 Skill 只提供方向，最终 action 必须由 LLM 根据实时 OBS 产生

允许：

```text
Strengthen the existing ground army and production path before taking
additional economic risk.
```

禁止：

```text
Build Gateway → Stalker → Immortal → Pylon.
```

最终仍由模型输出：

```json
{
  "reason": "...",
  "ordered_names": ["Pylon", "Gateway", "Stalker", "Immortal"]
}
```

## 1.5 Signed label 不能由 LLM 重新判断

以下标签只能来自统计 pipeline：

```text
preferred / positive
harmful / negative
default
frequency-selected
single-trace
```

LLM 只负责解释、语义压缩和自然语言化，禁止把 `frequency` 改写成 `positive`，也禁止把 `harmful` 改写成 `positive`。

---

# 2. 新增 Readable Skill Pipeline

新建：

```text
analysis/readable_skill_v1/
│
├── README.md
├── config.py
├── run_pipeline.py
│
├── common/
│   ├── io.py
│   ├── schemas.py
│   ├── obs_vocabulary.py
│   ├── method_policy.py
│   ├── provenance.py
│   └── validation.py
│
├── prompts/
│   ├── opening_annotation.md
│   ├── own_state_annotation.md
│   ├── opponent_state_annotation.md
│   ├── transition_annotation.md
│   └── hierarchy_consolidation.md
│
├── stage00_manifest.py
├── stage01_method_evidence_ir.py
├── stage02_observation_projection.py
├── stage03_llm_semantic_annotation.py
├── stage04_hierarchy_compile.py
├── stage05_validation.py
└── stage06_catalog.py
```

输出：

```text
analysis/outputs_readable_skill_v1/
SKILL_MINING_V2_READABLE/
```

---

# 3. 必须先做 Method-specific Evidence IR

当前 ablation 不能直接复用 full 的 annotation。

正确顺序必须是：

```text
Full statistical outputs
        ↓
Apply method / ablation information boundary
        ↓
Method-specific Evidence IR
        ↓
Observation Projection
        ↓
Method-specific LLM Annotation
        ↓
Method-specific Markdown Skill
```

禁止：

```text
Full annotation
→ 删除少量字段
→ 当成 ablation annotation
```

这会导致消融信息泄漏。

---

# 4. 六种 Method 的严格信息边界

统一定义：

```python
METHODS = {
    "full_signed_graph": ...,
    "ablation_single_trace": ...,
    "ablation_static_population": ...,
    "ablation_flat_adaptive": ...,
    "ablation_positive_only": ...,
    "ablation_frequency_only": ...,
}
```

## 4.1 full_signed_graph

允许：

```text
population opening
own state
opponent-conditioned state
preferred edges
harmful edges
default edges
value filtering
graph transition
next-state relation
```

节点 Badge：

```text
POSITIVE
NEGATIVE
DEFAULT
```

允许显示下级转移节点。

## 4.2 ablation_single_trace

只允许：

```text
一个 winning representative trace
opening identity
该 trace 自己的 macro trajectory
```

禁止：

```text
population prevalence
population response statistics
opponent-conditioned transition statistics
preferred / harmful labels
full graph annotation
```

为了保持最终格式相似，从这一条 trace 的时间序列构建：

```text
opening
phase continuation nodes
```

若 `source_trace` 没有足够时间信息，用 replay_id 回到 trajectory parquet，只提取这一条 replay 的宏观轨迹。

节点 Badge：

```text
TRACE
```

不能显示 `POSITIVE / NEGATIVE`。

## 4.3 ablation_static_population

允许：

```text
population opening statistics
population-common continuation
own-state / phase information
```

禁止：

```text
opponent-conditioned adaptive rules
positive / negative comparison
graph path
```

节点 Badge：

```text
COMMON
DEFAULT
```

trigger 只能主要描述自己的阶段 / 战略进展，不能使用 opponent-conditioned trigger。

## 4.4 ablation_flat_adaptive

允许：

```text
opponent-conditioned adaptive rules
positive
negative
default
value filtering
```

禁止：

```text
graph topology
next-state path
multi-hop transition guidance
```

最终仍生成 `SKILL.md + nodes/*.md`，但任何节点禁止出现 `Possible Next Nodes`。

Badge：

```text
POSITIVE
NEGATIVE
DEFAULT
```

## 4.5 ablation_positive_only

允许：

```text
population
opponent adaptation
graph
value filtering
preferred / positive
default
```

禁止：

```text
harmful / negative evidence
negative path
```

Badge：

```text
POSITIVE
DEFAULT
```

Agent-facing 文本不能出现基于被移除 negative evidence 的“historically harmful / worse outcome”描述。

## 4.6 ablation_frequency_only

只根据：

```text
transition frequency / p_response
```

选取 response。

不能利用：

```text
adjusted_lift
preferred/harmful value label
win enrichment
outcome-based sign
```

因此最高频不能写成 `POSITIVE / BEST / PREFERRED`。

Badge：

```text
FREQUENT
COMMON
```

---

# 5. Stage 01 — Method-specific Evidence IR

每个 opening × method 生成：

```text
01_method_ir/<method>/<opening_id>.json
```

统一 schema：

```json
{
  "method": "full_signed_graph",
  "opening_id": "PvP_O01",
  "race": "Protoss",
  "opponent_race": "Protoss",
  "opening_evidence": {},
  "own_states": [],
  "opponent_states": [],
  "transitions": [
    {
      "source_state_id": "...",
      "opponent_state_id": "...",
      "next_state_id": "...",
      "phase": [240, 300],
      "statistical_label": "positive",
      "response_id": "...",
      "response_cluster_features": {},
      "support": 0,
      "value_fields": {}
    }
  ],
  "allowed_information": {},
  "provenance": {}
}
```

这里仍是内部 IR，可以包含 action-derived statistics，但不能直接给 Agent。

---

# 6. Stage 02 — Observation-Compatible Semantic Projection

这是本次最重要的修改。

目标：

> 把 replay/action-space 中挖出的状态转换成与 Agent 实际 Observation 尽可能同构的语言空间。

现有 Agent OBS 重点概念包括：

```text
Time
Resources
Income
Supply used / cap / free
Workers current / ideal
Army supply
Completed
Under Construction
Workers En Route
Active Queues
Enemy Intelligence
Map Control
Army Advantage
Income Advantage
Power
Losses
Research & Technology
Threat Flags
```

Readable Skill 的 situation 语言应尽量围绕这些概念组织。

---

# 7. Own State 的 OBS-compatible 描述

Own state 允许描述：

```text
army composition
production posture
technology posture
economy / expansion posture
upgrade posture
air-vs-ground commitment
defensive commitment
```

如果统计证据没有实时：

```text
minerals
supply
army advantage
income advantage
```

则不能凭空写具体值。

正确：

```text
Your completed army and production should roughly resemble a
mid-game ground-oriented setup with established core technology.
```

错误：

```text
You should have 800 minerals and +10 army advantage.
```

Skill 可以提醒模型在 runtime 检查这些 OBS 字段，但不能伪造它们是历史统计条件。

---

# 8. Opponent State 必须改成 Agent OBS 风格

最终 Agent-facing Skill 禁止：

```text
OPP_S02
Opp_Cnt_Cum_Production
enemy action sequence
enemy build command list
```

应该写成：

```text
Enemy Intelligence is mainly consistent with a ground-focused army.
Remembered units are more likely to include Stalkers and Immortals
than Phoenixes or Void Rays, while the opponent also appears to have
meaningful technology investment.
```

要求：

- 使用 `Enemy Intelligence` 这一 runtime 语义；
- 使用真实 SC2 单位名；
- 允许粗粒度兵种组合；
- 不要求精确数量；
- 不声称 omniscient information；
- 使用 `remembered / observed / appears / consistent with / possible` 等不确定措辞。

---

# 9. Unit 描述规则

## 9.1 不要只写抽象类别

避免只写：

```text
ground-heavy
air-heavy
```

最好写：

```text
ground-heavy, with representative Enemy Intelligence cues such as
Stalkers and Immortals, and limited evidence of Phoenix or Void Ray presence
```

这样更容易与 runtime OBS 做语义匹配。

## 9.2 不输出 action list

内部可能看到：

```text
Stalker order
Gateway order
Immortal order
Probe order
Pylon order
```

Projection 后只保留态势相关内容：

```text
representative combat units: Stalker, Immortal
production posture: ground production established
technology posture: advanced ground support technology
```

必须丢弃动作顺序、工人动作、补给动作、完整建筑顺序。

## 9.3 数量默认粗粒度

不要写：

```text
3 Stalkers
2 Immortals
```

使用：

```text
few
several
multiple
dominant
limited
little evidence
```

配置：

```python
ALLOW_EXACT_OBS_COUNTS = False
```

## 9.4 Unit name 来源受控

新建：

```text
common/obs_vocabulary.py
```

从现有 SC2 entity / unit database 建合法单位名表。

LLM 输出的具体 unit / structure / upgrade 名必须可 grounding。

---

# 10. Observation Projection 中间 Schema

每个 state 转成：

```json
{
  "state_id": "...",
  "side": "opponent",
  "phase": "early_midgame",
  "army_domain": "ground",
  "army_style": "ranged_ground_with_advanced_support",
  "representative_unit_cues": [
    {"unit": "Stalker", "strength": "strong"},
    {"unit": "Immortal", "strength": "moderate"}
  ],
  "air_presence": "low",
  "production_posture": "moderate_to_heavy",
  "technology_posture": "established_ground_tech",
  "economy_posture": "normal",
  "expansion_posture": "unknown",
  "defense_posture": "low_or_uncertain",
  "pressure_posture": "possible_midgame_pressure",
  "special_threats": [],
  "confidence": "medium",
  "obs_style_summary_seed": {
    "enemy_intelligence": "...",
    "technology": "...",
    "pressure": "..."
  },
  "source_state_ids": ["..."]
}
```

证据不足字段必须写 `unknown`，不要猜。

---

# 11. Response Cluster → Policy Signature

禁止把 `top_actions` 直接送进最终 Skill。

新增：

```text
response_policy_signature
```

例如：

```json
{
  "economy_direction": "maintain",
  "expansion_direction": "delay",
  "production_direction": "increase",
  "technology_direction": "continue_existing_ground_tech",
  "army_direction": "strengthen_ground_quality",
  "air_direction": "do_not_open_new_air_branch_yet",
  "upgrade_direction": "continue_existing_path",
  "defense_direction": "stabilize_if_pressure_reaches_owned_zones",
  "tempo": "stabilize_then_resume_pressure",
  "confidence": "medium"
}
```

优先 deterministic 生成。

从 response cluster 的 action-family aggregate 提取：

```text
economy delta
production delta
tech delta
army family delta
air/ground delta
expansion delta
defense delta
upgrade delta
```

LLM 不直接从完整 action list 自由总结。

---

# 12. Stage 03 — LLM Annotation

每个 method 独立调用，禁止跨 method 复用 full annotation。

建议 4 Pass。

## Pass A — Opening Annotation

输入：

```text
method-allowed opening evidence
opening semantic aggregate
representative medoid features
```

输出：

```json
{
  "opening_name": "Cyber Core Expand",
  "opening_family": "tech-oriented macro opening",
  "opening_summary": "...",
  "strategic_goal": "...",
  "economy_character": "...",
  "production_character": "...",
  "technology_character": "...",
  "army_character": "...",
  "flexibility_note": "This is a strategic template, not a fixed build order."
}
```

## Pass B — State Annotation

Own / opponent 分开。

Opponent prompt 必须要求：

```text
Describe the state using concepts that could approximately be matched
against the runtime SC2 Agent observation.

Prefer wording such as:
- Enemy Intelligence shows / remembers ...
- mainly ground / mainly air / mixed
- representative units such as ...
- limited evidence of ...
- technology investment appears ...
- production appears light / moderate / heavy
- pressure appears low / possible / high

Do not mention:
- replay actions
- hidden build commands
- oracle state IDs
- exact unseen building counts
```

## Pass C — Transition Annotation

输入：

```text
own semantic state
opponent semantic state
statistical label
policy signature
next semantic state
```

输出：

```json
{
  "title": "...",
  "node_type": "positive",
  "trigger_summary": "...",
  "own_situation": "...",
  "opponent_situation": "...",
  "decision_direction": "...",
  "strategic_reason": "...",
  "avoid_direction": "...",
  "transition_goal": "...",
  "exit_or_recheck_condition": "...",
  "next_state_summary": "..."
}
```

对于 NEGATIVE，重点解释：

```text
什么态势下应避免某种战略方向
```

而不是输出“失败 action list”。

## Pass D — Hierarchy Consolidation

只合并：

```text
相同 sign
相近 trigger
相近 policy direction
相近 phase
```

禁止：

```text
positive + negative 合并
不同 opponent posture 强行合并
不同 method 信息混合
```

每个合并节点保留：

```text
source_state_ids
source_edge_ids
```

---

# 13. LLM Prompt 统一硬约束

所有 annotation prompt 加：

```text
You are compiling reusable strategic knowledge for an SC2
macro decision-making agent.

This is NOT a build-order generation task.

Do not output an ordered action list.
Do not reproduce raw replay actions.
Do not prescribe exact canonical action sequences.

Use natural-language strategic guidance:
- situation
- strategic direction
- trade-off
- adaptation
- risk
- transition goal

Opponent descriptions must be compatible with partial observations.
Use representative unit cues when supported by the data, especially
wording similar to runtime Enemy Intelligence.

Never expose oracle replay state, hidden action sequences, cluster IDs
or unseen exact counts.

The statistical sign is provided by the pipeline.
Do not change it.

Historical association is not causality.
```

---

# 14. Agent-facing Skill 最终目录

```text
SKILL_MINING_V2_READABLE/
│
├── full_signed_graph/
├── ablation_single_trace/
├── ablation_static_population/
├── ablation_flat_adaptive/
├── ablation_positive_only/
└── ablation_frequency_only/
```

内部：

```text
<method>/
└── protoss/
    └── PvP/
        └── PvP_O01/
            ├── SKILL.md
            ├── index.json
            ├── nodes/
            │   ├── N001.md
            │   ├── N002.md
            │   └── ...
            └── provenance/
                ├── method_ir.json
                ├── observation_projection.json
                ├── semantic_annotation.json
                ├── source_mapping.json
                └── validation_report.json
```

Agent 只能访问：

```text
SKILL.md
index.json
nodes/*.md
```

runtime 禁止读取 `provenance/`。

---

# 15. 第一层 `SKILL.md` 强制格式

**一个 `SKILL.md` 代表一个具体 Opening Strategy。**

模板：

```markdown
# Cyber Core Expand

## Skill Identity

- Skill ID: PvP_O01
- Matchup: Protoss vs Protoss
- Opening Family: Tech-oriented macro opening
- Method: Full Signed Graph

## Opening Strategy

This opening establishes early Cybernetics Core technology while keeping
enough Gateway-based production to remain flexible.

The historical population pattern is characterized by early technology
investment, sustained basic production, and a transition toward a stronger
mid-game army rather than a rigid all-in.

This is a strategic template, not a fixed build order.
Exact macro actions must be chosen from the current observation.

## Strategic Priorities

- Maintain the identity of the opening instead of blindly reproducing a sequence.
- Use current Completed / Under Construction / Active Queues to avoid duplicate work.
- Match adaptation decisions against current Enemy Intelligence.
- Re-evaluate economy, army and technology trade-offs at every decision.

## Decision Nodes

### [POSITIVE] N001 — Stabilize against ground pressure

**Trigger situation:**
Enemy Intelligence is dominated by ground combat units, with representative
cues such as Stalkers and Immortals, while there is little evidence of a major
air transition.

**Direction:**
Strengthen the existing ground army and production path before taking
additional economic risk.

**Read for details:** `N001`

---

### [NEGATIVE] N002 — Avoid greedy expansion under unresolved pressure

**Trigger situation:**
The opponent appears to maintain meaningful ground pressure while our current
posture has not yet converted technology investment into enough army strength.

**Risk direction:**
Do not add another greedy economic or unrelated technology branch before
stabilizing the army.

**Read for details:** `N002`

---

### [DEFAULT] N003 — Normal mid-game continuation

**Trigger situation:**
No strong opponent-specific signal dominates the current Enemy Intelligence.

**Direction:**
Continue developing the opening along its normal balanced technology,
production and economy path.

**Read for details:** `N003`
```

第一层必须先介绍 Opening Strategy，再列节点摘要。

---

# 16. 第一层节点摘要要求

每个 child summary 必须包含：

```text
node type
node title
trigger situation
one-sentence direction
node id
```

目标：让模型只看 Root 就能判断当前是否值得继续读取该节点。

摘要建议控制在：

```text
40–100 English words
```

不能把完整节点内容塞进 Root。

---

# 17. Signed / Ablation Badge 规则

统一 Badge：

```text
[POSITIVE]
[NEGATIVE]
[DEFAULT]
[COMMON]
[FREQUENT]
[TRACE]
```

| Method | 允许 Badge |
|---|---|
| Full Signed Graph | POSITIVE / NEGATIVE / DEFAULT |
| Single Trace | TRACE |
| Static Population | COMMON / DEFAULT |
| Flat Adaptive | POSITIVE / NEGATIVE / DEFAULT |
| Positive Only | POSITIVE / DEFAULT |
| Frequency Only | FREQUENT / COMMON |

任何 ablation 不得显示理论上已经移除的信息。

---

# 18. 下级 Node Markdown 强制格式

```markdown
# N001 — Stabilize against ground pressure

## Node Type

POSITIVE

## Summary

Use this branch when Enemy Intelligence suggests a sustained ground-oriented
opponent and immediate army strength matters more than additional economic greed.

## When This Applies

### Opponent cues

- Enemy Intelligence is mainly ground-oriented.
- Representative remembered units may include Stalkers and Immortals.
- There is limited evidence that Phoenixes or Void Rays are the main current commitment.
- Technology investment appears meaningful enough to support stronger ground units.

### Own cues

- The opening's core technology is already established or being established.
- Current production is capable of supporting the existing ground path.
- The live observation should be checked for army supply, free supply, active queues,
  and current resource bank before selecting exact actions.

These cues are approximate. They do not all need to be true.

## Recommended Strategic Direction

Prioritize converting the existing technology and production base into
usable ground combat power.

Continue the current strategic branch rather than opening an unrelated
technology path.

Economic growth can continue when affordable, but it should not prevent
near-term army stabilization.

## What This Does NOT Mean

This node is not an instruction to reproduce a historical action sequence.

Do not build units or structures only because they appeared in replay data.
Choose exact canonical actions from the current live observation.

## Transition Goal

Reach a posture where the ground threat no longer forces emergency military
investment and the opening can return to normal economy / technology development.

## Possible Next Situations

### N004 — Opponent shifts toward air

**Situation:** Enemy Intelligence begins to show a meaningful air transition.

**Direction:** Re-evaluate the ground-only continuation and prepare an
appropriate anti-air composition direction.

**Read:** `N004`
```

---

# 19. NEGATIVE Node 写法

NEGATIVE node 不是“失败动作列表”。

应该表达：

```text
在什么可观察态势下，某种战略方向在匹配历史条件中与更差结果相关，
因此当前应避免或谨慎继续该方向。
```

模板建议：

```markdown
## Risk Direction

Historical matched contexts associate this direction with worse outcomes.

Avoid committing additional resources to ... when ...

## Safer Re-evaluation

Before continuing this direction, re-check the live observation, especially:
- Enemy Intelligence
- current army posture
- active production / queues
- resource bank
- available technology
```

OBS 字段如果不是历史统计条件，只能作为 runtime re-check guidance，不能写成历史因果解释。

---

# 20. Next Situation 规则

只有 method 支持 graph 时允许 `Possible Next Situations`：

```text
full_signed_graph
ablation_positive_only
ablation_frequency_only
```

其中 frequency-only 的 next node 只能表示：

```text
frequent continuation
```

不能表示“更优”。

`flat_adaptive` 禁止 next-node link。

`single_trace` 如需表示后继，只能写：

```text
Next Trace Phase
```

不能宣称 adaptive graph。

---

# 21. `index.json`

```json
{
  "skill_id": "PvP_O01",
  "opening_name": "Cyber Core Expand",
  "method": "full_signed_graph",
  "root": "SKILL.md",
  "nodes": {
    "N001": {
      "path": "nodes/N001.md",
      "type": "positive",
      "title": "Stabilize against ground pressure",
      "summary": "...",
      "trigger_summary": "...",
      "children": ["N004"]
    }
  }
}
```

Runtime 只能通过 `index.json` 验证后的 node id 读取文件，禁止任意路径读取和 path traversal。

---

# 22. Stage 05 — Readable Skill Validation

## 22.1 Action-list Leakage

Agent-facing Markdown 禁止内部字段：

```text
canonical_actions
response_id
edge_id
own_state_id
opponent_state_id
OPP_S
OWN_S
```

这些只能存在 provenance。

## 22.2 Oracle Leakage

禁止：

```text
the opponent built exactly ...
the opponent ordered ...
the hidden opponent state is ...
```

要求 opponent 语言使用：

```text
Enemy Intelligence
observed
remembered
appears
consistent with
possible
limited evidence
```

## 22.3 Exact Count Leakage

默认禁止 replay-derived exact enemy unit count。

## 22.4 Unit Grounding

所有具体 unit / structure / upgrade 名必须能映射到 SC2 entity index。

## 22.5 Navigation Integrity

检查：

```text
Root 所有 Read node 存在
所有 child id 存在
不能引用其他 method
禁止 path traversal
```

## 22.6 Ablation Leakage

### Single Trace

禁止：

```text
population
positive
negative
preferred
harmful
```

### Static Population

禁止：

```text
enemy-conditioned trigger
positive
negative
```

### Flat Adaptive

禁止：

```text
next node
graph successor
multi-hop transition
```

### Positive Only

禁止：

```text
negative
harmful
worse-outcome path
```

### Frequency Only

禁止：

```text
positive
preferred
better outcome
adjusted lift
win enrichment
```

任何 leakage 必须使 pipeline fail，不要只 warning。

---

# 23. 新 Agent 工作目录

创建：

```text
/data2/shy_2608/SC2trace2nl/SC2-Agent-human-skill/
```

新增：

```text
SC2_Agent/
│
├── human_skill_common/
│   ├── __init__.py
│   ├── schema.py
│   ├── skill_loader.py
│   ├── skill_memory.py
│   ├── navigator.py
│   ├── protocol.py
│   ├── prompt_common.py
│   ├── trace_recorder.py
│   └── validation.py
│
├── human_skill_full/
│   ├── __init__.py
│   ├── agent.py
│   ├── prompt.py
│   └── config.py
│
├── human_skill_single_trace/
├── human_skill_static_population/
├── human_skill_flat_adaptive/
├── human_skill_positive_only/
└── human_skill_frequency_only/
```

每个 package 独立定义：

```python
AGENT_VERSION
SKILL_METHOD
ALLOWED_NODE_TYPES
ALLOW_GRAPH_NAVIGATION
```

例如：

```python
AGENT_VERSION = "human-skill-full-v1"
SKILL_METHOD = "full_signed_graph"
ALLOWED_NODE_TYPES = {"positive", "negative", "default"}
ALLOW_GRAPH_NAVIGATION = True
```

---

# 24. 六个独立 Agent package 的要求

不要只做一个：

```python
agent(mode="xxx")
```

然后所有实验共享同一个 prompt 文件。

为了实验可审计，每个 ablation 应有：

```text
独立 agent.py
独立 prompt.py
独立 config.py
明确 pinned skill root
明确 AGENT_VERSION
```

可以共享底层：

```text
skill_loader
memory
JSON protocol
canonical validation
logging
```

但从日志必须直接看出当前运行的是哪一个 ablation Agent。

---

# 25. 新 Bot 入口

不要修改原：

```text
dummies/generic/universal_llm_bot.py
```

复制得到：

```text
dummies/generic/universal_llm_human_skill_bot.py
```

新 Bot 保留：

```text
decision trigger
observation capture
scheduler
queue replacement
canonical validation
recording
```

替换 strategy summary loading / naive single call 为：

```text
hierarchical readable skill loading
multi-round skill reading decision
```

---

# 26. Skill 选择

第一版不要自动检索 opening。

新增：

```text
--force-human-skill PvP_O01
```

根据 Agent variant 自动绑定 method：

```text
SKILL_MINING_V2_READABLE/<method>/<race>/<matchup>/<opening_id>/SKILL.md
```

先隔离评估 Skill quality，不混入 Skill retrieval quality。

---

# 27. Skill Root Context 规则

每一次 macro decision 都必须包含完整：

```text
SKILL.md
```

Root 默认始终可见，不计入 read memory。

---

# 28. Skill Read Memory

实现：

```python
@dataclass
class MatchSkillMemory:
    skill_id: str
    method: str
    visited_node_ids: list[str]
    visited_node_contents: dict[str, str]
```

规则：

1. 每场比赛初始化为空；
2. 第一次 `READ_SKILL(N001)`：读取文件并写入 memory；
3. 同一节点再次请求：从 memory 返回；
4. 下一次 macro decision：所有已读节点完整内容重新加入 context；
5. 比赛结束：memory 写日志；
6. 新比赛：memory 清空。

---

# 29. 不保存普通长对话历史

下一轮只保留：

```text
fresh current observation
root skill
previously read skill nodes
unfinished queue
```

不保留：

```text
previous private reasoning
previous full prompt
all prior model messages
```

context 增长只来自显式读过的 Skill knowledge。

---

# 30. Multi-round JSON 协议

不依赖 provider native tools。

模型每轮只允许两类输出。

## 30.1 READ_SKILL

```json
{
  "type": "read_skill",
  "node_id": "N001"
}
```

Harness：

```text
validate node id
→ load node
→ append MatchSkillMemory
→ 同一次 decision 继续下一轮 LLM call
```

## 30.2 FINAL_DECISION

```json
{
  "type": "decision",
  "reason": "Enemy Intelligence remains ground-oriented, so I will strengthen the current ground path before taking more economic risk.",
  "ordered_names": ["Pylon", "Gateway", "Stalker", "Immortal"]
}
```

之后继续原：

```text
canonical validation
mapping
ExecutionScheduler.replace_uncommitted_queue()
```

---

# 31. Multi-round 最大轮数

配置：

```python
MAX_SKILL_READS_PER_DECISION = 3
MAX_AGENT_ROUNDS_PER_DECISION = 4
```

例：

```text
round 1: READ N001
round 2: READ N004
round 3: FINAL
```

达到上限仍未 final：追加一次强制 final prompt。

若仍失败：保持旧 uncommitted queue，与原 invalid-response 语义一致。

---

# 32. 决策 Prompt 结构

```text
[1. Agent Role]
[2. Decision Lifecycle]
[3. Queue / Commitment Semantics]
[4. Race Mechanics]
[5. Economy / Supply / Production Principles]
[6. Observation Field Guide]

[7. Opening Skill]
<完整 SKILL.md>

[8. Previously Read Skill Nodes]
<N001 full content>
<N004 full content>

[9. Current Observation]
<obs_text>

[10. Carry-over Uncommitted Tasks]
[...]

[11. Available Skill Read Protocol]

[12. Allowed Canonical Outputs]

[13. Response Contract]
```

Prompt 明确：

```text
Skill is guidance, not an executable build order.
Current Observation has priority over historical Skill prose
when selecting exact macro actions.
```

---

# 33. Agent 使用 Skill 的统一原则

Prompt 加入：

```text
1. First inspect the live observation.
2. Read the root opening strategy and available node summaries.
3. If one node appears decision-relevant but the summary is insufficient,
   request its full content.
4. You may read more than one node if necessary.
5. Previously read nodes are reusable knowledge, not commands that must be followed.
6. Produce exact macro actions only after reconciling Skill guidance with:
   - Resources
   - Supply
   - Completed
   - Under Construction
   - Active Queues
   - Enemy Intelligence
   - Army / Income Advantage
   - Threat Flags
7. Never copy a historical sequence from the Skill.
```

---

# 34. Variant Prompt 差异

## Full

```text
This Skill may contain positive, negative and default adaptive nodes
connected by hierarchical transition guidance.
```

## Single Trace

```text
This Skill was distilled from one representative human trajectory.
It does not contain population-level value judgments or opponent-adaptive
comparative evidence.
```

## Static Population

```text
This Skill describes common population-level strategic continuation.
It does not contain opponent-conditioned adaptive rules.
```

## Flat Adaptive

```text
This Skill contains adaptive positive/negative decision nodes,
but no graph-based next-state guidance.
```

## Positive Only

```text
This Skill contains positive/default graph guidance only.
Negative-path information has been withheld.
```

## Frequency Only

```text
This Skill contains frequent historical transitions.
Frequency does not imply that a direction is better.
```

---

# 35. Strategy Automation 处理

不要给每个 mined opening 人工写不同 tactical automation。

否则会引入额外实验变量。

新 Human Skill Agent 使用：

```text
race-generic automation profile
```

三族各一套，所有 full / ablation Agent 共用。

负责：

```text
attack/defense movement
rally
scouting
race utility
micro
```

不要依据具体 opening 人工调整 attack threshold 等行为。

如当前系统无法完全移除 strategy-specific profile，则至少建立统一 race-generic profile，并在 manifest 中记录。

---

# 36. Agent 日志

新增 schema version，例如：

```text
schema_version: 5
```

每次 decision 记录：

```json
{
  "agent_version": "human-skill-full-v1",
  "skill_method": "full_signed_graph",
  "skill_id": "PvP_O01",
  "cycle": 5,
  "game_time": 300,
  "skill_memory_before": ["N001"],
  "skill_reads_this_cycle": ["N004"],
  "skill_memory_after": ["N001", "N004"],
  "agent_rounds": [
    {"round": 1, "type": "read_skill", "node_id": "N004"},
    {"round": 2, "type": "decision"}
  ],
  "observation_at_this_moment": "...",
  "decision": {
    "reason": "...",
    "ordered_names": []
  }
}
```

每场额外输出：

```text
*.skill_reads.json
```

记录：

```text
which nodes were read
first-read game time
reuse count
node type
decision cycles using node
```

---

# 37. CLI

新增：

```bash
python run_vs_ai_human_skill.py \
  --human-skill-agent human-skill-full \
  --force-human-skill PvP_O01 \
  --decision-model DeepSeek-V4-flash \
  --decision-interval 60 \
  --enemy-race protoss
```

Ablation：

```text
--human-skill-agent human-skill-single-trace
--human-skill-agent human-skill-static-population
--human-skill-agent human-skill-flat-adaptive
--human-skill-agent human-skill-positive-only
--human-skill-agent human-skill-frequency-only
```

CLI 必须校验：

```text
agent variant ↔ skill method
```

禁止某个 ablation Agent 读取 full skill root。

---

# 38. Static Probe

新增：

```text
tools/probe_human_skill_agent.py
```

不启动 SC2。

输入：

```text
skill_id
method
fake obs
```

验证：

```text
root load
node summary
READ_SKILL
memory
FINAL_DECISION
canonical output parsing
```

至少准备：

```text
ground pressure
air transition
greedy opponent
low supply
high mineral bank
missing prerequisite
```

---

# 39. Ablation Matrix Probe

新增：

```text
tools/probe_human_skill_ablation_matrix.py
```

对同一个：

```text
opening
fake observation
model
```

依次运行六个 Agent，记录：

```text
root seen
node read
whether negative info existed
whether graph navigation existed
final queue
token usage
LLM calls
```

用于检查 ablation 是否真正隔离。

---

# 40. Pipeline Tests

新增：

```text
analysis/readable_skill_v1/tests/
```

至少：

```text
test_no_action_list_in_agent_skill.py
test_no_oracle_ids.py
test_node_navigation_integrity.py
test_ablation_information_boundary.py
test_unit_grounding.py
test_signed_label_preservation.py
test_frequency_not_called_positive.py
test_positive_only_has_no_negative.py
test_flat_has_no_next_node.py
test_single_trace_has_no_population_value.py
```

---

# 41. Agent Tests

新增：

```text
tools/tests/test_human_skill_loader.py
tools/tests/test_human_skill_memory.py
tools/tests/test_human_skill_protocol.py
tools/tests/test_human_skill_agent_variants.py
tools/tests/test_human_skill_queue_boundary.py
```

重点检查：

```text
原 scheduler 行为未变化
read_skill 不会执行 SC2 action
只有 final decision 才能 replace queue
已读 node 跨 decision 保留
已读 node 不跨 match 保留
invalid node id 被拒绝
path traversal 被拒绝
```

---

# 42. 完整执行顺序

## Phase 0 — Freeze Baseline

完成：

```text
记录 SC2_TRACE2NL commit
记录 SC2-Agent-knowlegde commit
建立新 Agent workspace
生成 manifest
```

验收：旧目录 `git status` clean，旧代码无修改。

## Phase 1 — Readable Skill Pipeline Skeleton

创建：

```text
analysis/readable_skill_v1/
analysis/outputs_readable_skill_v1/
SKILL_MINING_V2_READABLE/
```

暂不调用 LLM。

## Phase 2 — Method Evidence IR

实现六种 method 的严格裁剪。

验收：每种 method 至少对一个 opening 输出 IR，ablation leakage test 通过。

## Phase 3 — Observation Projection

实现：

```text
own state projection
opponent state projection
representative unit cue projection
response policy signature
```

抽样检查：

```text
不出现 action sequence
出现合理具体兵种
语言能与 Enemy Intelligence / Completed / Technology 等 OBS 概念对应
```

## Phase 4 — LLM Annotation Pilot

先只跑：

```text
1 个 PvP
1 个 TvZ
1 个 ZvT
```

人工检查后再全量。

## Phase 5 — Hierarchical Markdown Compile

生成：

```text
SKILL.md
index.json
nodes/
provenance/
```

重点检查 Root：

```text
opening strategy 清晰
child trigger 清晰
positive / negative 明显
summary 足以判断要不要读详情
```

## Phase 6 — Full Six-method Compile

六种 method 全部独立运行 annotation + compile。

禁止复用 full annotation。

## Phase 7 — Validation

全部运行：

```text
leakage
grounding
navigation
ablation boundary
```

任何关键 leakage 直接 fail。

## Phase 8 — 新 Agent Runtime

在 `SC2-Agent-human-skill` 实现：

```text
loader
navigator
memory
protocol
trace
```

先完成 full Agent。

## Phase 9 — 六个 Agent Version

建立六个独立 package，并验证 package → pinned method。

## Phase 10 — Static Probe

不启动 SC2，至少每个 Agent × 3 scenario。

## Phase 11 — SC2 Smoke Test

每个 Agent 至少跑 1 场，检查：

```text
没有读取 provenance
没有 path error
Skill memory 正常
scheduler 正常
```

## Phase 12 — Same-condition Ablation Sweep

同一：

```text
race
enemy race
opening
enemy difficulty
model
decision interval
map
```

分别跑：

```text
naive
full
5 ablations
```

---

# 43. 最终必须产出的文件

## Mining side

```text
analysis/readable_skill_v1/
analysis/outputs_readable_skill_v1/
SKILL_MINING_V2_READABLE/
READABLE_SKILL_BASELINE_MANIFEST.json
```

## Agent side

```text
SC2-Agent-human-skill/
│
├── SC2_Agent/human_skill_common/
├── SC2_Agent/human_skill_full/
├── SC2_Agent/human_skill_single_trace/
├── SC2_Agent/human_skill_static_population/
├── SC2_Agent/human_skill_flat_adaptive/
├── SC2_Agent/human_skill_positive_only/
├── SC2_Agent/human_skill_frequency_only/
├── dummies/generic/universal_llm_human_skill_bot.py
├── run_vs_ai_human_skill.py
└── tools/
```

---

# 44. 最终验收标准

## Skill

- [ ] 每个 Skill 对应一个明确 Opening Strategy。
- [ ] Root 第一层先介绍开局策略。
- [ ] Root 包含所有下级节点摘要。
- [ ] 每个节点摘要包含 trigger + simple direction。
- [ ] 有 signed evidence 的方法明确显示 POSITIVE / NEGATIVE。
- [ ] 无 sign 信息的 ablation 不伪造 positive / negative。
- [ ] Agent-facing Skill 无 action list。
- [ ] Agent-facing Skill 无 enemy action list。
- [ ] Opponent situation 尽可能使用 Agent OBS 风格。
- [ ] Opponent 描述尽量包含代表性真实 SC2 单位名，而非只有抽象类别。
- [ ] 不使用精准隐藏单位数量。
- [ ] 不出现 oracle state ID / cluster ID。
- [ ] 每个 node 可追溯到 provenance。

## Ablation

- [ ] 六种方法都先生成独立 Evidence IR。
- [ ] 六种方法都经过独立 LLM annotation。
- [ ] 不共享 full annotation。
- [ ] 最终目录结构同构。
- [ ] 信息边界 validator 全部通过。

## Agent

- [ ] 原 naive Agent 未修改。
- [ ] 新 Agent 是独立 workspace。
- [ ] 六个 Skill method 各自有独立 Agent package/version。
- [ ] Root 每轮都在 context。
- [ ] 已读完整 node 跨 decision 保留。
- [ ] 普通历史 CoT 不跨 decision 保留。
- [ ] 模型可多轮 READ_SKILL。
- [ ] 只有 FINAL_DECISION 可以触发 queue replacement。
- [ ] 原 canonical validation / scheduler 行为保持不变。
- [ ] 日志能完整恢复 Skill read trajectory。

---

# 45. 最终系统结构

```text
Human Replay
    ↓
────────────────────────────────────────
Existing Skill Mining V2
────────────────────────────────────────
Opening Discovery
Own / Opponent State Mining
Response Mining
Transition Value
Signed Strategy Graph
    ↓
────────────────────────────────────────
New Readable Skill Compiler
────────────────────────────────────────
Method-specific Evidence IR
    ↓
Observation-Compatible Projection
    │
    ├── own posture
    ├── Enemy-Intelligence-like opponent posture
    ├── representative unit cues
    └── response policy signature
    ↓
Method-specific LLM Annotation
    ↓
Hierarchy Consolidation
    ↓
Readable Markdown Skill
    │
    ├── Opening Strategy
    ├── node summaries
    ├── signed / ablation node badges
    └── nodes/*.md
    ↓
────────────────────────────────────────
Human Skill Agent
────────────────────────────────────────
Current OBS
+
Opening SKILL.md
+
Previously Read Full Nodes
+
Unfinished Queue
    ↓
LLM
    ├── READ_SKILL
    ├── READ_SKILL
    └── FINAL_DECISION
             ↓
       ordered_names
             ↓
Canonical Validation
             ↓
Original ExecutionScheduler
             ↓
SC2
```

---

# 46. 最重要的实现原则

整个实现始终围绕：

> **Human trajectory statistics determine what strategic situations and transitions are worth preserving; the LLM turns those statistics into observation-compatible strategic knowledge; the runtime Agent uses that knowledge as guidance, but must still infer the current situation and choose concrete actions from the live SC2 observation.**

不要把系统做成：

```text
trajectory
→ action template
→ exact state matcher
→ replay action executor
```

应该是：

```text
trajectory population
→ strategic evidence
→ readable hierarchical skill
→ LLM observation-conditioned reasoning
→ concrete macro decision
```
