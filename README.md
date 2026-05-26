# MAVMRF

[![CI](https://github.com/FratresMedAI/mavmrf/actions/workflows/ci.yml/badge.svg)](https://github.com/FratresMedAI/mavmrf/actions/workflows/ci.yml)

**Maritime Autonomous Vehicle Monitoring and Response Framework** — a simulation-first Python pipeline for multi-sensor maritime detect, track, and classify.

The default demo runs on a **live simulated sensor stream**. YOLOv8 inference is enabled with pinned dependencies; simulation-provided detections remain as fallback when inference returns no boxes.

![Monitor output](docs/screenshots/monitor_frame.png)

## Highlights

- **Multi-sensor simulation** — sonar, acoustic, optical, and magnetic streams
- **YOLOv8 detection** — pretrained `yolov8n.pt` by default; optional fine-tuning on synthetic data
- **Fusion & tracking** — weighted multi-sensor fusion and SORT-style persistent tracks
- **Operator outputs** — bearing, estimated range, bearing rate, contact typing, change detection
- **File replay** — JSON frames via `JsonFileSensorAdapter` (`incoming_data/samples/`)
- **Configurable clutter filtering** — `--filter-sensitivity low|medium|high`

## Quick start

```bash
cd marmf
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
python main.py --mode monitor --duration 30 --num-objects 8
```

Reports and plots are written to `marmf/reports/` (gitignored locally).

## Optional: train on synthetic data

```bash
cd marmf
python scripts/generate_dataset.py --clean
python main.py --mode train
python main.py --mode monitor --weights runs/mavmrf_yolo_training/weights/best.pt
```

## Architecture

```text
Simulated / file streams
        │
        ▼
  Preprocessing ──► YOLOv8 detection
        │                    │
        └──────► Sensor fusion ◄── SORT tracking
                        │
                        ▼
              Response engine + JSON / PNG reports
```

## Repository layout

| Path | Description |
|------|-------------|
| [`marmf/`](marmf/) | Core framework — sensors, models, tracking, response |
| [`marmf/scripts/generate_dataset.py`](marmf/scripts/generate_dataset.py) | Synthetic YOLO dataset generator |
| [`marmf/tests/`](marmf/tests/) | Pytest smoke tests |
| [`docs/`](docs/) | Solution brief, capability matrix, demo script |

Full CLI reference: [`marmf/README.md`](marmf/README.md).

## Tech stack

Python 3.12 · OpenCV · NumPy · Ultralytics (YOLOv8) · PyTorch · Matplotlib · SciPy · pytest

## Disclaimer

Portfolio prototype using **simulated sensor data**. Not intended for operational deployment without live sensor integration and validation.

## License

MIT — see [LICENSE](LICENSE).
