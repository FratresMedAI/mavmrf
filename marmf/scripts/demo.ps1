# MAVMRF local demo — clone-and-run (no hosted cloud UI).
# Installs deps, runs simulation-first monitor, writes reports + visualizations.
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

python -m pip install -r requirements.txt
python main.py --mode monitor --no-trained --duration 10 --num-objects 8
Write-Host ""
Write-Host "Local demo complete (no cloud app)."
Write-Host "Reports and plots: $Root\reports\"
