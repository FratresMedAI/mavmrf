# MAVMRF

[![Tests](https://github.com/FratresMedAI/mavmrf/actions/workflows/tests.yml/badge.svg)](https://github.com/FratresMedAI/mavmrf/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

**Maritime Autonomous Vehicle Monitoring and Response Framework** — a simulation-first Python pipeline for multi-sensor maritime detect, track, and classify.

On a fresh clone, monitor mode uses **simulation detections by default** (no YOLO download). YOLO is opt-in via training, `--pretrained`, or `--weights`.

> **Layout note:** Application code lives in the [`marmf/`](marmf/) directory; the installable package name is **`mavmrf`**.

![Monitor output](docs/screenshots/monitor_frame.png)

## Contents

- [Highlights](#highlights)
- [Quick start](#quick-start)
- [Detection modes](#detection-modes)
- [Optional: train on synthetic data](#optional-train-on-synthetic-data)
- [Architecture](#architecture)
- [Documentation](#documentation)
- [Repository layout](#repository-layout)
- [Tech stack](#tech-stack)
- [Contributing](#contributing)
- [Citation](#citation)
- [Disclaimer](#disclaimer)
- [License](#license)

## Highlights

- **Multi-sensor simulation** — sonar, acoustic, optical, and magnetic streams
- **Honest detection modes** — simulation default; YOLO when trained or explicitly requested
- **Fusion & tracking** — IoU-matched object IDs, weighted fusion, SORT-style tracks
- **Operator outputs** — bearing, estimated range, bearing rate, contact typing, change detection
- **File replay** — JSON frames via `JsonFileSensorAdapter` (`incoming_data/samples/`)
- **Automated tests** + GitHub Actions CI

## Quick start

```bash
cd marmf
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux / macOS
# source .venv/bin/activate

pip install -r requirements.txt
pip install -e .
python main.py --mode monitor --duration 10 --num-objects 8 --no-trained
```

Or run `scripts/demo.ps1` (Windows) / `scripts/demo.sh` (Linux/macOS).

From the repo root you can also use:

```bash
pip install -e marmf
```

Reports include `detection_source` (`simulation`, `trained`, `pretrained`, or `explicit`).

## Detection modes

| Mode | How to enable |
|------|----------------|
| `simulation` (default) | No flags; uses simulator optical detections |
| `trained` | After `main.py --mode train`; auto-loads `best.pt` |
| `pretrained` | `--pretrained` (downloads `yolov8n.pt`) |
| `explicit` | `--weights PATH` |

Use `--no-trained` to skip auto-loading local trained weights.

## Optional: train on synthetic data

```bash
cd marmf
python scripts/generate_dataset.py --clean
python main.py --mode train
python main.py --mode monitor
```

## Architecture

See [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for pipeline diagram, module map, and extension points.

```text
Simulated / file streams → preprocess → detect → track → fuse → report
```

## Documentation

| Doc | Description |
|-----|-------------|
| [docs/README.md](docs/README.md) | Documentation index |
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | Pipeline and extension points |
| [docs/SOLUTION_BRIEF.md](docs/SOLUTION_BRIEF.md) | Executive narrative |
| [docs/capability_matrix.md](docs/capability_matrix.md) | Capability → evidence |
| [docs/DEMO_SCRIPT_3_MIN.md](docs/DEMO_SCRIPT_3_MIN.md) | Demo script |
| [CHANGELOG.md](CHANGELOG.md) | Release history |
| [SUPPORT.md](SUPPORT.md) | Where to get help |
| [SECURITY.md](SECURITY.md) | Vulnerability reporting |

Full CLI reference: [`marmf/README.md`](marmf/README.md).

## Repository layout

| Path | Description |
|------|-------------|
| [`marmf/`](marmf/) | Core framework (package name `mavmrf`) |
| [`docs/`](docs/) | Architecture, brief, samples, screenshots |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Setup, tests, CI |
| [`marmf/tests/`](marmf/tests/) | Pytest suite |

## Tech stack

Python 3.12 · OpenCV · NumPy · Ultralytics (YOLOv8) · PyTorch · Matplotlib · SciPy · pytest · ruff

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). By participating, you agree to the [Code of Conduct](CODE_OF_CONDUCT.md).

## Citation

See [CITATION.cff](CITATION.cff). Prefer the “Cite this repository” button on GitHub when available.

## Disclaimer

Portfolio prototype using **simulated sensor data**. Not intended for operational deployment without live sensor integration and validation.

## License

MIT — see [LICENSE](LICENSE).
