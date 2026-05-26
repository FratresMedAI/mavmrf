# Contributing to MAVMRF

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
```

## CI

GitHub Actions workflow: [`.github/workflows/test-suite.yml`](.github/workflows/test-suite.yml)

Runs on push/PR to `master`: lint (ruff), pytest, dataset smoke, monitor smoke, file replay.

If workflows do not run on first clone, enable Actions under **Settings → Actions → General** and allow workflows for this repository.

## Pull requests

- Keep changes focused
- Ensure `pytest tests -q` and `ruff check .` pass
- Update README/docs when CLI behavior changes
