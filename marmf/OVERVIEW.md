# MAVMRF Overview

MAVMRF is a modular, simulation-first COTS Python framework for maritime environmental monitoring and human-in-the-loop decision support.

## Core Technical Approach

- Multi-sensor streams (sonar, acoustic, optical, magnetic) with preprocessing and weighted fusion
- YOLOv8 detection and classification for marine object categories (`large_uuv`, `small_rov`, `semi_submersible`, `research_glider`, `commercial_drone`, `unidentified_object`, `surface_buoy`, `debris_cluster`)
- SORT-style multi-object tracking with trajectory history and change detection
- Rule-based notification/advisory output with structured JSON reporting
- Operator-facing metrics: bearing, estimated range, and bearing rate
- Configurable clutter/false-alarm filter sensitivity (`low`, `medium`, `high`)

## Integration

- Open adapter contract in `interfaces/sensor_adapter.py` for fixed/mobile platform integration
- Simulation-first pipeline for rapid testing before live sensor onboarding
- Modular architecture suitable for edge compute deployments

## Path Forward

Live sensor adapters, calibration on representative datasets, and sustained edge runtime benchmarking. Example outputs are generated under `reports/` when you run monitor mode.
