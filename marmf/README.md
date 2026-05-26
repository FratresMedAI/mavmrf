# Maritime Autonomous Vehicle Monitoring and Response Framework (MAVMRF)

MAVMRF is a modular, simulation-first Python framework for multi-sensor environmental monitoring and human-in-the-loop decision support.

## Key Capabilities

- Simulated and file-based multi-sensor streams (sonar, acoustic, optical, magnetic)
- End-to-end workflow: Simulation → Preprocessing → Detection → Sensor Fusion → SORT Tracking → Reports
- Eight marine object classes with operator metrics (bearing, range, bearing rate)
- Configurable clutter filtering (`low`, `medium`, `high`)
- JSON reports with `detection_source` metadata

## Detection modes

Fresh clone default: **`simulation`** — no YOLO model download.

Resolution order:

1. `--weights PATH` → `explicit`
2. `runs/mavmrf_yolo_training/weights/best.pt` if present → `trained` (skip with `--no-trained`)
3. `--pretrained` → `pretrained` (`yolov8n.pt`)
4. Otherwise → `simulation`

When YOLO runs, boxes are IoU-matched to simulator detections so sonar/acoustic/magnetic fusion keeps correct `object_id`s.

## Project Structure

```text
marmf/
├── requirements.txt
├── pytest.ini
├── data.yaml
├── config.py
├── train.py
├── main.py
├── scripts/generate_dataset.py
├── utils/bbox.py
├── sensors/
├── models/
├── tracking/
├── response/
├── interfaces/
├── incoming_data/samples/
├── tests/
└── run.bat
```

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
pip install -e .
```

See [`../CONTRIBUTING.md`](../CONTRIBUTING.md) for full dev setup.

## CLI Usage

### Monitor (live simulation)

```bash
python main.py --mode monitor --no-trained
python main.py --mode monitor --duration 10 --num-objects 8
python main.py --mode monitor --pretrained --duration 5
python main.py --mode monitor --weights runs/mavmrf_yolo_training/weights/best.pt
```

### File replay

```bash
python main.py --mode monitor --use-files --no-trained
```

### Train

```bash
python scripts/generate_dataset.py --clean
python main.py --mode train
```

Training validates that dataset images exist before starting.

## Tests

```bash
pytest tests -q
ruff check .
```

## Output Artifacts

- `report_frame_XXXXX.json` — fused objects, tracks, notifications, `detection_source`
- `visualization_frame_XXXXX.png` — track trajectories and fused positions

See [`OVERVIEW.md`](OVERVIEW.md) for a concise technical summary.
