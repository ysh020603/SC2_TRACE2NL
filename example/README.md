# 解析数据样例（example）

本目录存放少量**已解析**的对局 JSON，用于快速理解两种输出格式，无需下载全量 `raw_data` / `data/action_json`。

| 子目录 | 来源解析器 | 语义 |
|--------|------------|------|
| [`action_json/`](action_json/) | `sc2mine parse-actions-*`（`game.events`） | 玩家**下达的宏观指令**（意图） |
| [`full_json/`](full_json/) | `sc2mine parse-file/parse-dir`（tracker） | 观测到的单位出生 / 建筑完成等事件 |

索引摘要见 [`samples_index.json`](samples_index.json)。

## 样例列表

| 文件 | 对局 | 地图 | 时长 | timeline 条数 | 说明 |
|------|------|------|------|---------------|------|
| `action_json/PvP_24ffab6e684b489337ffdaaf.json` | PP | Kairoskreuz LE | ~10:11 | 31 | 神族镜像，无 tracker |
| `action_json/PvT_8abbe43bf2fa7f6f273e0138.json` | PT | Thunderbird LE | ~08:35 | 30 | 神族 vs 人族 |
| `action_json/TvZ_9616e16a8ec30a99ff0ff3a5.json` | TZ | Kairos Junction LE | ~09:23 | 31 | 人族 vs 虫族 |
| `action_json/ZvZ_5880dc45b29cbc4eca33c771.json` | ZZ | Acropolis EC | ~05:33 | 29 | 虫族镜像 |
| `full_json/tracker_PvT_d7e1c3fa6acac1064cdb1752.json` | PT | Old Republic LE | — | 106 | sc2reader 官方样本，含 tracker |

> 样例中的 `source_file` 已改为仅文件名；`data_quality.standard_action_database` 改为仓库相对路径，避免泄露本机绝对路径。

## 如何复现

```bash
# action_json（暴雪包 / 无 tracker）
sc2mine parse-actions-file path/to/game.SC2Replay \
  --json-out data/action_json/TvZ \
  --action-database data_sc2_260701/data_base_sc2_260701.json

# full_json（有 tracker）
sc2mine parse-file path/to/game.SC2Replay --category sc2reader_official
```

---

## 一、`action_json` 格式（命令意图）

适用：`raw_data/by_matchup/*` 等缺少 `replay.tracker.events` 的批次。

### 顶层字段

| 字段 | 类型 | 含义 |
|------|------|------|
| `replay_id` | string | 对局 ID（通常为源文件内容哈希前缀） |
| `source_file` | string | 源 replay 路径/文件名 |
| `map_name` | string | 地图名 |
| `version` / `base_build` | string / int | 客户端版本 |
| `duration_seconds` / `duration_clock` | number / string | 时长 |
| `game_type` / `real_type` | string | 如 `1v1` |
| `region` | string | 地区代码 |
| `played_at` | string | ISO 时间 |
| `matchup` | string | 简写对局，如 `PT` / `TZ` / `PP` |
| `winner` / `winners` | object / list | 胜者信息 |
| `players` | list | 玩家对象（含各自 `build_order`） |
| `timeline` | list | **全场**宏观指令时间线（双边混合，按时间排序） |
| `macro_action_count` | int | `timeline` 长度 |
| `game_event_counts` | object | 原始 game event 类型计数 |
| `unmapped_abilities` | list | 未能映射到标准库的能力名 |
| `tracker_event_counts` | object | 通常为空对象（无 tracker） |
| `data_quality` | object | 数据质量与不可用字段声明 |
| `parser_version` | string | 解析器版本 |

### `players[]` 主要字段

| 字段 | 含义 |
|------|------|
| `player_id` | 玩家编号 |
| `name` / `race` / `pick_race` | 名称与种族 |
| `result` / `is_winner` | 胜负 |
| `mmr` / `mmr_available` | MMR（可能为 `null`） |
| `build_order` | **该玩家**的宏观指令列表（结构与 timeline 项相同，但不重复 `player_id` 等归属字段） |

### timeline / build_order 单条事件

```json
{
  "time": "00:01",
  "second": 1.0,
  "frame": 20,
  "event": "production",
  "action": "ordered",
  "name": "Probe",
  "ability": "TrainProbe",
  "standard_action_name": "NEXUSTRAIN_PROBE",
  "standard_result_name": "Probe",
  "standard_result_type": "Unit",
  "standard_mapping_status": "result_and_semantic",
  "standard_mapping_confidence": 1.0,
  "occurrence_index": 1,
  "queued": false,
  "build_time_seconds": 17.0,
  "estimated_completion_second": 18.0,
  "estimated_completion_time": "00:18",
  "source": "game_events",
  "observed_completed": false,
  "text": "00:01 Probe #1 ordered",
  "player_id": 1,
  "player_name": "",
  "race": "Protoss"
}
```

