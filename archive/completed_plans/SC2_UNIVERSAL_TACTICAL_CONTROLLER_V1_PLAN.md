# SC2 Agent V1 — Universal Tactical Controller
## 通用战术 / 微操托管层改造补充方案

> **归档状态：已完成（2026-08-10）**
> 本文档保留为设计与验收依据，不再作为待执行计划。实现已进入
> outer repo 当前通过 `SC2-Agent-human-skill/` submodule 固定 Agent，实现分支为
> `codex/human-skill-agent`；最终根因修复与文档同步已进入 `83654f8`。

### 最终实现映射

- 通用控制器落在 `SC2_Agent/universal_tactics/`，包含 snapshot、composition、
  readiness、posture、adaptive attack、race utilities、trace 与 validation；
- `UniversalLLMBot` 和 Human-Skill Bot 已统一接入 Universal Tactics V1；
- `DEFEND > GATHER > ATTACK` 优先级、readiness gate、cohesion、侦测、空地军
  兼容、timing/max-supply gate、hysteresis/cooldown 均已实现；
- 旧 `strategy_tools.py` 已建立 `TACTICAL_MIGRATION_MANIFEST.json`，保留为迁移
  基线，不再进入 Human-Skill live tactical path；
- 冻结配置为 `UNIVERSAL_TACTICS_V1_CONFIG.json`，策略清单记录于
  `docs/tactical_strategy_tools_inventory.md`；
- 当前代码相关自动化测试已包含在 `tools/tests/test_universal_tactical_controller.py`
  与 `tools/tests/test_universal_tactical_integration.py`；合并后的相关测试集为
  224 passed（排除仓库既有、无关的 dataset checksum 用例）。

### 归档说明

SC2 observation stall 已收敛为 Human-Skill bot 名称触发真人实时模式的子串误判，
修复后 Qwen3-32B 1200 秒压力测试为 15/15 首轮干净完成。现行启动约束见 Agent
仓库 `docs/SC2_BATCH_EXPERIMENT_POLICY.md`，事故摘要见
`docs/SC2_OBSERVATION_NOT_RETURNING_ROOT_CAUSE_AND_FIX.md`。

> 本文档是一个**独立补充任务书**。
> 只处理当前 SC2 Agent 中“每个策略需要独立 `strategy_tools.py` 托管微操/攻击逻辑”的问题。
> **不包含 Skill 挖掘、Skill 语言化、分层 Markdown、Skill Node、Skill Read Memory 等内容。**

---

# 1. 改造目标

当前 Agent 中，每个策略目录通常存在：

```text
SKILL/<race>/<strategy>/strategy_tools.py
```

这些文件负责托管：

- 通用防守；
- 部队集结；
- 攻击触发；
- 工人/侦察等种族自动化；
- 少量策略特有的战术逻辑；
- 固定的 `attack_threshold`；
- 有时还存在特定兵种/科技的攻击 gate。

这种设计在使用大量自动挖掘出的新 Opening / Skill 时不可扩展，因为：

```text
新增一个 Skill
→ 还需要人工写一个 strategy_tools.py
```

会使：

- Skill 和 tactical micro 强耦合；
- 每个 Skill 带入不同人工先验；
- Full / Ablation 实验无法保证战术层一致；
- 攻击阈值本身成为隐藏实验变量；
- 新挖掘 Skill 无法直接运行。

本次 V1 改造的目标是：

> **所有种族、所有 Skill、所有 Ablation，共享同一套 Universal Tactical Controller。**

最终不再需要：

```text
SKILL/<race>/<strategy>/strategy_tools.py
```

来决定：

```text
什么时候守
什么时候集结
什么时候攻击
什么时候撤退
```

而是由实时游戏状态统一决定。

---

# 2. V1 的核心设计原则

V1 不重新实现单位级微操。

已有 Sharpy 已经具备：

```text
Marine / Marauder → MicroBio
SiegeTank         → MicroTanks
Battlecruiser     → MicroBattleCruisers
Stalker           → MicroStalkers
Lurker            → MicroLurkers
...
未知单位           → GenericMicro
```

因此 V1 只新增：

```text
Universal Tactical Controller
```

它负责：

```text
DEFEND
GATHER
ATTACK
RETREAT
```

真正进入战斗以后，继续使用：

```text
GroupCombatManager
→ MicroRules
→ existing per-unit micro
```

---

# 3. 最终职责划分

改造后必须形成如下边界：

