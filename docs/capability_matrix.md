# MAVMRF Capability Matrix

## Scope

Maps MAVMRF capabilities to detect, track, and classify requirements.

## Requirement Mapping

- Detection information for operator decision support
  - Status: Implemented
  - Evidence: `response/response_engine.py` adds `bearing`, `estimated_range`, and `bearing_rate` in each fused object report entry.

- Confident track estimation using one or more sensors
  - Status: Implemented
  - Evidence: `tracking/tracker.py` SORT-style track persistence with per-track history.

- Classification/discrimination of subsea object types
  - Status: Implemented
  - Evidence: `models/detection_model.py`, `data.yaml` 8 classes, and class outputs in monitoring reports.

- Differentiation support (biological-like vs non-biological-like)
  - Status: Implemented (demo heuristic)
  - Evidence: `response/response_engine.py` includes `contact_type` field (`biological_like`, `non_biological_like`, `unknown`).

- Clutter/false-alarm reduction with sensitivity control
  - Status: Implemented
  - Evidence: `sensors/preprocessing.py` + `config.py` + `main.py --filter-sensitivity` (`low`, `medium`, `high`).

- Multi-sensor support (sonar/acoustic/optical/magnetic)
  - Status: Implemented
  - Evidence: `sensors/simulation.py` live stream generation + fusion pipeline in `sensors/fusion.py`.

- Open architecture for fixed/mobile integration paths
  - Status: Implemented (prototype adapter contract)
  - Evidence: `interfaces/sensor_adapter.py` (`SensorAdapter`, `JsonFileSensorAdapter`).

## Runtime Validation

- Command: `pytest tests -q`
- Monitor: `python main.py --mode monitor --duration 2 --num-objects 3 --filter-sensitivity high`
- File replay: `python main.py --mode monitor --use-files`
- Optional trained weights: `python main.py --mode monitor --weights runs/mavmrf_yolo_training/weights/best.pt`
- Result: Successful end-to-end runs with generated reports and visualizations.
