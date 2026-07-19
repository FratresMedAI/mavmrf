#!/usr/bin/env bash
# MAVMRF local demo — clone-and-run (no hosted cloud UI).
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

python -m pip install -r requirements.txt
python main.py --mode monitor --no-trained --duration 10 --num-objects 8
echo ""
echo "Local demo complete (no cloud app)."
echo "Reports and plots: $ROOT/reports/"
