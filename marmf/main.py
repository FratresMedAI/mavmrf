import argparse
import json
import logging
from pathlib import Path
from typing import Dict, Generator, List, Optional

import numpy as np

from config import INCOMING_DATA_DIR, LOGGING, PROJECT_ROOT, SIMULATION
from models.detection_model import DetectionModel
from response.response_engine import ResponseEngine
from sensors.fusion import MultiSensorFusion
from sensors.preprocessing import SensorPreprocessor
from sensors.simulation import MultiSensorSimulator
from tracking.tracker import SortStyleTracker
from utils.visualization import plot_tracking_and_fusion

LOGGER = logging.getLogger(__name__)


def setup_logging() -> None:
    logging.basicConfig(level=LOGGING["level"], format=LOGGING["format"])


def load_file_stream(incoming_dir: Path) -> Generator[Dict, None, None]:
    files = sorted(incoming_dir.glob("*.json"))
    if not files:
        raise FileNotFoundError(
            f"No .json frame files found in {incoming_dir}. Use default simulated stream or add files."
        )

    for idx, file in enumerate(files):
        with file.open("r", encoding="utf-8") as f:
            frame = json.load(f)
        frame.setdefault("frame_id", idx)
        frame.setdefault("timestamp", float(idx))
        frame.setdefault("optical_frame", np.zeros((640, 640, 3), dtype=np.uint8))
        yield frame


def simulate_stream(duration: int, num_objects: int) -> Generator[Dict, None, None]:
    simulator = MultiSensorSimulator()
    yield from simulator.stream(duration_sec=duration, num_objects=num_objects)


def run_monitor(use_files: bool, duration: int, num_objects: int, filter_sensitivity: str) -> None:
    detector = DetectionModel()
    pre = SensorPreprocessor(filter_sensitivity=filter_sensitivity)
    fusion = MultiSensorFusion()
    tracker = SortStyleTracker()
    responder = ResponseEngine()

    if use_files:
        LOGGER.info("Running monitor mode with file-based input from incoming_data/")
        stream = load_file_stream(INCOMING_DATA_DIR)
    else:
        LOGGER.info("Running monitor mode with LIVE simulated sensor stream (default)")
        stream = simulate_stream(duration=duration, num_objects=num_objects)

    previous = None
    processed_frames = 0
    last_stable_tracks = 0
    total_notifications = 0

    for frame in stream:
        prepared = pre.preprocess(frame, previous_frame=previous)
        previous = frame

        detections = detector.infer(prepared["optical_frame"], fallback_detections=prepared.get("optical_detections", []))
        detections = tracker.update(detections, timestamp=prepared["timestamp"])
        fused = fusion.fuse(prepared, detections)

        # ensure fused objects carry track id by nearest bbox match with detections
        for obj in fused:
            for det in detections:
                if obj.get("bbox") == det.get("bbox"):
                    obj["track_id"] = det.get("track_id")
                    break

        track_history = tracker.export_track_history()
        report = responder.evaluate(
            timestamp=prepared["timestamp"],
            fused_objects=fused,
            track_history=track_history,
            changes=prepared.get("changes", []),
        )
        last_stable_tracks = len(track_history)
        total_notifications += len(report.get("notifications", []))
        responder.save_report(report, frame_id=int(prepared["frame_id"]))
        plot_tracking_and_fusion(track_history, fused, frame_id=int(prepared["frame_id"]))
        processed_frames += 1

    LOGGER.info("Monitoring run complete. Processed %s frames.", processed_frames)
    print(
        f"Monitoring run complete. Processed {processed_frames} frames with stable tracks and notifications for safe maritime operations support."
    )


def run_train() -> None:
    import train as train_entry

    train_entry.main()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="MAVMRF CLI")
    parser.add_argument("--mode", choices=["train", "monitor"], required=True, help="Pipeline mode")
    parser.add_argument(
        "--use-files",
        action="store_true",
        help="Use file-based input from incoming_data/ instead of default live simulation stream",
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=SIMULATION["default_duration_sec"],
        help="Simulation duration in seconds (monitor mode)",
    )
    parser.add_argument(
        "--num-objects",
        type=int,
        default=SIMULATION["default_num_objects"],
        help="Number of simulated objects (monitor mode)",
    )
    parser.add_argument(
        "--filter-sensitivity",
        choices=["low", "medium", "high"],
        default=SIMULATION.get("default_filter_sensitivity", "medium"),
        help="Clutter filtering sensitivity for change detection and monitoring outputs",
    )
    return parser.parse_args()


def main() -> None:
    setup_logging()
    args = parse_args()

    try:
        if args.mode == "train":
            run_train()
        else:
            run_monitor(
                use_files=args.use_files,
                duration=args.duration,
                num_objects=args.num_objects,
                filter_sensitivity=args.filter_sensitivity,
            )
    except Exception as exc:
        LOGGER.exception("Fatal error during execution: %s", exc)
        raise


if __name__ == "__main__":
    main()