```text
Macro Decision Layer
        │
        │  决定生产 / 科技 / 扩张
        ▼
ExecutionScheduler


Live Battle State
        │
        ▼
Universal Tactical Controller
        │
        ├── DEFEND
        ├── GATHER
        ├── ATTACK
        └── RETREAT
        │
        ▼
GroupCombatManager
        │
        ▼
Existing MicroRules
        │
        ├── Tank micro
        ├── Marine micro
        ├── Stalker micro
        ├── Lurker micro
        ├── BC micro
        └── Generic micro
```

必须保证：

```text
Skill / Opening ID
```

不参与 Tactical Controller 的行为判断。

---

# 4. 非协商约束

## 4.1 不允许按 Skill 分支

禁止：

```python
if skill_id == "PvP_O01":
    ...

if strategy_name == "lurkers":
    ...

if opening == "marine_rush":
    ...
```

Universal Tactical Controller 只能读取：

```text
live SC2 state
race
own army
enemy army
zone state
combat power
army advantage
income advantage
supply
local threat
```

---

## 4.2 不允许保留 Skill-specific Attack Threshold

必须逐步移除：

```text
attack_threshold = 3
attack_threshold = 10
attack_threshold = 24
attack_threshold = 32
attack_threshold = 50
attack_threshold = 60
...
```

V1 不允许：

```text
不同 Skill 使用不同 attack threshold
```

---

## 4.3 不重新实现已有 Unit Micro

不要重新写：

```text
Tank siege logic
Stalker blink logic
Marine kite
BC yamato / retreat jump
Lurker burrow
Viking combat
```

除非现有 Sharpy 明确不支持某单位。

默认：

```text
reuse existing MicroRules
```

---

## 4.4 Full 与所有 Ablation 必须使用同一个 V1

实验时：

```text
Full
Single Trace
Static Population
Flat Adaptive
Positive Only
Frequency Only
```

必须全部使用：

```text
Universal Tactical Controller V1
```

不能为不同方法调整 threshold。

---

# 5. 新代码目录

在新的 Human Skill Agent workspace 中新增：

```text
SC2_Agent/
└── universal_tactics/
    ├── __init__.py
    ├── controller.py
    ├── battle_snapshot.py
    ├── composition.py
    ├── readiness.py
    ├── posture.py
    ├── race_utilities.py
    ├── adaptive_zone_attack.py
    ├── universal_plan.py
    ├── config.py
    ├── logging.py
    └── validation.py
```

V1 不需要：

```text
policies/positional_push.py
policies/harass.py
...
```

这些属于未来 V2。

---

# 6. BattleSnapshot

新增统一的实时战术输入对象：

```python
@dataclass
class BattleSnapshot:
    game_time: float

    own_total_power: float
    enemy_known_power: float
    enemy_predicted_power: float

    own_ground_power: float
    own_air_power: float
    own_ground_presence: float
    own_air_presence: float

    enemy_ground_power: float
    enemy_air_power: float
    enemy_ground_presence: float
    enemy_air_presence: float

    own_melee_power: float
    own_siege_power: float
    own_detector_count: int
    own_stealth_power: float

    enemy_melee_power: float
    enemy_siege_power: float
    enemy_detector_count: int
    enemy_stealth_power: float

    army_advantage: str
    predicted_army_advantage: str
    income_advantage: str

    supply_used: float
    supply_cap: float

    army_supply: float

    threatened_zone_count: int
    max_local_enemy_power: float
    max_local_own_defender_power: float

    largest_army_group_power: float
    largest_army_group_fraction: float

    enemy_static_defense_target_power: float

    proxy_detected: bool
```

第一版不需要全部字段一次实现。

必须最少有：

```text
own_total_power
enemy_predicted_power
predicted_army_advantage
income_advantage
supply_used
largest_army_group_fraction
zone threat
```

---

# 7. BattleSnapshot 的数据来源

优先复用已有 Sharpy manager。

## GameAnalyzer

使用：

```text
our_power
enemy_power
enemy_predict_power
our_army_advantage
our_army_predict
our_income_advantage
enemy_air
```

不要重新计算另一套优势状态。

---

## ExtendedPower

复用：

```text
power
air_presence
ground_presence
air_power
ground_power
melee_power
surround_power
detectors
stealth_power
```

---

## Zone Manager

用于：

```text
当前己方哪些 zone 被攻击
目标 zone 静态防御
enemy owned zones
gather point
proxy building
```

