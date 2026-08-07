# SC2 TRACE2NL / sc2-replay-miner

从人类对战 `.SC2Replay` 中提取双边宏观事实与近似 Build Order，并支撑后续开局策略挖掘、Skill 生成，以及与 knowledge-backed SC2 Agent 的对接。

面向 agent / 人类的标准数据流：

1. 将待解析 replay 放入 `data/replays/<category>/`，或使用 `raw_data/by_matchup/` 全量库
2. 有 tracker 时：`sc2mine parse-dir --category <category>`
3. 无 tracker（暴雪 AI/ML 包）时：`sc2mine parse-actions-dir ...`
4. 读取 `data/artifacts/`、`data/full_json/` 或 `data/action_json/`
5. 可选：跑 `analysis/` 策略挖掘，消费 `SKILL/` 与 submodule `SC2-Agent-knowlegde/`

## Hard constraints

- **不要**安装 StarCraft II 客户端、PySC2，也不要在游戏里回放。
- Tracker 主解析：`sc2reader==1.9.0`，`load_level=3`（metadata + players + tracker events）。
- 宏观指令解析：`load_level=4`（`game.events`），用于缺少 tracker 的批次。
- 主动流水线范围：**human vs human**；本地 AI / agent 对战日志见 [`archive/local_ai_logs/`](archive/local_ai_logs/README.md)。
- 真实 API 密钥只放本地 `API_config/config.json`（已 gitignore）；仓库只保留 `config.example.json`。

## Repository layout

```text
SC2trace2nl/
├── README.md
├── pyproject.toml                 # package: sc2-replay-miner, CLI: sc2mine
├── .gitmodules                    # SC2-Agent-knowlegde submodule
│
├── src/sc2_replay_miner/          # 解析器、BO、导出、CLI
├── tests/                         # pytest
├── configs/                       # 种族 taxonomy / morph whitelist / 默认参数
├── scripts/                       # bootstrap、下载、批量、暴雪 ZIP 解压分类
│
├── data/
│   ├── replays/<category>/        # 待解析 human replay（按类别）
│   ├── artifacts/<category>/      # parquet / 报告 / 错误（非完整 JSON）
│   ├── full_json/<category>/      # tracker 路径的完整对局 JSON
│   └── action_json/<matchup>/     # game.events 宏观指令 JSON
│
├── raw_data/                      # 暴雪官方大批量 replay（按 PvP/PvT/... 整理）
├── data_sc2_260701/               # 标准 Ability/Unit/Upgrade 知识库（动作名映射）
│
├── analysis/                      # 开局策略发现流水线（plan Phase 1–8 / plan2 pilot）
├── SKILL/                         # 分种族 adaptive Skill（skill.json + Top_agent.md）
├── plans/                         # 设计方案归档（plan.md / plan_2.md）
│
├── API_Tools/                     # LLM 调用与 reasoning 抽取工具
├── API_config/                    # config.example.json（真实 config.json 本地自建）
│
├── SC2-Agent-knowlegde/           # git submodule：knowledge-backed SC2 Agent
├── archive/local_ai_logs/         # 非 human 样本归档
├── vendor/                        # 可选外部参考钉扎（非运行时依赖）
└── logs/                          # 运行日志（gitignore 内容）
```

二进制 replay、大批量生成 JSON、真实 API key 均不入库；目录骨架（`README.md` / `.gitkeep`）保留在 Git 中。

## Environment setup

推荐 Conda + Python 3.11。

```bash
conda create -n sc2replay python=3.11 -y
conda activate sc2replay

# 可选国内镜像
export PIP_INDEX_URL=https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
export PIP_DEFAULT_TIMEOUT=120

bash scripts/bootstrap.sh
```

`scripts/bootstrap.sh` 会以 editable 模式安装包（`pip install -e ".[dev]"`），并写入 `requirements.lock.txt` / `environment.txt`。

校验：

```bash
python -c "import sc2reader; print(sc2reader.__version__)"
sc2mine version
```

克隆时请带上 Agent 子模块：

```bash
git clone --recurse-submodules git@github.com:ysh020603/SC2_TRACE2NL.git
# 若已克隆：
git submodule update --init --recursive
```

