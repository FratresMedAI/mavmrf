# MAVMRF Capability Matrix

## Scope

Maps MAVMRF capabilities to detect, track, and classify requirements.

## Requirement Mapping

- Detection information for operator decision support
  - Status: Implemented
  - Evidence: `response/response_engine.py` adds `bearing`, `estimated_range`, and `bearing_rate`.

- Confident track estimation using one or more sensors
  - Status: Implemented
  - Evidence: `tracking/tracker.py` SORT-style persistence; IoU track attach in `utils/bbox.py`.

- Classification/discrimination of subsea object types
  - Status: Implemented
  - Evidence: `models/detection_model.py`, `data.yaml`, report class outputs.

- Multi-sensor fusion with matched object IDs
  - Status: Implemented
  - Evidence: `utils/bbox.match_detections` + `sensors/fusion.py`.

- Clutter/false-alarm reduction with sensitivity control
  - Status: Implemented
  - Evidence: `sensors/preprocessing.py`, `--filter-sensitivity`.

- Open architecture for fixed/mobile integration
  - Status: Implemented (prototype)
  - Evidence: `interfaces/sensor_adapter.py`, `--use-files` replay.

## Runtime Validation

```bash
pytest tests -q
python main.py --mode monitor --duration 2 --num-objects 3 --no-trained
python main.py --mode monitor --use-files --no-trained
```

Expected: reports include `detection_source: simulation` on fresh clone; CI green on GitHub.