---

## Roles / GroupCombatManager

用于：

```text
attacking units
defending units
free combat units
army group cohesion
```

---

# 8. 注意：Siege Power 不要直接依赖现有累计值

现有 `ExtendedPower` 的 siege 字段实现需要人工检查。

V1 如果只用于：

```text
attack / defend / gather
```

可以先不强依赖 siege fraction。

如果必须计算：

```text
own_siege_power
enemy_siege_power
```

则在 `composition.py` 中重新遍历单位累加，不直接使用可能存在覆盖行为的旧字段。

---

# 9. CompositionProfile

V1 只做基础兵力适配，不做复杂战术路由。

新增：

```python
@dataclass
class CompositionProfile:
    total_power: float

    ground_fraction: float
    air_fraction: float

    anti_ground_coverage: float
    anti_air_coverage: float

    melee_fraction: float
    siege_fraction: float

    detector_present: bool
    stealth_present: bool

    average_speed: float | None
    average_range: float | None
```

目的不是选择复杂 tactical style。

V1 只用它检查：

```text
当前军队是否具备基本交战能力
```

例如：

```text
敌方 air-heavy
但我方 anti-air coverage 极低
```

则不应仅凭 total power 发起攻击。

---

# 10. TacticalPosture

统一状态：

```python
class TacticalPosture(Enum):
    DEFEND = "defend"
    GATHER = "gather"
    ATTACK = "attack"
    RETREAT = "retreat"
```

V1 不增加：

```text
HARASS
POSITIONAL_PUSH
AIR_HARASS
```

保持最简单实验版本。

---

# 11. Controller 总体逻辑

入口：

```python
class UniversalTacticalController:
    def decide_posture(self, snapshot: BattleSnapshot) -> TacticalPosture:
        ...
```

优先级固定：

```text
RETREAT / DEFEND
>
GATHER
>
ATTACK
```

实际执行建议：

```text
1. Emergency defense
2. Active retreat handling
3. Army cohesion
4. Composition safety
5. Attack readiness
6. Otherwise gather
```

---

# 12. DEFEND 条件

只要己方重要 zone 出现明显敌军威胁：

```text
DEFEND
```

不要因为全局 army advantage 很高就忽略基地防御。

建议：

```python
if snapshot.threatened_zone_count > 0:
    return DEFEND
```

具体 zone 的防守继续使用：

```text
PlanZoneDefense
```

现有 PlanZoneDefense 已经会：

```text
计算 assaulting enemy power
按需求分配 defender
必要时拉 worker
威胁解除后释放 defender
```

不要重写。

---

# 13. RETREAT 的处理

V1 不需要在顶层重新实现复杂撤退。

已有：

```text
PlanZoneAttack
```

会在战斗中比较：

```text
own local power
enemy local power
```

并切换：

```text
Retreat
Withdraw
```

因此 V1：

```text
保留原 PlanZoneAttack retreat state machine
```

新 `AdaptiveZoneAttack` 只替换：

```text
什么时候开始 ATTACK
```

不要替换：

```text
攻击过程中什么时候撤退
```

除非后续测试发现明显 bug。

---

# 14. GATHER 条件

如果没有紧急防守，但军队未充分集结：

```text
GATHER
```

核心指标：

```text
largest_army_group_fraction
```

定义：

```text
largest spatial combat group power
/
total available combat power
```

推荐默认：

```python
MIN_COHESION_TO_ATTACK = 0.72
```

不要为不同 Skill 改。

建议初始 sweep：

```text
0.65
0.72
0.78
```

最后选一个统一值。

如果：

```text
largest_army_group_fraction < threshold
```

则：

```text
GATHER
```

使用：

```text
PlanZoneGather
```

或 Terran 对应的：

```text
PlanZoneGatherTerran
```

但这只是 race mechanic 层差异，不是 Skill 差异。

---

# 15. Composition Safety Gate

攻击前必须检查：

```text
能不能打到对方主要兵种
```

不能只比较：

```text
total power
```

---

## 15.1 Enemy Air Coverage

如果：

```text
enemy_air_presence / enemy_total_power
```

较高，但：

```text
own_air_power
```

不足，则：

```text
GATHER
```

推荐第一版条件：

```python
if enemy_air_fraction >= 0.35:
    if own_anti_air_coverage_ratio < 0.8:
        block_attack = True
```

不要把这些阈值写死在每个 strategy。

---

## 15.2 Enemy Ground Coverage

