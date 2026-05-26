# MAVMRF Overview

MAVMRF is a modular, simulation-first COTS Python framework for maritime environmental monitoring and human-in-the-loop decision support.

## Core Technical Approach

- Multi-sensor streams (sonar, acoustic, optical, magnetic) with preprocessing and weighted fusion
- YOLOv8 detection with simulation fallback detections
- SORT-style multi-object tracking with trajectory history and change detection
- Rule-based notification/advisory output with structured JSON reporting
- Operator-facing metrics: bearing, estimated range, and bearing rate
- Configurable clutter/false-alarm filter sensitivity (`low`, `medium`, `high`)

## Getting to Trained Inference

1. Generate synthetic labels from the simulator:
   `python scripts/generate_dataset.py --clean`
2. Train:
   `python main.py --mode train`
3. Run monitor with fine-tuned weights:
   `python main.py --mode monitor --weights runs/mavmrf_yolo_training/weights/best.pt`

## Integration

- Open adapter contract in `interfaces/sensor_adapter.py` for fixed/mobile platform integration
- File replay via `JsonFileSensorAdapter` and JSON frames in `incoming_data/samples/`
- Modular architecture suitable for edge compute deployments

## Path Forward

Live sensor adapters, calibration on representative datasets, and sustained edge runtime benchmarking.
