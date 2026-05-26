import argparse
import logging

from config import DATA_YAML, LOGGING, PROJECT_ROOT
from models.detection_model import train_model


def setup_logging() -> None:
    logging.basicConfig(level=LOGGING["level"], format=LOGGING["format"])


def main() -> None:
    parser = argparse.ArgumentParser(description="Train MAVMRF YOLO model")
    parser.add_argument("--data", default=str(DATA_YAML), help="Path to YOLO data.yaml")
    args = parser.parse_args()

    setup_logging()
    data_path = DATA_YAML.__class__(args.data)
    if not data_path.exists():
        raise FileNotFoundError(f"data.yaml not found: {data_path}")

    train_model(data_yaml=data_path, project_root=PROJECT_ROOT)


if __name__ == "__main__":
    main()
