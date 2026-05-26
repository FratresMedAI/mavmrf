# MAVMRF

[![Tests](https://github.com/FratresMedAI/mavmrf/actions/workflows/test-suite.yml/badge.svg)](https://github.com/FratresMedAI/mavmrf/actions/workflows/test-suite.yml)

**Maritime Autonomous Vehicle Monitoring and Response Framework** — a simulation-first Python pipeline for multi-sensor maritime detect, track, and classify.

On a fresh clone, monitor mode uses **simulation detections by default** (no YOLO download). YOLO is opt-in via training, `--pretrained`, or `--weights`.

![Monitor output](docs/screenshots/monitor_frame.png)

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
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
pip install -e .
python main.py --mode monitor --duration 10 --num-objects 8 --no-trained
```

Or run `scripts/demo.ps1` (Windows) / `scripts/demo.sh` (Linux/macOS).

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

## Repository layout

| Path | Description |
|------|-------------|
| [`marmf/`](marmf/) | Core framework |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Pipeline and extension points |
| [`CONTRIBUTING.md`](CONTRIBUTING.md) | Setup, tests, CI |
| [`marmf/tests/`](marmf/tests/) | Pytest suite |

Full CLI reference: [`marmf/README.md`](marmf/README.md).

## Tech stack

Python 3.12 · OpenCV · NumPy · Ultralytics (YOLOv8) · PyTorch · Matplotlib · SciPy · pytest · ruff

## Disclaimer

Portfolio prototype using **simulated sensor data**. Not intended for operational deployment without live sensor integration and validation.

## License

MIT — see [LICENSE](LICENSE).
