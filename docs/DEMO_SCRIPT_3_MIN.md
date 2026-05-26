# 3-Minute Demo Script (MAVMRF)

## 0:00-0:20 | Opening

"This is MAVMRF — Maritime Autonomous Vehicle Monitoring and Response Framework. In this demo I'll show how we detect, track, and classify subsea contacts with operator-ready outputs."

## 0:20-0:50 | Problem + Value

"Operators need reliable detection-to-decision time in cluttered harbor environments. MAVMRF combines multi-sensor ingestion, fusion, tracking, and AI-assisted classification into one pipeline to improve contact awareness and reduce fragmented workflows."

## 0:50-1:35 | Technical Walkthrough

"The runtime pipeline is: ingestion from sonar, acoustic, optical, and magnetic streams; preprocessing with clutter filtering; YOLO-based detection and classification; weighted multi-sensor fusion; SORT-style persistent tracking; and rule-based report generation."

"Each frame outputs key operator fields: bearing, estimated range, bearing rate, class and confidence, track ID and history, and contact type differentiation."

## 1:35-2:10 | Capabilities

"For detection we provide per-contact operator metrics. For tracking we maintain persistent IDs and trajectory continuity. For classification we support eight marine classes plus biological-like versus non-biological-like differentiation. Filter sensitivity can be set to low, medium, or high for clutter control."

## 2:10-2:40 | Evidence

"Runs produce structured JSON reports and time-indexed visualizations in `marmf/reports/`. By default the live simulator drives the pipeline; optionally run with fine-tuned weights via `--weights runs/mavmrf_yolo_training/weights/best.pt` after synthetic training."

## 2:40-3:00 | Close

"MAVMRF is built for rapid integration through an open adapter interface and modular architecture. Next steps are live feed integration, threshold calibration on real datasets, and edge deployment benchmarking."

## 30-Second Q&A Backup

- **Why practical now:** modular COTS-oriented stack with operator-facing outputs today.
- **What's configurable:** filter sensitivity, thresholds, ingest sources, adapter implementations.
- **What scales:** fixed and mobile deployments through the sensor adapter contract.