类似：

```text
enemy_ground_presence
```

很高但己方：

```text
anti-ground power
```

明显不足：

```text
不主动 ATTACK
```

---

## 15.3 Detection Gate

如果敌方已知/预测：

```text
stealth_power > threshold
```

且：

```text
own_detector_count == 0
```

则：

```text
不进行主动深度推进
```

V1 可以继续 GATHER / DEFEND。

---

# 16. Attack Readiness

新增：

```python
def should_start_attack(snapshot: BattleSnapshot) -> bool:
    ...
```

不要使用 Skill-specific fixed power。

采用可解释 condition tree。

---

# 17. Attack Rule A — Clear Army Advantage

如果：

```text
predicted_army_advantage
>= ClearAdvantage
```

且：

```text
cohesion pass
composition safety pass
```

则：

```text
ATTACK
```

优势等级需要使用现有 `Advantage` enum，而不是字符串比较。

---

# 18. Attack Rule B — Timing Window

如果：

```text
predicted_army_advantage
>= SmallAdvantage
```

同时：

```text
income_advantage <= Even
```

说明：

```text
现在军力相对更强
但长期经济不占优势
```

这种情况下倾向：

```text
ATTACK
```

这是一个通用 timing-window 逻辑。

不要绑定：

```text
Stim ready
2 Lurkers
6 Tanks
Battlecruiser count
```

---

# 19. Attack Rule C — Near Max Supply

如果：

```text
supply_used >= 190
```

并且：

```text
composition safety pass
```

允许攻击。

目的是避免满人口长期囤兵。

---

# 20. Attack Rule D — Enemy Weak / Exposed

可选第一版规则：

如果：

```text
own_total_power
明显大于 enemy_predicted_power
```

且：

```text
目标 zone static defense 不高
```

也可以攻击。

但不要引入复杂连续打分系统。

如果现有 `GameAnalyzer` advantage 足够覆盖，可以暂时不单独实现。

---

# 21. 默认不攻击

如果：

```text
无明显军事优势
无 timing window
未接近满人口
```

则：

```text
GATHER
```

不要为了“保持进攻性”加入随机攻击。

---

# 22. AdaptiveZoneAttack

新增：

```python
class AdaptiveZoneAttack(PlanZoneAttack):
    ...
```

设计原则：

保留父类：

```text
target selection
proxy target
enemy zone selection
static defense consideration
attacker role management
reinforcement join
local retreat
attack status
```

只覆盖：

```python
_should_attack(...)
```

或者更干净地增加：

```python
_should_start_attack(...)
```

由 Universal Controller 提供 readiness。

---

# 23. 不再使用 start_attack_power 作为主门槛

现有：

```python
PlanZoneAttack(start_attack_power)
```

依赖：

```text
start_attack_power
```

V1 中可以：

```text
保留一个极低 global floor
```

例如：

```python
GLOBAL_MIN_ATTACK_POWER = 6
```

作用只是避免：

```text
1–2 个单位误触发进攻
```

而不是代表策略 timing。

这个值必须：

```text
所有 race
所有 skill
所有 ablation
```

一致，或者最多 race-independent。

---

# 24. Race Utilities

三族仍然存在游戏机制差异。

因此允许：

```text
race_utilities.py
```

内部根据 race 加载机制性工具。

---

## Terran

可以保留：

```text
MineOpenBlockedBase
PlanCancelBuilding
LowerDepots
WorkerScout
CallMule
ScanEnemy
DistributeWorkers
SpeedMining
ManTheBunkers
ContinueBuilding
PlanZoneGatherTerran
```

注意：

```text
MULE / Scan
```

属于种族机制，不是 Skill-specific tactical adaptation。

---

## Protoss

可以保留：

```text
PlanCancelBuilding
WorkerScout
ChronoAnyTech
ChronoBuilding
MorphWarpGates
DistributeWorkers
SpeedMining
PlanZoneGather
```

---

## Zerg

可以保留：

```text
PlanCancelBuilding
OverlordScout
InjectLarva
SpreadCreep
DistributeWorkers
SpeedMining
PlanZoneGather
```

---

# 25. Race Utility 也必须避免 Strategy-specific 参数

例如禁止：

```python
if opening_is_rush:
    spread_creep = False
```

V1 应采用一个统一 race profile。

如果某 race mechanic 在特定情况下确实应该动态启停，应根据：

```text
live state
```

而不是 strategy name。

第一版优先保持：

