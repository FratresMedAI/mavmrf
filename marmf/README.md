# Maritime Autonomous Vehicle Monitoring and Response Framework (MAVMRF)

MAVMRF is a modular, simulation-first COTS Python framework for multi-sensor environmental monitoring and human-in-the-loop decision support in ports, harbors, waterways, and coastal zones.

## Key Capabilities
- Simulated and file-based multi-sensor streams (sonar, acoustic, optical, magnetic).
- End-to-end workflow: Simulation -> Preprocessing -> YOLOv8 Detection -> Sensor Fusion -> SORT Tracking -> Notification Support.
- Classification and object differentiation across marine object classes.
- Operator-facing metrics in reports, including bearing, estimated range, and bearing rate.
- Configurable clutter/false-alarm filtering sensitivity (`low`, `medium`, `high`).
- Automatic JSON reports and Matplotlib visualizations.

## Deployment and Extensibility
MAVMRF is designed as a modular COTS-style prototype extensible to edge computing hardware and integration with fixed or mobile platforms for real-world maritime safety operations in ports, harbors, and coastal zones. The open architecture supports rapid testing and teaming with partners for platform integration or additional capabilities.

## Project Structure

```text
marmf/
├── requirements.txt
├── data.yaml
├── config.py
├── train.py
├── main.py
├── sensors/
│   ├── simulation.py
│   ├── preprocessing.py
│   └── fusion.py
├── models/
│   └── detection_model.py
├── tracking/
│   └── tracker.py
├── response/
│   └── response_engine.py
├── utils/
│   └── visualization.py
├── incoming_data/
├── reports/
├── README.md
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

### 1) Monitor mode (default: LIVE simulated streams)

Run a live simulated monitoring session:

```bash
python main.py --mode monitor
```

Run with custom simulation parameters:

```bash
python main.py --mode monitor --duration 60 --num-objects 12
```

Use optional file-based input from `incoming_data/` (secondary/fallback mode):

```bash
python main.py --mode monitor --use-files
```

Use filter sensitivity tuning for clutter reduction behavior:

```bash
python main.py --mode monitor --filter-sensitivity high
```

### 2) Train mode (YOLOv8)

```bash
python main.py --mode train
```

Or directly:

```bash
python train.py --data data.yaml
```

## Data Classes (`data.yaml`)

The model differentiates these observed marine object categories:

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

- Simulation world size, depth, object density behavior, and noise reduction settings.
- Sensor fusion weights for combined state estimation.
- Detection confidence/IoU thresholds.
- Tracking association and lifecycle parameters.
- Response proximity-based notification thresholds.
- Filter sensitivity controls for clutter/false-alarm handling.

## Output Artifacts

Monitor runs generate outputs in `reports/`:

- `report_frame_XXXXX.json` containing:
  - detections and fused object states,
  - bearing / estimated range / bearing rate fields,
  - contact type differentiation (`biological_like`, `non_biological_like`, `unknown`),
  - track history,
  - change detection (`new`/`moving`) for observed objects,
  - simulated notification/advisory entries.
- `visualization_frame_XXXXX.png` containing:
  - tracked trajectories,
  - fused state points.

## Notes
- This is a simulation-first COTS prototype focused on detect, track, and classify capabilities.
- An open adapter contract is included in `interfaces/sensor_adapter.py` for fixed/mobile integration pathways.
- Open to collaboration with partners providing platform deployment or additional monitoring capabilities.