字段说明：

| 字段 | 含义 |
|------|------|
| `event` | 宏观类别：`production` / `construction` / `tech_morph` / `upgrade_research` |
| `action` | 固定为 `ordered`（下单，不是确认完成） |
| `name` | 可读结果名（单位/建筑/升级） |
| `ability` | sc2reader / replay 原始能力名 |
| `standard_action_name` | `data_sc2_260701` 中的标准 `Ability.name`；无法映射时为 `null` |
| `standard_result_name` / `standard_result_type` | 标准结果实体及类型（`Unit` / `Upgrade` 等） |
| `estimated_completion_*` | 用 balance build time **估算**完成时刻，不证明实际完成 |
| `observed_completed` | 恒为 `false`（本模式无 tracker 观测） |
| `source` | 恒为 `game_events` |

### `data_quality`（务必阅读）

典型声明：

- `parse_mode`: `game_events_macro_actions`
- `semantics`: `player_command_intent`
- `tracker_available`: `false`
- `positions_included` / `micro_actions_included`: `false`
- `unavailable`: 无法提供的信息列表，例如确认出生/完工、死亡、资源与人口状态、可靠取消关联等

**不要**把 action_json 当成“单位已经造出来”的观测日志。

---

## 二、`full_json` 格式（tracker 观测）

适用：含 `replay.tracker.events` 的 human / sc2reader 样本。

### 与 action_json 的关键差异

| 维度 | action_json | full_json (tracker) |
|------|-------------|---------------------|
| 事件来源 | `game.events` 下单 | tracker 出生/完工等 |
| `action` 示例 | `ordered` | `born` 等 |
| 是否含坐标 | 否 | timeline 可含 `x` / `y` |
| 玩家 BO 视图 | 仅 `build_order` | 另有 `build_order_core_6m` / `build_order_strategy_8m` |
| 完成语义 | 估算、未观测 | 更接近“已出现在场上” |

### 顶层字段（样例）

与 action 路径共享大量元数据字段（`replay_id`、`map_name`、`matchup`、`players`、`timeline` 等），并额外包含例如：

- `tracker_event_counts`
- `unknown_names`
- 玩家侧 `build_order_core_6m` / `build_order_strategy_8m`

### tracker timeline 单条示例

```json
{
  "time": "00:17",
  "second": 17.0,
  "frame": 284,
  "player_id": 2,
  "player_name": "HADB",
  "race": "Terran",
  "event": "unit_born",
  "action": "born",
  "name": "SCV",
  "occurrence_index": 1,
  "x": 138.0,
  "y": 132.0,
  "text": "00:17 SCV #1 born"
}
```

### Build Order 视图定义

- `build_order`：该玩家全场宏观相关事件序列
- `build_order_core_6m`：前 6 分钟建筑开工 / 科技变形 / 升级
- `build_order_strategy_8m`：core + 早期关键/基础单位

分类规则见仓库根目录 `configs/`。

---

## 三、命名与标准库

两套名字会同时出现在 action 路径中：

1. **原始名** `ability`：如 `BuildSupplyDepot`、`TrainProbe`
2. **标准名** `standard_action_name`：如 `TERRANBUILD_SUPPLYDEPOT`、`NEXUSTRAIN_PROBE`

标准名来自 [`data_sc2_260701/data_base_sc2_260701.json`](../data_sc2_260701/data_base_sc2_260701.json)。  
映射失败时 `standard_action_name = null`，并记入顶层 `unmapped_abilities`，解析器**不会**静默猜名。

---

## 四、阅读建议

1. 先打开任意 `action_json/*.json`，看 `data_quality`，确认语义边界。
2. 对照同一文件的 `timeline` 与 `players[*].build_order`：前者双边混排，后者按玩家切分。
3. 再打开 `full_json/tracker_*.json`，对比 `action: born` 与坐标字段，理解 tracker 观测差异。
4. 全量数据仍在 `data/action_json/<matchup>/` 与 `data/full_json/<category>/`（生成物默认 gitignore）。

更多流水线说明见根目录 [`README.md`](../README.md)、[`data/action_json/README.md`](../data/action_json/README.md)、[`raw_data/README.md`](../raw_data/README.md)。
