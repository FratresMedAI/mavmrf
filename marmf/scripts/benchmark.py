"""Seeded pipeline benchmark — reproducible gates for portfolio validation."""

from __future__ import annotations

import argparse
import json
import sys
import time
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from config import TRACKING  # noqa: E402
from models.detection_model import DetectionModel  # noqa: E402
from response.response_engine import ResponseEngine  # noqa: E402
from sensors.fusion import MultiSensorFusion  # noqa: E402
from sensors.preprocessing import SensorPreprocessor  # noqa: E402
from sensors.simulation import MultiSensorSimulator  # noqa: E402
from tracking.tracker import SortStyleTracker  # noqa: E402
from utils.bbox import attach_track_ids  # noqa: E402

DEFAULT_OUT_DIR = PROJECT_ROOT.parent / "docs" / "benchmarks"


def run_benchmark(
    seed: int,
    duration_sec: int,
    num_objects: int,
    filter_sensitivity: str,
) -> dict:
    detector = DetectionModel(weights=None, use_pretrained=False, allow_trained=False)
    pre = SensorPreprocessor(filter_sensitivity=filter_sensitivity)
    fusion = MultiSensorFusion()
    tracker = SortStyleTracker()
    responder = ResponseEngine()
    sim = MultiSensorSimulator(seed=seed)

    previous = None
    frames = 0
    contact_types: Counter[str] = Counter()
    total_fused = 0
    notifications = 0
    track_ids: set[int] = set()
    t0 = time.perf_counter()

    for frame in sim.stream(duration_sec=duration_sec, num_objects=num_objects):
        prepared = pre.preprocess(frame, previous_frame=previous)
        previous = frame
        detections = detector.infer(
            prepared["optical_frame"],
            fallback_detections=prepared.get("optical_detections", []),
        )
        detections = tracker.update(detections, timestamp=prepared["timestamp"])
        fused = fusion.fuse(prepared, detections)
        attach_track_ids(fused, detections, threshold=TRACKING["iou_match_threshold"])
        track_history = tracker.export_track_history()
        report = responder.evaluate(
            timestamp=prepared["timestamp"],
            fused_objects=fused,
            track_history=track_history,
            changes=prepared.get("changes", []),
            detection_source=detector.source,
        )
        frames += 1
        total_fused += len(fused)
        for obj in fused:
            contact_types[str(obj.get("contact_type", "unknown"))] += 1
            tid = obj.get("track_id")
            if tid is not None:
                track_ids.add(int(tid))
        notifications += len(report.get("notifications", []))

    elapsed = time.perf_counter() - t0
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "seed": seed,
        "duration_sec": duration_sec,
        "num_objects": num_objects,
        "filter_sensitivity": filter_sensitivity,
        "detection_source": detector.source,
        "frames_processed": frames,
        "elapsed_sec": round(elapsed, 3),
        "frames_per_sec": round(frames / elapsed, 2) if elapsed > 0 else 0.0,
        "unique_track_ids": len(track_ids),
        "total_fused_object_observations": total_fused,
        "mean_fused_per_frame": round(total_fused / frames, 2) if frames else 0.0,
        "notifications_total": notifications,
        "contact_type_counts": dict(contact_types),
    }


def write_outputs(result: dict, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    json_path = out_dir / "seeded_run.json"
    md_path = out_dir / "README.md"

    json_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    contacts = result["contact_type_counts"]
    contact_rows = "\n".join(f"| `{k}` | {v} |" for k, v in sorted(contacts.items())) or "| — | 0 |"

    md = f"""# Seeded benchmark

Reproducible simulation-only gate. Regenerate with:

```bash
cd marmf
python scripts/benchmark.py --seed {result["seed"]} --duration {result["duration_sec"]} --num-objects {result["num_objects"]}
```

## Conditions

| Parameter | Value |
|-----------|-------|
| Seed | `{result["seed"]}` |
| Duration (sec) | {result["duration_sec"]} |
| Simulated objects | {result["num_objects"]} |
| Filter sensitivity | `{result["filter_sensitivity"]}` |
| Detection source | `{result["detection_source"]}` |
| Generated (UTC) | {result["generated_at_utc"]} |

## Results

| Metric | Value |
|--------|-------|
| Frames processed | {result["frames_processed"]} |
| Elapsed (sec) | {result["elapsed_sec"]} |
| Throughput (frames/sec) | {result["frames_per_sec"]} |
| Unique track IDs | {result["unique_track_ids"]} |
| Total fused observations | {result["total_fused_object_observations"]} |
| Mean fused objects / frame | {result["mean_fused_per_frame"]} |
| Notifications (total) | {result["notifications_total"]} |

### Contact types (observation counts)

| Contact type | Count |
|--------------|-------|
{contact_rows}

Machine-readable copy: [`seeded_run.json`](seeded_run.json).

These numbers are **simulation gates**, not field performance claims.
"""
    md_path.write_text(md, encoding="utf-8")
    print(f"Wrote {json_path}")
    print(f"Wrote {md_path}")
    print(json.dumps({k: result[k] for k in ("frames_processed", "unique_track_ids", "frames_per_sec", "detection_source")}, indent=2))


def main() -> None:
    parser = argparse.ArgumentParser(description="Run seeded MAVMRF simulation benchmark")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--duration", type=int, default=5)
    parser.add_argument("--num-objects", type=int, default=6)
    parser.add_argument("--filter-sensitivity", default="medium", choices=["low", "medium", "high"])
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT_DIR)
    args = parser.parse_args()

    result = run_benchmark(
        seed=args.seed,
        duration_sec=args.duration,
        num_objects=args.num_objects,
        filter_sensitivity=args.filter_sensitivity,
    )
    write_outputs(result, args.out_dir)


if __name__ == "__main__":
    main()