本地 API（仅在需要调 LLM 时）：

```bash
cp API_config/config.example.json API_config/config.json
# 编辑 config.json，填入真实 key；该文件不会被提交
```

## Data layout

### Category contract（tracker 路径）

类别名在三棵树之间镜像，统一使用 `snake_case`：

```text
data/
  replays/<category>/       # 输入 .SC2Replay
  artifacts/<category>/     # parquet、报告、错误、预览
  full_json/<category>/     # 完整对局 JSON
```

| Category | Meaning |
|----------|---------|
| `human_ladder` | 天梯 / 匹配 |
| `human_tournament` | 职业 / 赛事 |
| `sc2reader_official` | sc2reader 官方 `test_replays/5.0.15` 样本 |

### Matchup contract（暴雪全量 / action 路径）

```text
raw_data/by_matchup/{PvP,PvT,PvZ,TvT,TvZ,ZvZ}/
data/action_json/{PvP,PvT,PvZ,TvT,TvZ,ZvZ}/
```

`raw_data/` 来自暴雪 AI/ML Replay 归档，按 AssignedRace 对局整理；多数文件**没有** `replay.tracker.events`，应走 action parser。详见 [`raw_data/README.md`](raw_data/README.md)。

### Canonical action database

`data_sc2_260701/data_base_sc2_260701.json` 提供标准 `Ability` / `Unit` / `Upgrade` 名称与关系图。  
action parser 用它把 replay 原始能力名映射为 `standard_action_name`（例如 `BuildSupplyDepot` → `TERRANBUILD_SUPPLYDEPOT`）。结构说明见 [`data_sc2_260701/DATA_STRUCTURE.md`](data_sc2_260701/DATA_STRUCTURE.md)。

## Tracker pipeline（有 tracker events）

1. 将 `.SC2Replay` 放入 `data/replays/<category>/`
2. 解析：

```bash
sc2mine parse-dir --category <category> --workers 4
```

3. 可选报告：

```bash
sc2mine report data/artifacts/<category>
```

4. 消费：
   - 表格 / 运维输出：`data/artifacts/<category>/`
   - 单局完整 JSON：`data/full_json/<category>/<replay_id>.json`
   - 合并数组：`data/full_json/<category>/full_matches.json`

等价显式形式：

```bash
sc2mine parse-dir data/replays/<category> \
  --artifacts data/artifacts/<category> \
  --json-out data/full_json/<category>
```

### Useful commands

```bash
sc2mine inspect data/replays/sc2reader_official/95435_0.SC2Replay
sc2mine parse-file path/to/game.SC2Replay --category human_ladder
sc2mine show-bo data/replays/human_tournament/some.SC2Replay --type strategy_8m
bash scripts/download_test_replays.sh
bash scripts/run_small_batch.sh sc2reader_official
```

### Artifacts / full JSON / BO 含义

**Artifacts**（`data/artifacts/<category>/`）：

| File | Meaning |
|------|---------|
| `replays.parquet` | 每局一行：版本、地图、时长、解析状态 |
| `players.parquet` | 玩家、种族、胜负、MMR（缺失为 `null`） |
| `macro_events.parquet` | 全场宏观事件时间线 |
| `build_orders.parquet` | `core_6m` / `strategy_8m` / `all_macro` |
| `summary_report.json` | 批次成功率、对局、未知名 |
| `unknown_names.json` | 未知单位/建筑名 |
| `parse_errors.jsonl` | 逐文件失败（仅有错误时出现） |
| `preview.json` | 单文件调试预览 |
| `sample_build_orders.md` | `report` 生成的可读 BO 样本 |

**Full JSON**：自包含对局文档，含地图/版本/时长/matchup、`winner`/`winners`、玩家信息，以及 `timeline` / `build_order*`。

**Build-order 定义**：

- `core_6m`：前 6 分钟建筑开工、科技变形、升级
- `strategy_8m`：core + 早期关键/基础单位出生
- `all_macro`：全场宏观事件，用于重生其他 BO 视图

分类与 morph 白名单在 `configs/`，不要在 `parser.py` 里硬编码完整单位表。

## Macro action parser（无 tracker / `game.events`）

