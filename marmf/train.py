import argparse
import logging
from pathlib import Path
from typing import Optional

from config import DATA_YAML, DETECTION, INCOMING_DATA_DIR, LOGGING, PROJECT_ROOT
from models.detection_model import train_model

LOGGER = logging.getLogger(__name__)

DATASET_HINT = "Run `python scripts/generate_dataset.py --clean` first."


def validate_dataset() -> None:
    train_images = INCOMING_DATA_DIR / "images" / "train"
    val_images = INCOMING_DATA_DIR / "images" / "val"

    missing = []
    for split, path in (("train", train_images), ("val", val_images)):
        if not path.exists() or not any(path.glob("*.jpg")):
            missing.append(split)

    if missing:
        raise FileNotFoundError(
            f"Missing YOLO dataset images for: {', '.join(missing)}. {DATASET_HINT}"
        )


def setup_logging() -> None:
    logging.basicConfig(level=LOGGING["level"], format=LOGGING["format"])


def run(data_yaml: Optional[Path] = None, epochs: Optional[int] = None) -> None:
    data_path = data_yaml or DATA_YAML
    if not data_path.exists():
        raise FileNotFoundError(f"data.yaml not found: {data_path}")

    validate_dataset()
    train_model(data_yaml=data_path, project_root=PROJECT_ROOT, epochs=epochs)


def main() -> None:
    parser = argparse.ArgumentParser(description="Train MAVMRF YOLO model")
    parser.add_argument("--data", default=str(DATA_YAML), help="Path to YOLO data.yaml")
    parser.add_argument(
        "--epochs",
        type=int,
        default=DETECTION["train_epochs"],
        help="Training epochs",
    )
    args = parser.parse_args()

    setup_logging()
    run(data_yaml=Path(args.data), epochs=args.epochs)


if __name__ == "__main__":
    main()
