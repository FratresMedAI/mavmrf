# Contributing to MAVMRF

Thanks for your interest. Please read the [Code of Conduct](CODE_OF_CONDUCT.md) and [SUPPORT.md](SUPPORT.md). Report security issues via [SECURITY.md](SECURITY.md), not public issues.

## Setup

```bash
cd marmf
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -e .
```

## Run tests

```bash
cd marmf
pytest tests -q
ruff check .
```

From repo root:

```bash
pip install -e marmf
pytest marmf/tests -q
```

## Run the demo

```bash
cd marmf
python main.py --mode monitor --no-trained --duration 10
# or: scripts/demo.ps1  /  scripts/demo.sh
```

## Train on synthetic data

```bash
cd marmf
python scripts/generate_dataset.py --clean
python main.py --mode train
python main.py --mode monitor
```

## Regenerate docs fixtures

```bash
cd marmf
python main.py --mode monitor --no-trained --duration 2 --num-objects 3
cp reports/report_frame_00000.json ../docs/samples/report_frame_00005.json
cp reports/visualization_frame_00000.png ../docs/screenshots/monitor_frame.png

# README GIF (needs Pillow from requirements-dev.txt)
python main.py --mode monitor --no-trained --duration 3 --num-objects 4
python scripts/make_demo_gif.py

# Seeded benchmark table
python scripts/benchmark.py --seed 42 --duration 5 --num-objects 6
```

## CI

GitHub Actions workflow: [`.github/workflows/tests.yml`](.github/workflows/tests.yml)

Runs on push/PR to `master`: lint (ruff), pytest, dataset smoke, monitor smoke, file replay.

If a new fork shows workflows disabled, enable Actions under **Settings → Actions → General**. Quote shell commands that contain colons in workflow YAML (for example the `grep` assertion on `Detection source: simulation`).

## Pull requests

- Keep changes focused
- Ensure `pytest tests -q` and `ruff check .` pass
- Update README/docs when CLI behavior changes
- Use the PR template checklist
