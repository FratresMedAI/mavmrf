# MAVMRF Overview

MAVMRF is a modular, simulation-first Python framework for maritime environmental monitoring and human-in-the-loop decision support.

## Detection modes

| Source | When |
|--------|------|
| `simulation` | Default on fresh clone — uses simulator `optical_detections` |
| `trained` | After synthetic dataset training (`best.pt` exists) |
| `pretrained` | User passes `--pretrained` |
| `explicit` | User passes `--weights PATH` |

Reports record `detection_source` on every frame.

## Core pipeline

- Multi-sensor streams with preprocessing and weighted fusion
- IoU-based detection matching and track ID assignment
- SORT-style tracking with trajectory history
- Rule-based notifications (advisory/notification levels only)
- Structured JSON + Matplotlib outputs

## Getting to trained inference

1. `python scripts/generate_dataset.py --clean`
2. `python main.py --mode train`
3. `python main.py --mode monitor` (auto-loads trained weights)

Use `--no-trained` to force simulation detections even when `best.pt` exists.
