#!/usr/bin/env bash
set -euo pipefail
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

export PIP_INDEX_URL="${PIP_INDEX_URL:-https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple}"
export PIP_DEFAULT_TIMEOUT="${PIP_DEFAULT_TIMEOUT:-120}"

python -m pip install --upgrade pip setuptools wheel
python -m pip install -e ".[dev]"
python - <<'PY'
import sc2reader
print("sc2reader:", sc2reader.__version__)
PY
python -m pip freeze > requirements.lock.txt
python --version > environment.txt
uname -a >> environment.txt
echo "Bootstrap complete."
