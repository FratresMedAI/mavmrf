# 3-Minute Demo Script (MAVMRF - REEF Component 1)

## 0:00-0:20 | Opening
"Thank you for the opportunity. This is MAVMRF, a modular maritime monitoring framework aligned to REEF Component 1. In this short demo, I’ll show how we detect, track, and classify subsea contacts with operator-ready outputs."

## 0:20-0:50 | Problem + Value
"Operators need reliable detection-to-decision time in cluttered harbor environments. MAVMRF combines multi-sensor ingestion, fusion, tracking, and AI-assisted classification into one pipeline to improve contact awareness and reduce fragmented workflows."

## 0:50-1:35 | Technical Walkthrough
"The runtime pipeline is: ingestion from sonar, acoustic, optical, and magnetic streams; preprocessing with clutter filtering; YOLO-based detection/classification; weighted multi-sensor fusion; SORT-style persistent tracking; and rule-based report generation."

"Each frame outputs key operator fields: bearing, estimated range, bearing rate, class/confidence, track ID/history, and contact type differentiation."

## 1:35-2:10 | Component 1 Mapping
"For Detect, we provide per-contact operator metrics. For Track, we maintain persistent IDs and trajectory continuity. For Classify, we support eight marine classes plus biological-like versus non-biological-like differentiation. Filter sensitivity can be toggled low/medium/high for clutter control."

## 2:10-2:40 | Evidence
"The submission package includes structured JSON reports and time-indexed visualizations at early, middle, and late frames to show track development and fused state consistency over time."

## 2:40-3:00 | Transition Path / Close
"MAVMRF is built for rapid integration through an open adapter interface and modular architecture. Near-term next steps are live feed integration, threshold calibration with representative datasets, and edge deployment benchmarking."

"Happy to walk through architecture and performance details next."

## 30-Second Q&A Backup
- Why this is practical now: modular COTS-oriented stack, already producing operator-facing outputs.
- What is configurable: filter sensitivity, thresholds, ingest sources, and adapter implementations.
- What scales: fixed/mobile deployments through adapter-based integration.
