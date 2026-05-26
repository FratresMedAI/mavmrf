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

GitHub Actions workflow: [`.github/workflows/tests.yml`](.github/workflows/tests.yml)

Runs on push/PR to `master`: lint (ruff), pytest, dataset smoke, monitor smoke, file replay.

### First-time Actions enable

If the **Tests** workflow appears in the Actions tab but shows **no runs** after pushing, enable workflows once:

1. Open [Actions](https://github.com/FratresMedAI/mavmrf/actions) for this repo while signed in as the owner.
2. If prompted, click **I understand my workflows, go ahead and enable them**.
3. Confirm **Settings → Actions → General → Actions permissions** is set to **Allow all actions and reusable workflows**.
4. Push any commit to `master` (or use **Run workflow** on the Tests workflow) and verify a green run.

The workflow YAML must stay valid — quote shell commands that contain colons (for example the `grep` assertion on `Detection source: simulation`).

## Pull requests

- Keep changes focused
- Ensure `pytest tests -q` and `ruff check .` pass
- Update README/docs when CLI behavior changes