```text
固定 race-generic behavior
```

---

# 26. Universal Plan

新增：

```python
def create_universal_tactical_plan(race: Race) -> BuildOrder:
    ...
```

整体结构：

```text
Race Utility
↓
PlanZoneDefense
↓
Universal Gather
↓
AdaptiveZoneAttack
↓
PlanFinishEnemy
```

建议内部顺序：

```python
SequentialList([
    common_safety_tools,
    race_specific_utility_tools,
    PlanZoneDefense(),
    UniversalGather(),
    AdaptiveZoneAttack(),
    PlanFinishEnemy(),
])
```

注意 Sharpy `SequentialList` / `Step` 的 blocking 行为，需要测试保证：

```text
PlanZoneDefense
```

不会永久阻塞：

```text
AdaptiveZoneAttack
```

---

# 27. strategy_tools.py 的迁移

第一阶段不要立即删除旧文件。

保留旧：

```text
SKILL/*/*/strategy_tools.py
```

但新 Human Skill Agent 不再调用它们。

新 Bot 从：

```python
_load_strategy_tools()
```

改成：

```python
_load_universal_tactical_tools()
```

逻辑：

```python
return create_universal_tactical_plan(self.my_race)
```

完全不读取：

```text
selected_strategy
skill_id
opening_id
```

---

# 28. Automation Profile 的处理

当前每个 strategy 可能通过：

```text
AUTOMATION_PROFILE
```

向 LLM prompt 暴露：

```text
attack threshold
special behavior
attack gate
```

新 Human Skill Agent V1 中不要再加载：

```text
strategy-specific AUTOMATION_PROFILE
```

改成：

```text
UNIVERSAL_TACTICAL_PROFILE
```

内容只描述：

```text
Combat movement and attack timing are controlled by a shared
state-driven tactical controller.

The tactical controller considers:
- live army advantage
- predicted enemy power
- army cohesion
- air/ground coverage
- local defense requirements
- supply pressure

The macro decision model does not directly choose unit movement
or attack timing.
```

---

# 29. 原有特殊策略行为如何处理

## 29.1 BC 主动 Tactical Jump 进敌主矿

V1：

```text
删除 strategy-specific TacticalJumpIn
```

原因：

```text
它属于特定策略的额外人工优势
```

保留已有 Unit Micro 中：

```text
BC low-health retreat jump
Yamato usage
```

因为这些属于单位级通用行为。

---

## 29.2 Marine Rush Force Field 坡口撤退

V1 有两个选项。

推荐第一版：

```text
暂时不迁移该 strategy-specific 行为
```

直接使用：

```text
default PlanZoneAttack + existing pathing
```

如果 smoke test 发现该问题频繁导致明显异常，再迁移为：

```text
UniversalPathHazardGuard
```

条件必须是：

```text
实时检测关键通路 Force Field
```

不能是：

```text
marine_rush 才启用
```

---

## 29.3 Lurker 2 只后才进攻

删除：

```text
UnitReady(Lurker, 2)
```

由：

```text
army advantage
cohesion
composition safety
```

决定是否攻击。

---

## 29.4 Tank / Raven / Stim gate

全部删除：

```text
Stim 90%
4 Tank
1 Raven
6 Tank after 9:00
...
```

如果这导致某些阵容过早进攻，优先通过：

```text
Universal attack readiness
cohesion
composition safety
```

修正。

不要重新加入 unit-specific strategy gate。

---

# 30. 配置文件

新增：

```python
@dataclass(frozen=True)
class UniversalTacticalConfig:
    min_cohesion_to_attack: float = 0.72
    global_min_attack_power: float = 6.0

    clear_advantage_attack: bool = True
    timing_window_attack: bool = True
    max_supply_attack: bool = True

    max_supply_trigger: float = 190

    enemy_air_fraction_gate: float = 0.35
    min_anti_air_coverage_ratio: float = 0.80

    enemy_ground_fraction_gate: float = 0.50
    min_anti_ground_coverage_ratio: float = 0.80

    block_attack_without_detection: bool = True

    debug_logging: bool = False
```

这些参数属于：

```text
global tactical config
```

不能由 Skill 覆盖。

---

# 31. 不要一开始做复杂 score

V1 不建议：

```python
attack_score =
    0.3 * army_advantage
  + 0.2 * economy
  + 0.2 * supply
  + ...
```

原因：

- 难解释；
- 参数太多；
- 容易重新变成人工 tuning；
- 论文实验不够干净。

