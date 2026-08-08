# 全量 action JSON 解析

## 启动

```bash
conda activate sc2replay
nohup python -u analysis/full_parse/run_full_parse.py \
  --workers 48 --batch-size 2000 \
  > analysis/full_parse/logs/master.log 2>&1 &
```

支持断点续跑：已存在且带 `source_file` 的 JSON 会跳过。

## 状态

```bash
python analysis/full_parse/check_status.py
cat analysis/full_parse/state/status.json
```

## 后续分析

解析完成后运行当前 V2 流水线：

```bash
python analysis/skill_mining_v2/run_pipeline.py --fresh --full-windows
```

PID 文件：

- `state/parse.pid`
- `state/watchdog.pid`
