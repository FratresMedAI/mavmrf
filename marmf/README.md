# Maritime Autonomous Vehicle Monitoring and Response Framework (MAVMRF)

MAVMRF is a modular, simulation-first Python framework for multi-sensor environmental monitoring and human-in-the-loop decision support in ports, harbors, waterways, and coastal zones.

## Key Capabilities

- Simulated and file-based multi-sensor streams (sonar, acoustic, optical, magnetic)
- End-to-end workflow: Simulation → Preprocessing → YOLOv8 Detection → Sensor Fusion → SORT Tracking → Notification Support
- Classification across eight marine object classes
- Operator-facing metrics: bearing, estimated range, bearing rate
- Configurable clutter/false-alarm filtering (`low`, `medium`, `high`)
- JSON reports and Matplotlib visualizations

## Project Structure

```text
marmf/
├── requirements.txt
├── pytest.ini
├── data.yaml
├── config.py
├── train.py
├── main.py
├── scripts/
│   └── generate_dataset.py
├── sensors/
├── models/
├── tracking/
├── response/
├── utils/
├── interfaces/
├── incoming_data/
│   └── samples/          # committed JSON replay fixtures
├── tests/
├── reports/              # generated locally
└── run.bat
```

## Installation

1. Open a terminal in `marmf/`.
2. Create a virtual environment (recommended):
   - `python -m venv .venv`
   - `.venv\Scripts\activate`
3. Install dependencies:
   - `pip install -r requirements.txt`

## CLI Usage

### Monitor mode (default: live simulated stream)

```bash
python main.py --mode monitor
python main.py --mode monitor --duration 60 --num-objects 12
python main.py --mode monitor --filter-sensitivity high
```

### Weights resolution

Detection model path is resolved in order:

1. `--weights PATH` if provided
2. `runs/mavmrf_yolo_training/weights/best.pt` if present
3. `yolov8n.pt` (pretrained)

```bash
python main.py --mode monitor --weights runs/mavmrf_yolo_training/weights/best.pt
```

If YOLO inference fails or returns no boxes, simulation-provided detections are used as fallback.

### File replay (JsonFileSensorAdapter)

```bash
python main.py --mode monitor --use-files
python main.py --mode monitor --use-files --incoming-dir incoming_data/samples
```

Sample frames are included under `incoming_data/samples/`.

### Train mode

Generate a synthetic dataset, then train:

```bash
python scripts/generate_dataset.py --clean
python main.py --mode train
python train.py --data data.yaml --epochs 10
```

`python main.py --mode train` calls the same training entrypoint without argparse conflicts.

## Data Classes (`data.yaml`)

1. `large_uuv`
2. `small_rov`
3. `semi_submersible`
4. `research_glider`
5. `commercial_drone`
6. `unidentified_object`
7. `surface_buoy`
8. `debris_cluster`

## Configuration

Tune parameters in `config.py`:

- Simulation world size, object density, noise, filter sensitivity
- Sensor fusion weights
- Detection confidence/IoU thresholds
- Tracking association parameters
- Response proximity thresholds

## Output Artifacts

Monitor runs generate outputs in `reports/`:

- `report_frame_XXXXX.json` — detections, fused states, bearing/range/bearing_rate, tracks, notifications
- `visualization_frame_XXXXX.png` — track trajectories and fused positions

## Tests

```bash
pytest tests -q
```

## Notes

- Simulation-first prototype focused on detect, track, and classify pipeline architecture
- `interfaces/sensor_adapter.py` defines the integration contract for fixed/mobile feeds
- See [`OVERVIEW.md`](OVERVIEW.md) for a concise technical summary