优先：

```text
condition tree
```

---

# 32. 推荐最终 Decision Tree

```text
START
  │
  ▼
Own important zone under attack?
  │
  ├── YES → DEFEND
  │
  └── NO
        │
        ▼
Attack already active and retreat state triggered?
        │
        ├── YES → existing PlanZoneAttack retreat
        │
        └── NO
              │
              ▼
Army power below global minimum?
              │
              ├── YES → GATHER
              │
              └── NO
                    │
                    ▼
Army cohesion < 0.72?
                    │
                    ├── YES → GATHER
                    │
                    └── NO
                          │
                          ▼
Composition safety failed?
                          │
                          ├── YES → GATHER
                          │
                          └── NO
                                │
                                ▼
Predicted Army >= Clear Advantage?
                                │
                    ┌───────────┴───────────┐
                   YES                      NO
                    │                        │
                    ▼                        ▼
                  ATTACK          Small Army Advantage
                                  + income not ahead?
                                            │
                                  ┌─────────┴─────────┐
                                 YES                  NO
                                  │                    │
                                  ▼                    ▼
                                ATTACK          Supply >= 190?
                                                       │
                                             ┌─────────┴────────┐
                                            YES                 NO
                                             │                   │
                                             ▼                   ▼
                                           ATTACK              GATHER
```

---

# 33. Hysteresis

必须防止：

```text
ATTACK
GATHER
ATTACK
GATHER
```

每几秒来回切换。

新增：

```text
posture hysteresis
```

建议：

```python
MIN_ATTACK_COMMIT_SECONDS = 15
MIN_GATHER_COMMIT_SECONDS = 8
```

注意：

已有 `PlanZoneAttack` 本身有 attack state。

所以 V1 优先使用其状态机。

Controller 不要每 tick 重新创建：

```text
PlanZoneAttack instance
```

必须持久存在。

---

# 34. Attack Cooldown

撤退之后不要立即重新 Attack。

新增：

```python
REATTACK_COOLDOWN_AFTER_RETREAT = 12
```

第一版统一配置。

如果已有 `PlanZoneAttack` 的：

```text
RETREAT_TIME
```

足够，可以直接复用，不再重复。

---

# 35. Logging

每次 Tactical posture 变化记录：

```json
{
  "game_time": 420.5,
  "from": "gather",
  "to": "attack",

  "reason": "clear_predicted_army_advantage",

  "snapshot": {
    "own_total_power": 43.2,
    "enemy_predicted_power": 29.4,
    "predicted_army_advantage": "ClearAdvantage",
    "income_advantage": "Even",
    "largest_army_group_fraction": 0.81,
    "supply_used": 134
  },

  "skill_id": "PvP_O01",
  "skill_id_used_for_routing": false
}
```

最后一项必须永远：

```json
false
```

---

# 36. Tactical Trace

每场比赛新增：

```text
*.tactical_trace.json
```

包括：

```text
posture timeline
attack start
retreat start
defense activation
cohesion
army advantage
composition safety gate
attack trigger reason
```

后续论文可以统计：

```text
attack timing
number of attacks
retreat rate
average cohesion at attack
attack win/loss exchange
```

---

# 37. Cross-Skill Invariance Test

这是最关键测试。

构造完全相同：

```text
race
own units
enemy units
zone state
game time
supply
army advantage
```

只修改：

```text
skill_id
opening_id
ablation method
```

则：

```text
UniversalTacticalController.decide_posture()
```

必须输出完全相同结果。

新增：

```text
test_tactical_controller_skill_invariance.py
```

---

# 38. Race Invariance 与 Race Mechanic

Tactical readiness 逻辑本身尽量 race-neutral。

例如：

```text
Clear Army Advantage → Attack
```

三个种族一致。

只有：

```text
race utility
gather implementation
worker / special macro utility
```

允许 race-specific。

测试：

```text
相同抽象 BattleSnapshot
```

不同 race 输入：

```text
posture 决策应一致
```

除非明确存在 race mechanic 必需差异。

---

# 39. Unit Composition Tests

至少准备：

## Terran Bio

```text
Marine + Marauder + Medivac
```

验证：

```text
正常 attack / gather
MicroBio 自动生效
```

---

## Terran Tank

```text
Marine + Tank
```

验证：

```text
Universal Controller 不要求 Tank-specific gate
进入攻击后 MicroTanks 自动 siege
```

---

