import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_main_monitor_subprocess():
    result = subprocess.run(
        [
            sys.executable,
            "main.py",
            "--mode",
            "monitor",
            "--duration",
            "1",
            "--num-objects",
            "2",
            "--no-trained",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert "Detection source: simulation" in result.stdout + result.stderr
