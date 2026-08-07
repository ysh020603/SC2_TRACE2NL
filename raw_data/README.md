# raw_data：暴雪官方 Replay 按对局整理库

本目录存放从本地暴雪 Replay ZIP 归档解压、并按 **实际开局种族对局（AssignedRace）** 整理后的原始 `.SC2Replay` 数据。

## 数据来源

| 项目 | 说明 |
|---|---|
| 上游渠道 | Blizzard Game Data API / `s2-client-replays`（美区） |
| 本地 ZIP 主档 | `/data2/wyq/2026_02/mini-AlphaStar/scripts/download_replay/third/download` |
| 版本筛选 | 归档名均为 `4.10.0.75689-*`（按客户端版本 `4.10.0` 下载） |
| ZIP 概况 | 100 个包；其中 **16 个非空**、**84 个合法空包** |
| 授权 | [AI and Machine Learning License](https://blzdistsc2-a.akamaihd.net/AI_AND_MACHINE_LEARNING_LICENSE.html)；解压密码 `iagreetotheeula` |
| 核验记录 | [`docs/SC2_暴雪Replay本地资产核验总结.md`](docs/SC2_暴雪Replay本地资产核验总结.md) |

这些 ZIP **不是按种族分包**，而是按打包日期/分片存放的混合天梯 1v1 包。本目录在解压后按对局二次整理。

详细核验结论（103,787 唯一文件名、第一包 4,049 局等）见 `docs/` 中归档文档。

## 目录结构

```text
raw_data/
  README.md                          # 本说明
  manifest.json                      # 解压/分类统计清单
  docs/
    SC2_暴雪Replay本地资产核验总结.md  # 来源核验归档
  by_matchup/
    PvP/   # 神族 vs 神族
    PvT/   # 神族 vs 人族
    PvZ/   # 神族 vs 虫族
    TvT/   # 人族 vs 人族
    TvZ/   # 人族 vs 虫族
    ZvZ/   # 虫族 vs 虫族
  logs/                              # 解压日志（可选）
```

## 分类规则

1. 只处理非空 ZIP（大小 > 22 字节）。
2. 从每个 replay 的 `replay.gamemetadata.json` 读取两位玩家的 **AssignedRace**（实际开局种族，Random 已落成 P/T/Z）。
3. 按无序对局归类：`PvT == TvP`，以此类推。
4. 跨 ZIP 重复文件名只保留首次出现的副本，不重复累计。
5. **不修改** 源 ZIP 目录；原始归档仍视为只读主档。

分类脚本：`scripts/extract_blizzard_zips_by_matchup.py`。

## 当前统计

解压分类已完成（详见 `manifest.json`）：

| 对局 | 局数 | 约占用 |
|---|---:|---:|
| PvP | 10,336 | 594 MiB |
| PvT | 25,449 | 1.8 GiB |
| PvZ | 19,016 | 1.4 GiB |
| TvT | 16,060 | 1.1 GiB |
| TvZ | 23,161 | 2.0 GiB |
| ZvZ | 9,765 | 628 MiB |
| **合计（唯一）** | **103,787** | **约 7.5 GiB** |

补充：

- 跨 ZIP 重复文件名跳过：**567**
- 解析失败：**0**
- 分类依据：`AssignedRace` 无序对局
- 耗时：约 3165 秒

说明：旧笔记中的 “TvT 约 16,060” 与本次全量分类结果一致；“虫族约 9,620”接近本次 ZvZ 9,765，但历史 `replay_zvz` 目录本身仍未找回。

快速复核：

```bash
python - <<'PY'
import json
from pathlib import Path
m = json.loads(Path('raw_data/manifest.json').read_text())
print('written:', m.get('written'))
print('duplicates_skipped:', m.get('duplicate_skipped'))
print('parse_errors:', m.get('parse_errors'))
print('matchups:', m.get('matchup_counts'))
PY
```

## 宏观指令解析（适用于本批数据）

这批暴雪 AI/ML Replay 没有 `replay.tracker.events`，因此原有 tracker
解析器无法确认单位出生、建筑完成、死亡、资源和人口状态。不过，
`replay.game.events` 完整保留了玩家下达的操作指令。

仓库新增了独立解析命令，**不改变原有 tracker 解析流程**：

```bash
# 单局
sc2mine parse-actions-file \
  raw_data/by_matchup/TvZ/<replay>.SC2Replay \
  --json-out data/action_json/TvZ

# 单个对局目录
sc2mine parse-actions-dir raw_data/by_matchup/TvZ \
  --json-out data/action_json/TvZ \
  --workers 4
```

新解析器只保留以下宏观指令：

- `production`：生产工人和作战单位；
- `construction`：建造建筑、气矿和附属建筑；
- `tech_morph`：基地/科技建筑变形；
- `upgrade_research`：研究科技和攻防升级。

它会丢弃攻击、移动、右键、选中、编队、相机等微操事件，也不会输出
目标坐标或单位位置。JSON 保持与现有 full-match 输出相近的结构，但
`build_order` 的含义是玩家**下达命令**，不是确认完成：

```json
{
  "time": "00:24",
  "event": "construction",
  "action": "ordered",
  "name": "SupplyDepot",
  "ability": "BuildSupplyDepot",
  "standard_action_name": "TERRANBUILD_SUPPLYDEPOT",
  "standard_result_name": "SupplyDepot",
  "standard_result_type": "Unit",
  "standard_mapping_status": "result_and_semantic",
  "source": "game_events",
  "observed_completed": false
}
```

`ability` 保留 Replay/sc2reader 原始名称；`standard_action_name` 映射到
`data_sc2_260701/data_base_sc2_260701.json` 的 `Ability.name`。无法在该
标准库中找到对应项时不会猜测错误名称，而是输出 `null`，并记录在
`unmapped_abilities` 和 `data_quality.standard_action_unmapped`。

预计完成时间由命令时间加 sc2reader 的 balance build time 得出，仅供参考。
每个文件的 `data_quality` 会明确记录不可获得的信息。瞬间退出或不足一分钟
的极短对局可能没有宏观动作，这不属于解析失败。

### 分层抽样结果（2026-08-05）

按 PvP/PvT/PvZ/TvT/TvZ/ZvZ 各抽 40 局，共 240 局：

- 成功：**240/240（100%）**；
- 宏观指令：**33,092** 条；
- `production`：20,831；
- `construction`：9,850；
- `tech_morph`：532；
- `upgrade_research`：1,879；
- 标准 Action 映射：**33,081/33,092（99.967%）**；
- 未映射：11 条，均为 `EvolvePathogenGlands`；当前标准库中不存在
  Pathogen Glands 对应的 Ability/Upgrade 条目；
- 微操能力泄漏：**0**；
- 坐标/位置字段：**0**；
- JSON 格式错误：**0**。
- 51 个玩家侧没有宏观动作，抽查均为 0～数十秒内结束的极短局；
  这些文件元数据和事件流均成功读取，不计为解析失败。

抽样结果保存在被 gitignore 的 `raw_data/logs/action_samples/`，不会提交
大量派生 JSON。

## 与仓库其他数据的关系

| 路径 | 角色 |
|---|---|
| `raw_data/by_matchup/*` | 暴雪官方大批量原始 replay（按对局） |
| `data/replays/<category>/` | 本仓库解析流水线的待处理输入（小样本/精选） |
| `data/artifacts/`、`data/full_json/` | `sc2mine` 解析产物 |
| `data/action_json/` | 基于 game events 的宏观指令 JSON |

建议：需要全量或按种族实验时从 `raw_data` 取数；日常解析仍按 README 主流程把子集拷入 `data/replays/<category>/`。

## 重新生成

```bash
conda activate sc2replay
python scripts/extract_blizzard_zips_by_matchup.py \
  --zip-dir /data2/wyq/2026_02/mini-AlphaStar/scripts/download_replay/third/download \
  --out-dir /data2/shy_2608/SC2trace2nl/raw_data
```

脚本支持断点续跑：目标目录中已存在的同名 `.SC2Replay` 会跳过。

## 注意

- `.SC2Replay` 二进制默认被 `.gitignore` 忽略；文档与 `manifest.json` 可纳入版本管理。
- 包内可能混有邻近 build（如 `4.9.3` / `4.10.1`），解析时请读 replay 内部版本，不要只信 ZIP 文件名。
- 请勿在源 ZIP 目录原地解压或覆盖。