## Terran BC

验证：

```text
不再主动 strategy-specific jump enemy main
已有 BC micro Yamato / retreat jump 正常
```

---

## Protoss Stalker

验证：

```text
不需要 PvP/PvT Skill-specific tactics
MicroStalkers 自动工作
```

---

## Protoss Mixed Ground

```text
Zealot + Stalker + Immortal
```

验证：

```text
Composition safety
group cohesion
```

---

## Zerg Roach/Hydra

验证：

```text
正常 gather / attack
```

---

## Zerg Lurker

验证：

```text
不要求 “2 Lurkers ready”
只依据统一 readiness
已有 Lurker micro 生效
```

---

# 40. Air Coverage Tests

场景：

```text
Enemy: air-heavy
Own: strong total ground power but little anti-air
```

期望：

```text
GATHER
```

不能：

```text
ATTACK because total power is high
```

---

# 41. Detection Test

场景：

```text
Enemy known stealth power
Own detector = 0
```

期望：

```text
block aggressive attack
```

但如果：

```text
own base is being attacked
```

仍然：

```text
DEFEND
```

防守优先。

---

# 42. Economic Timing Test

场景：

```text
Army = SmallAdvantage
Income = ClearDisadvantage
Cohesion = 0.80
Composition safety = pass
```

期望：

```text
ATTACK
```

理由：

```text
timing_window
```

---

# 43. Economic Greed Test

场景：

```text
Army = SmallDisadvantage
Income = ClearAdvantage
```

期望：

```text
GATHER / DEFEND
```

不能为了“进攻积极性”强攻。

---

# 44. Near Max Supply Test

场景：

```text
Supply = 195
Army = Even
Composition safety = pass
Cohesion = high
```

期望：

```text
ATTACK
```

---

# 45. Defense Priority Test

场景：

```text
Army = ClearAdvantage
但自然矿正在被显著攻击
```

期望：

```text
DEFEND
```

不是：

```text
ATTACK
```

---

# 46. Regression Tests

必须确保以下原功能不被破坏：

```text
canonical queue
ExecutionScheduler
building / production
worker handling
observation recorder
game recording
replay saving
```

Universal Tactical Controller 不得调用：

```text
ExecutionScheduler.replace_uncommitted_queue()
```

它只管理：

```text
combat unit roles / movement
```

---

# 47. 工程迁移顺序

## Phase 0 — Freeze

记录：

```text
原 Agent commit
新 Agent branch
旧 strategy_tools 数量
当前所有 fixed attack thresholds
当前所有 attack gates
当前所有 special tactical behavior
```

生成：

```text
TACTICAL_MIGRATION_MANIFEST.json
```

---

## Phase 1 — Inventory

扫描：

```text
SKILL/*/*/strategy_tools.py
```

抽取：

```text
race
attack_threshold
attack_gate
special behavior
common utilities
strategy-specific classes
```

输出：

```text
docs/tactical_strategy_tools_inventory.md
```

---

## Phase 2 — Universal Race Utilities

实现：

```text
race_utilities.py
```

先确保：

```text
Terran / Protoss / Zerg
```

都能启动比赛。

---

## Phase 3 — BattleSnapshot

实现统一状态提取。

Static test。

---

## Phase 4 — CompositionProfile

实现：

```text
air / ground
anti-air / anti-ground
detector / stealth
cohesion
```

---

## Phase 5 — Universal Readiness

实现：

```text
defense gate
cohesion gate
composition gate
army advantage trigger
timing trigger
max supply trigger
```

---

## Phase 6 — AdaptiveZoneAttack

继承：

```text
PlanZoneAttack
```

替换固定 attack threshold。

---

## Phase 7 — Universal Tactical Plan

所有 Human Skill Agent 改用：

```text
create_universal_tactical_plan(race)
```

---

## Phase 8 — Disable strategy_tools loading

新 Agent 不再读取：

```text
SKILL/<race>/<strategy>/strategy_tools.py
```

保留旧文件仅供 baseline。

---

## Phase 9 — Static Tests

完成：

```text
cross-skill invariance
composition safety
timing
defense
max supply
detection
```

---

## Phase 10 — SC2 Smoke Test

至少：

```text
Terran × 3 compositions
Protoss × 3 compositions
Zerg × 3 compositions
```

---

## Phase 11 — Threshold Sweep

仅允许对：

```text
global V1 parameters
```

做小范围统一 tuning。

例如：