原有 tracker 解析器保持不变。对缺少 `replay.tracker.events` 的暴雪包使用独立 action parser：

```bash
# 单局
sc2mine parse-actions-file path/to/game.SC2Replay \
  --json-out data/action_json \
  --action-database data_sc2_260701/data_base_sc2_260701.json

# 目录
sc2mine parse-actions-dir raw_data/by_matchup/TvZ \
  --json-out data/action_json/TvZ \
  --workers 4

# 可复现抽样
sc2mine parse-actions-dir raw_data/by_matchup/TvZ \
  --json-out raw_data/logs/action_sample/TvZ \
  --limit 40 --seed 42 --workers 4
```

保留的宏观指令：

- `production`：工人与作战单位
- `construction`：建筑、气矿、附属建筑
- `tech_morph`：基地/科技建筑变形
- `upgrade_research`：科技与攻防升级

排除攻击、移动、右键、选中、编队、相机等微操；不导出坐标/位置。

语义是**命令意图**，不是观测完成态：每项为 `action: "ordered"`、`source: "game_events"`、`observed_completed: false`。  
`ability` 保留原始名；`standard_action_name` 来自标准库；无法映射时为 `null` 并记入 `unmapped_abilities`，绝不静默猜名。详见 [`data/action_json/README.md`](data/action_json/README.md) 与各文件的 `data_quality`。

## Analysis & Skills

| Path | Role |
|------|------|
| [`plans/`](plans/README.md) | 方案归档：`plan.md`（开局策略发现）、`plan_2.md`（自适应 Skill） |
| [`analysis/`](analysis/README.md) | Phase 1–8 统计流水线与产出；plan2 pilot 脚本 |
| [`SKILL/`](SKILL/README.md) | 9 个分种族 pilot Skill（`skill.json` / `evidence.json` / `Top_agent.md`） |

复现分析（需已有 `data/action_json`）：

```bash
conda activate sc2replay
python analysis/phase1_audit/run_audit.py
python analysis/run_pipeline.py
python analysis/plan2/run_plan2_pilot.py
```

Skill 目录约定：

```text
SKILL/<race>/<strategy>/
  skill.json
  evidence.json
  Top_agent.md
  validation_report.json
```

## SC2-Agent submodule

Knowledge-backed agent 以 **git submodule** 挂在仓库根目录（不在 `vendor/`）：

| Local path | Remote | Branch |
|------------|--------|--------|
| `SC2-Agent-knowlegde/` | [ysh020603/SC2-Agent-260510](https://github.com/ysh020603/SC2-Agent-260510/tree/SC2-Agent-knowlegde) | `SC2-Agent-knowlegde` |

```bash
git submodule update --init --recursive

# 拉取上游并更新钉住的 submodule commit
git submodule update --remote SC2-Agent-knowlegde
git add SC2-Agent-knowlegde
git commit -m "Bump SC2-Agent-knowlegde submodule"
```

`API_Tools/` 与 `API_config/` 也在本仓库根目录提供一份可提交工具与 example 配置，供分析 / LLM 调用使用；子模块内部另有对应目录。

## CLI overview

| Command | Purpose |
|---------|---------|
| `sc2mine inspect` | 查看单局 tracker 字段 |
| `sc2mine parse-file` / `parse-dir` | tracker 路径解析 |
| `sc2mine parse-actions-file` / `parse-actions-dir` | game.events 宏观指令解析 |
| `sc2mine show-bo` | 可读 Build Order |
| `sc2mine report` | artifacts 汇总报告 |
| `sc2mine version` | 版本 |

## Tests

```bash
pytest -q
ruff check .
```

## Known limitations

1. Tracker 事件给出的是单位完成时间，不是点击/下单时间。
2. 赛事房可能 `mmr = null`。
3. `UnitTypeChangeEvent` 仅保留白名单科技变形。
4. 本地 AI/agent replay 已归档，不在主动流水线中。
5. Action JSON 无法确认完成、死亡、资源、人口，也难以可靠关联取消；极短对局可能没有宏观动作。
6. Skill 中的对手风格标签目前可由完整对手 BO 派生（oracle）；上线需映射到可侦察情报。胜率为关联证据，不是因果。
