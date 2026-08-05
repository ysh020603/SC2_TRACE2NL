# SC2 暴雪 Replay 本地资产核验总结

> 整理依据：2026-08-05 完成的本地只读搜索、ZIP 目录核验、少量 replay 抽样、脚本哈希与来源对照。  
> 本文是结论摘要，不替代原始核验记录；所有路径均为当时 Windows 本地路径。

## 一、结论摘要

这次核验已经确认：**此前从暴雪渠道下载的 Replay 归档和对应下载脚本仍保存在本地**，历史记录中的“103,787 局”也找到了可靠的数据依据。

但要区分三种统计口径：

| 统计对象 | 数量 | 含义 |
|---|---:|---|
| ZIP 文件 | 100 个 | 暴雪 replay-api 下载形成的归档包 |
| ZIP 内 `.SC2Replay` 条目 | 104,354 个 | 包含跨 ZIP 重复条目 |
| 唯一 replay 文件名 | 103,787 个 | 对 ZIP 成员名去重后的结果；对应旧笔记的“约 103,787 局” |
| 当前已解压 replay | 4,049 个 | 仅与第一个官方 ZIP 完全对应，不是全部归档的解压结果 |

因此，目前可以确认的是：

- 官方归档数据仍在，100 个 ZIP 共约 3.56 GiB；
- 103,787 是归档内唯一 replay 文件名数量，不是磁盘上已解压文件数；
- 已解压的 4,049 个 replay 是第一包的完整内容；
- 没有证据证明这 4,049 个文件是 TvT、ZvZ 或其他种族筛选子集；
- 下载脚本仍在，但属于 mini-AlphaStar 保存并修改的 Blizzard 官方脚本衍生版；
- replay 数据已找回，原先完整的 DI-Star/PySC2 运行环境则尚未找回。

## 二、已确认的核心资产

### 1. 暴雪官方 Replay ZIP 库

- 路径：`D:\wyq\code\wyq\2026_02\mini-AlphaStar\scripts\download_replay\third\download`
- ZIP 数量：100 个
- 总大小：3,825,201,401 字节，约 3.56 GiB
- 版本命名：全部以 `4.10.0.75689-` 开头
- ZIP 状态：100 个均可正常读取
- 非空 ZIP：16 个
- 合法空 ZIP：84 个
- replay 条目总数：104,354 个
- 唯一 replay 文件名：103,787 个
- 重复的额外条目：567 个

这批 ZIP 应视为当前最重要的**原始数据主档**。84 个空 ZIP 是结构合法的空归档，不应直接当作损坏文件删除。

### 2. 已解压 Replay

- 路径：`D:\wyq\code\wyq\2026_02\mini-AlphaStar\data\Replays\filtered_replays_1`
- replay 数量：4,049 个
- 总大小：304,394,808 字节，约 290.3 MiB
- 对应归档：`4.10.0.75689-20190814_114049-1.zip`

文件名和文件大小均与第一份官方 ZIP 的 4,049 个成员逐一匹配。因此，该目录应理解为“第一包的完整解压结果”，而不能根据目录名 `filtered_replays_1` 推断它已经完成种族筛选。

抽样中同时出现 PvZ、PvP、TvT、ZvZ、TvZ 和 PvT，更进一步说明它不是已确认的纯 TvT 或纯 ZvZ 数据集。

### 3. 下载脚本

- 路径：`D:\wyq\code\wyq\2026_02\mini-AlphaStar\scripts\download_replay\third\download_replays.py`
- 大小：9,449 字节
- SHA-256：`D4C710756F1E3AB968DC56186143CD73ED109D489629F0BFF51C8A6CE7C192B9`
- 项目来源：`https://github.com/liuruoze/mini-AlphaStar.git`
- 上游基础：Blizzard `s2client-proto/samples/replay-api`

脚本保留了以下关键能力：

- 通过 Battle.net OAuth 获取访问令牌；
- 查询 `s2-client-replays`；
- 按 SC2 版本批量下载 ZIP；
- 使用 `iagreetotheeula` 解压；
- 通过 `--filter_version` 保留、删除或分类不同版本 replay；
- 通过 `--extract`、`--download_dir` 和 `--replays_dir` 控制下载与输出。

它与 Blizzard 当前官方仓库文件哈希及部分功能不同，因此准确表述应为：**基于 Blizzard 官方 replay-api 的 mini-AlphaStar 修改版**，而不是“未经修改的官方原版”。

脱敏后的等价调用方式为：

```bash
python download_replays.py \
  --key='<BLIZZARD_CLIENT_ID>' \
  --secret='<BLIZZARD_CLIENT_SECRET>' \
  --version='4.10.0' \
  --replays_dir='<NEW_WORKING_DIR>/Replays' \
  --download_dir='./download' \
  --extract \
  --filter_version='keep'
```

恢复使用时应输出到新目录，不要直接覆盖现存 ZIP 和已解压数据。

## 三、版本与数据关系

### 已确认的版本

归档文件名、mini-AlphaStar 配置和第一包解压文件之间相互印证，说明原下载流程主要使用：

- SC2 版本：`4.10.0`
- 具体 build：`4.10.0.75689`

但 archive 的查询版本不等于每个 replay 的内部版本。对 4,049 个已解压文件抽取 20 个样本后：

- 16 个内部版本为 `4.10.0.75689`；
- 4 个内部版本为 `4.9.3.75025`。

这说明数据包内部存在版本混合。后续解析程序必须按 replay 的实际 build 处理，不能只依据 ZIP 文件名硬编码。

### 数据链路

