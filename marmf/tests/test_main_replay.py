import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_main_file_replay_subprocess():
    result = subprocess.run(
        [sys.executable, "main.py", "--mode", "monitor", "--use-files", "--no-trained"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
