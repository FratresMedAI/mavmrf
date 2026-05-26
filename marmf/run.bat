@echo off
setlocal

echo [MAVMRF] Starting Maritime Autonomous Vehicle Monitoring and Response Framework...

if not exist ".venv" (
    echo [MAVMRF] Creating virtual environment...
    python -m venv .venv
)

call .venv\Scripts\activate

echo [MAVMRF] Installing/updating dependencies...
pip install -r requirements.txt

echo [MAVMRF] Launching monitor mode with LIVE simulated stream (default)...
python main.py --mode monitor

echo [MAVMRF] Done.
endlocal
