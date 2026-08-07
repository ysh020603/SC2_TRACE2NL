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

## 看门狗

Cursor loop 每 5 分钟检查一次；完成后自动跑 `analysis/run_pipeline.py --with-phase1` 并生成详细报告。

PID 文件：

- `state/parse.pid`
- `state/watchdog.pid`
