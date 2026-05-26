#!/usr/bin/env python3
"""Generate a synthetic YOLO dataset from the MAVMRF multi-sensor simulator."""

from __future__ import annotations

import argparse
import logging
import shutil
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import cv2

from config import INCOMING_DATA_DIR, LOGGING
from sensors.simulation import MultiSensorSimulator

LOGGER = logging.getLogger(__name__)


def bbox_to_yolo_line(bbox: list[float], class_id: int, img_w: int, img_h: int) -> str:
    x1, y1, x2, y2 = bbox
    cx = ((x1 + x2) / 2.0) / img_w
    cy = ((y1 + y2) / 2.0) / img_h
    w = (x2 - x1) / img_w
    h = (y2 - y1) / img_h
    return f"{class_id} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f}"


def export_split(
    output_dir: Path,
    split: str,
    num_frames: int,
    num_objects: int,
    seed_offset: int,
) -> Counter:
    images_dir = output_dir / "images" / split
    labels_dir = output_dir / "labels" / split
    images_dir.mkdir(parents=True, exist_ok=True)
    labels_dir.mkdir(parents=True, exist_ok=True)

    class_counts: Counter = Counter()
    sim = MultiSensorSimulator(seed=42 + seed_offset)
    duration_sec = max(1, int(num_frames / max(1, sim.cfg["fps"])))

    frame_idx = 0
    for frame in sim.stream(duration_sec=duration_sec, num_objects=num_objects):
        if frame_idx >= num_frames:
            break

        optical = frame["optical_frame"]
        h, w = optical.shape[:2]
        stem = f"{split}_{frame_idx:05d}"
        image_path = images_dir / f"{stem}.jpg"
        label_path = labels_dir / f"{stem}.txt"

        cv2.imwrite(str(image_path), optical)
        lines = []
        for det in frame.get("optical_detections", []):
            class_id = int(det.get("class_id", 5))
            bbox = det.get("bbox", [0, 0, 0, 0])
            lines.append(bbox_to_yolo_line(bbox, class_id, w, h))
            class_counts[class_id] += 1

        label_path.write_text("\n".join(lines) + ("\n" if lines else ""), encoding="utf-8")
        frame_idx += 1

    return class_counts


def generate_dataset(
    output_dir: Path,
    train_frames: int,
    val_frames: int,
    num_objects: int,
    clean: bool,
) -> None:
    if clean:
        for sub in ("images", "labels"):
            target = output_dir / sub
            if target.exists():
                shutil.rmtree(target)

    train_counts = export_split(output_dir, "train", train_frames, num_objects, seed_offset=0)
    val_counts = export_split(output_dir, "val", val_frames, num_objects, seed_offset=1000)

    total = train_frames + val_frames
    print(f"Generated {total} frames under {output_dir}")
    print(f"  images/train, labels/train: {train_frames} frames")
    print(f"  images/val, labels/val:     {val_frames} frames")
    print(f"  train class counts: {dict(sorted(train_counts.items()))}")
    print(f"  val class counts:   {dict(sorted(val_counts.items()))}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate synthetic YOLO dataset from MAVMRF simulator")
    parser.add_argument(
        "--output",
        type=Path,
        default=INCOMING_DATA_DIR,
        help="Output root directory (default: incoming_data/)",
    )
    parser.add_argument("--train-frames", type=int, default=160, help="Number of training frames")
    parser.add_argument("--val-frames", type=int, default=40, help="Number of validation frames")
    parser.add_argument("--num-objects", type=int, default=8, help="Simulated objects per frame")
    parser.add_argument("--clean", action="store_true", help="Remove existing images/ and labels/ before generating")
    args = parser.parse_args()

    logging.basicConfig(level=LOGGING["level"], format=LOGGING["format"])
    generate_dataset(
        output_dir=args.output.resolve(),
        train_frames=args.train_frames,
        val_frames=args.val_frames,
        num_objects=args.num_objects,
        clean=args.clean,
    )


if __name__ == "__main__":
    main()
