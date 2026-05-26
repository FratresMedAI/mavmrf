# Project REEF — MAVMRF

**Maritime Autonomous Vehicle Monitoring and Response Framework (MAVMRF)** — a simulation-first Python pipeline for multi-sensor maritime detect, track, and classify, developed in alignment with the DIU Robotic Exclusion & Engagement Framework (REEF) Component 1.

Portfolio highlight: end-to-end computer-vision and sensor-fusion workflow from synthetic multi-modal streams through YOLOv8 detection, SORT tracking, operator-facing JSON reports, and Matplotlib visualizations.

## Highlights

- **Multi-sensor simulation** — sonar, acoustic, optical, and magnetic streams (live sim or file replay)
- **Detection & classification** — YOLOv8 with eight marine object classes (`data.yaml`)
- **Fusion & tracking** — weighted multi-sensor fusion and SORT-style persistent tracks
- **Operator outputs** — bearing, estimated range, bearing rate, contact typing, change detection
- **Extensible integration** — `sensor_adapter.py` contract for fixed/mobile platform feeds
- **Configurable clutter filtering** — `--filter-sensitivity low|medium|high`

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

## Quick start

```bash
cd marmf
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
python main.py --mode monitor --duration 30 --num-objects 8
```

Outputs are written under `marmf/reports/` (gitignored; generated locally).

Training:

```bash
python main.py --mode train
```

Full CLI options, class list, and configuration notes: [`marmf/README.md`](marmf/README.md).

## Repository layout

| Path | Description |
|------|-------------|
| [`marmf/`](marmf/) | Core framework — sensors, models, tracking, response |
| [`docs/`](docs/) | Solution brief, compliance matrix, demo script, sample report |
| [`DIU_Submission_Ready/`](DIU_Submission_Ready/) | Original submission packet materials (markdown/HTML) |

## Tech stack

Python 3 · OpenCV · NumPy · Ultralytics (YOLOv8) · Matplotlib · SciPy · scikit-learn

## Sample output

A representative monitor frame report is included at [`docs/samples/report_frame_00005.json`](docs/samples/report_frame_00005.json). Run the monitor locally to regenerate full report and visualization series.

## Disclaimer

This repository is a **portfolio / prototype** implementation using simulated sensor data. It is not affiliated with or endorsed by the U.S. government or DIU. REEF program naming is used for technical context only.

## License

MIT — see [LICENSE](LICENSE).
