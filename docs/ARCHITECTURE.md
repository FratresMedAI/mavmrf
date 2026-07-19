# MAVMRF Architecture

## Pipeline

```text
Input stream (simulation or file replay)
        │
        ▼
  SensorPreprocessor ──► change detection, normalization
        │
        ▼
  DetectionModel ──► simulation | trained | pretrained | explicit
        │              (YOLO boxes IoU-matched to stream detections)
        ▼
  SortStyleTracker ──► persistent track IDs
        │
        ▼
  MultiSensorFusion ──► sonar + acoustic + optical + magnetic
        │
        ▼
  ResponseEngine ──► JSON reports + Matplotlib plots
```

## Detection modes

| Source | When |
|--------|------|
| `simulation` | Default — no YOLO load; uses stream `optical_detections` |
| `trained` | `runs/mavmrf_yolo_training/weights/best.pt` exists |
| `pretrained` | User passes `--pretrained` |
| `explicit` | User passes `--weights PATH` |

Reports record `detection_source` on every frame.

## Module map

| Module | Role |
|--------|------|
| [`marmf/sensors/simulation.py`](../marmf/sensors/simulation.py) | Multi-sensor stream generator |
| [`marmf/sensors/preprocessing.py`](../marmf/sensors/preprocessing.py) | Normalization and change detection |
| [`marmf/models/detection_model.py`](../marmf/models/detection_model.py) | YOLO inference + simulation fallback |
| [`marmf/utils/bbox.py`](../marmf/utils/bbox.py) | IoU matching for IDs and track attach |
| [`marmf/tracking/tracker.py`](../marmf/tracking/tracker.py) | SORT-style tracker |
| [`marmf/sensors/fusion.py`](../marmf/sensors/fusion.py) | Weighted multi-sensor fusion |
| [`marmf/response/response_engine.py`](../marmf/response/response_engine.py) | Operator metrics and notifications |
| [`marmf/interfaces/sensor_adapter.py`](../marmf/interfaces/sensor_adapter.py) | Integration contract for external feeds |

## Place in the Fratres X stack

MAVMRF is a **clone-and-run** open-source thread under [Fratres X AI](https://fratres-x.com): physics-first simulation, honest maturity labels, and reviewable fusion outputs.

It sits next to Fratres defensive-sensing / contested-autonomy prototypes (multi-modal streams, conservative fusion, operator-facing audit artifacts) without claiming a fielded maritime product. Use it as a reproducible lab for detect → track → fuse → report before wiring real adapters.

## Extension points

- **Live sensors:** implement `SensorAdapter.stream()` yielding frames with `sonar`, `acoustic`, `magnetic`, `optical_frame` or `optical_detections`
- **Training data:** `scripts/generate_dataset.py` exports YOLO labels from the simulator
- **File replay:** JSON under `incoming_data/samples/`; optional `optical_image` sidecar JPG
- **Gates:** `scripts/benchmark.py` writes seeded metrics under [`docs/benchmarks/`](benchmarks/)

## Outputs

Each monitor run writes to `marmf/reports/`:

- `report_frame_XXXXX.json` — fused objects, tracks, notifications, `detection_source`
- `visualization_frame_XXXXX.png` — trajectories and fused positions
