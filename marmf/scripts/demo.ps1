$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

python -m pip install -r requirements.txt
python main.py --mode monitor --no-trained --duration 10 --num-objects 8
Write-Host "Reports: $Root\reports\"