```text
cohesion:
0.65 / 0.72 / 0.78

anti-air ratio:
0.70 / 0.80 / 0.90
```

不能：

```text
按 Skill tuning
```

---

## Phase 12 — Freeze V1

最终写：

```text
UNIVERSAL_TACTICS_V1_CONFIG.json
```

所有实验使用同一个配置。

---

# 48. 主实验要求

后续正式实验：

```text
Naive
Full
Single Trace
Static Population
Flat Adaptive
Positive Only
Frequency Only
```

如果它们属于同一个 race / map / opponent setting，则必须共享：

```text
同一个 Universal Tactical Controller V1
同一个 V1 config
同一个 unit micro system
同一个 ExecutionScheduler
```

---

# 49. 不应该做的事情

禁止：

```text
为某个 Skill 单独调 attack threshold
为 Lurker Skill 添加 Lurker-specific gate
为 Tank Skill 添加 Tank-specific timing
为 BC Skill 添加主动 jump
为 rush opening 单独改变 universal combat policy
```

否则会重新引入：

```text
Skill-specific tactical prior
```

---

# 50. V1 不做的内容

明确不在本轮实现：

```text
multi-policy tactical routing
positional push router
harass squad
air harass
drop control
capital-ship raid
learned combat policy
LLM-controlled micro
```

这些全部属于：

```text
V2+
```

---

# 51. 最终验收 Checklist

## Architecture

- [ ] 所有新 Skill 不再需要独立 `strategy_tools.py`。
- [ ] 新 Agent 不加载 strategy-specific `AUTOMATION_PROFILE`。
- [ ] 所有 Skill / Ablation 共用 Universal Tactical Controller。
- [ ] Tactical Controller 不读取 Skill 内容。
- [ ] Tactical Controller 不读取 Opening ID。
- [ ] Tactical Controller 不读取 Ablation method。

## Attack

- [ ] 固定 strategy attack threshold 被移除。
- [ ] 攻击由实时 army advantage 决定。
- [ ] 支持 army-vs-income timing window。
- [ ] 支持 max-supply attack。
- [ ] 有 cohesion gate。
- [ ] 有 composition safety gate。
- [ ] 有 detection safety gate。

## Defense / Retreat

- [ ] Base threat 优先触发 defense。
- [ ] 继续复用 PlanZoneDefense。
- [ ] 继续复用 PlanZoneAttack 的 local retreat。
- [ ] 不重新实现一套 retreat system。

## Micro

- [ ] GroupCombatManager 仍为唯一主要 combat manager。
- [ ] 默认 MicroRules 不被破坏。
- [ ] Tank micro 正常。
- [ ] Stalker micro 正常。
- [ ] BC micro 正常。
- [ ] Zerg unit micro 正常。
- [ ] GenericMicro fallback 正常。

## Experiment

- [ ] Cross-Skill invariance test 通过。
- [ ] Full / Ablations tactical config 完全一致。
- [ ] Tactical trace 可恢复每次 attack / defend / gather / retreat 原因。
- [ ] 所有实验记录 V1 config hash。

---

# 52. 最终系统结构

```text
                 Macro Agent
                     │
                     ▼
               ordered_names
                     │
                     ▼
              ExecutionScheduler


════════════════════════════════════════


                 Live SC2 State
                     │
                     ▼
                GameAnalyzer
                     │
                     ├───────────────┐
                     │               │
                     ▼               ▼
             BattleSnapshot   CompositionProfile
                     │               │
                     └───────┬───────┘
                             ▼
               Universal Tactical Controller
                             │
                 ┌───────────┼───────────┐
                 ▼           ▼           ▼
               DEFEND      GATHER      ATTACK
                                         │
                                         ▼
                               AdaptiveZoneAttack
                                         │
                                         ▼
                               GroupCombatManager
                                         │
                                         ▼
                                  Default MicroRules
                                         │
               ┌─────────────────────────┼───────────────────────┐
               ▼                         ▼                       ▼
           Unit Micro                Unit Micro              GenericMicro
```

---

# 53. 一句话设计边界

> **Macro Agent 决定造什么；Universal Tactical Controller 依据实时态势决定守、集结还是进攻；Sharpy 已有 Unit Micro 决定每种兵具体怎么打。**

V1 的核心不是提高微操复杂度，而是：

> **移除所有 Skill-specific tactical code，使 Tactical / Micro 层成为统一、实时、可复现、与 Skill 完全解耦的实验基础设施。**
