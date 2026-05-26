import argparse
import json
import logging
from pathlib import Path
from typing import Dict, Generator, Optional

import numpy as np

from config import INCOMING_SAMPLES_DIR, LOGGING, SIMULATION, TRACKING
from interfaces.sensor_adapter import JsonFileSensorAdapter
from models.detection_model import DetectionModel
from response.response_engine import ResponseEngine
from sensors.fusion import MultiSensorFusion
from sensors.preprocessing import SensorPreprocessor
from sensors.simulation import MultiSensorSimulator
from tracking.tracker import SortStyleTracker
from train import run as run_train
from utils.bbox import attach_track_ids
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
        if "optical_frame" not in frame:
            frame["optical_frame"] = np.zeros((640, 640, 3), dtype=np.uint8)
        yield frame


def simulate_stream(duration: int, num_objects: int) -> Generator[Dict, None, None]:
    simulator = MultiSensorSimulator()
    yield from simulator.stream(duration_sec=duration, num_objects=num_objects)


def run_monitor(
    use_files: bool,
    duration: int,
    num_objects: int,
    filter_sensitivity: str,
    weights: Optional[str] = None,
    use_pretrained: bool = False,
    allow_trained: bool = True,
    incoming_dir: Optional[Path] = None,
) -> None:
    detector = DetectionModel(
        weights=weights,
        use_pretrained=use_pretrained,
        allow_trained=allow_trained,
    )
    pre = SensorPreprocessor(filter_sensitivity=filter_sensitivity)
    fusion = MultiSensorFusion()
    tracker = SortStyleTracker()
    responder = ResponseEngine()

    if use_files:
        replay_dir = incoming_dir or INCOMING_SAMPLES_DIR
        LOGGER.info("Running monitor mode with file-based input from %s", replay_dir)
        adapter = JsonFileSensorAdapter(load_file_stream(replay_dir))
        stream = adapter.stream()
    else:
        LOGGER.info("Running monitor mode with LIVE simulated sensor stream (default)")
        stream = simulate_stream(duration=duration, num_objects=num_objects)

    previous = None
    processed_frames = 0

    for frame in stream:
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
        responder.save_report(report, frame_id=int(prepared["frame_id"]))
        plot_tracking_and_fusion(track_history, fused, frame_id=int(prepared["frame_id"]))
        processed_frames += 1

    LOGGER.info("Monitoring run complete. Processed %s frames.", processed_frames)
    print(f"Monitoring run complete. Processed {processed_frames} frames.")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="MAVMRF CLI")
    parser.add_argument("--mode", choices=["train", "monitor"], required=True, help="Pipeline mode")
    parser.add_argument(
        "--use-files",
        action="store_true",
        help="Replay JSON frames from incoming_data/samples/ via JsonFileSensorAdapter",
    )
    parser.add_argument(
        "--incoming-dir",
        type=Path,
        default=None,
        help="Directory of JSON frame files for --use-files (default: incoming_data/samples/)",
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
    parser.add_argument(
        "--weights",
        type=str,
        default=None,
        help="Explicit YOLO weights path (detection source: explicit)",
    )
    parser.add_argument(
        "--pretrained",
        action="store_true",
        help="Use pretrained yolov8n.pt when no trained weights are present",
    )
    parser.add_argument(
        "--no-trained",
        action="store_true",
        help="Do not auto-load local runs/mavmrf_yolo_training/weights/best.pt",
    )
    parser.add_argument(
        "--epochs",
        type=int,
        default=None,
        help="Training epochs (train mode)",
    )
    return parser.parse_args()


def main() -> None:
    setup_logging()
    args = parse_args()

    try:
        if args.mode == "train":
            run_train(epochs=args.epochs)
        else:
            run_monitor(
                use_files=args.use_files,
                duration=args.duration,
                num_objects=args.num_objects,
                filter_sensitivity=args.filter_sensitivity,
                weights=args.weights,
                use_pretrained=args.pretrained,
                allow_trained=not args.no_trained,
                incoming_dir=args.incoming_dir,
            )
    except Exception as exc:
        LOGGER.exception("Fatal error during execution: %s", exc)
        raise


if __name__ == "__main__":
    main()