```text
Blizzard Game Data API / s2-client-replays
    └─ 100 个 4.10.0.75689-*.zip
       ├─ 16 个非空包
       ├─ 84 个合法空包
       └─ 104,354 个 replay 条目 / 103,787 个唯一文件名
          └─ 第一包：4,049 个 replay
             └─ filtered_replays_1：4,049 个完全对应的已解压文件
                └─ mini-AlphaStar / PySC2 转换代码的默认输入之一
```

SC2_scout_RL、sharpy-sc2、SC2-Agent 等目录中的 replay 属于模型、LLM、SL/RL 或测试运行生成的数据，应与官方下载归档分开统计。

## 四、对旧记录的修正

| 旧记录或推测 | 本次结论 | 状态 |
|---|---|---|
| 全部 replay 约 103,787 局 | 与 ZIP 内唯一 replay 文件名数完全一致 | 已确认，但须注明统计口径 |
| 虫族 replay 约 9,620 个 | 未找到 `replay_zvz` 或可对应的数据目录 | 未确认 |
| TvT replay 约 16,060 局 | 未找到 `replay_tvt`、`replay_tvt_1`～`replay_tvt_8` | 未确认 |
| 主要版本为 4.10.0 | 归档和代码均支持，具体 build 为 75689 | 已确认 |
| 下载或处理过 5.0.15 | 未找到归档、数据或日志证据 | 未确认 |
| 已保存完整 DI-Star 工程 | 只发现路径引用和受其启发的 mini-AlphaStar 代码 | 未找到 |
| `filtered_replays_1` 是种族筛选集 | 实际与第一 ZIP 完全对应，抽样种族混合 | 已否定原推测 |

后期某份统计只扫描了 500 个文件，其中 499 个可读、69 个 TvT。该小批次结果不能用来推导历史“16,060 个 TvT”的结论。

## 五、与当前 Replay 解析失败的关系

本次核验说明：**问题不是原始 replay 数据已经丢失，而是完整的解析运行环境和部分历史处理结果没有一起保存下来。**

目前仍缺少：

- 完整 DI-Star 源码树；
- `replay_zvz`、`replay_tvt_*` 等历史筛选结果；
- `gen_z.py`；
- SC2 `Versions` 目录中的匹配客户端，例如 Base75689；
- Battle.net Cache、部分地图和完整数据版本依赖；
- `5.0.15` 数据包或对应运行记录。

这与此前 PySC2 脚本的实际报错一致：脚本能够导入，但在启动 replay 前找不到硬编码的 `/data2/SC2/StarCraftII/Versions`。因此，恢复下载数据与恢复 PySC2 观测解析是两个不同问题：

1. **下载数据恢复：已基本完成。**ZIP、第一批解压文件和下载脚本均已找到。
2. **完整 observation/action 转换环境：尚未恢复。**若需要 PySC2 原始观测，仍需匹配的 SC2 客户端、地图和缓存。
3. **无需客户端的事件解析：仍可继续修复。**主要 replay 已包含 tracker/game events，可优先修复 `sc2reader` 对 `.backup` 元数据的回退逻辑。

## 六、建议的保全与后续处理顺序

### 数据保全

1. 将 100 个 ZIP 作为原始只读档案，不在原目录解压、删除或覆盖。
2. 保留现有重复副本作为冗余，但统计时不要重复累加。
3. 为每个 ZIP 生成独立 SHA-256 清单；现有 manifest 指纹只基于文件名、大小和时间，不等于每个 ZIP 的内容哈希。
4. 将数据明确分为：`raw_archives`、`extracted_replays`、`generated_replays`、`derived_outputs`。
5. 所有重新下载和解析工作均在新建工作目录中进行。
6. 历史 Blizzard Client ID/Secret 即使未在本次检查中发现，也应撤销并轮换；新凭据不要写入脚本、Markdown 或命令历史。

### 解析路线

建议按成本从低到高推进：

1. 先用 `s2protocol` 或修复后的 `sc2reader` 读取 replay 内部元数据、tracker events 和 game events；
2. 为缺少主 `replay.details.cache_handles` 的文件增加 `.backup` 元数据回退；
3. 在少量 replay 上验证单位、建造、升级、资源和玩家动作字段；
4. 只有确实需要完整 PySC2 observation/action 对齐时，再恢复 Base75689 对应的 SC2 客户端、地图和 Cache；
5. 小样本通过后，再对 103,787 个唯一 replay 建索引和批处理，不要直接全量运行。

## 七、关键路径与指纹

| 对象 | 路径或指纹 |
|---|---|
| 官方 ZIP 主目录 | `D:\wyq\code\wyq\2026_02\mini-AlphaStar\scripts\download_replay\third\download` |
| 4,049 个已解压 replay | `D:\wyq\code\wyq\2026_02\mini-AlphaStar\data\Replays\filtered_replays_1` |
| 下载脚本 | `D:\wyq\code\wyq\2026_02\mini-AlphaStar\scripts\download_replay\third\download_replays.py` |
| 下载脚本 SHA-256 | `D4C710756F1E3AB968DC56186143CD73ED109D489629F0BFF51C8A6CE7C192B9` |
| 100 ZIP manifest SHA-256 | `033336d34bf11d7d17080134af0e64878736c287f2ad547cc5c0fb139ee78ea7` |
| 4,049 replay manifest SHA-256 | `fbe51d6e27294b93e021a83a40002820c87992a613dccb2e386ac4bd9db2cfcb` |
| 原始完整核验文档 | `D:\wyq\code\wyq\SC2_暴雪Replay数据与下载方法_最终说明.md` |

## 八、一句话总结

**暴雪官方 4.10.0.75689 Replay 归档、第一批 4,049 个已解压文件及下载脚本都已找回；103,787 个唯一 replay 的历史总量得到确认，但 TvT/ZvZ 子集、完整 DI-Star 工程以及匹配的 SC2/PySC2 解析环境尚未找回。**
