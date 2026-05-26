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

echo [MAVMRF] Launching monitor mode (simulation detections, 10s)...
python main.py --mode monitor --no-trained --duration 10 --num-objects 8

echo [MAVMRF] Done. Reports written to reports\
endlocal
