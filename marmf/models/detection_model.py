import logging
from pathlib import Path
from typing import Dict, List, Optional

import numpy as np

from config import CLASS_NAMES, DETECTION, TRAINED_WEIGHTS

LOGGER = logging.getLogger(__name__)


def resolve_model_path(weights: Optional[str] = None) -> tuple[Path | str, str]:
    """Return model path and source label: trained, pretrained, or explicit override."""
    if weights:
        return weights, "explicit"

    if TRAINED_WEIGHTS.exists():
        return TRAINED_WEIGHTS, "trained"

    return DETECTION["model_name"], "pretrained"


class DetectionModel:
    def __init__(self, model_name: Optional[str] = None, weights: Optional[str] = None):
        resolved, self.source = resolve_model_path(weights or model_name)
        self.model_name = str(resolved)
        self.model = None
        self._load_model()

    def _load_model(self) -> None:
        try:
            from ultralytics import YOLO

            self.model = YOLO(self.model_name)
            LOGGER.info("Loaded YOLO model (%s): %s", self.source, self.model_name)
        except Exception as exc:
            self.model = None
            LOGGER.warning(
                "Unable to load YOLO model (%s). Falling back to simulation detections. Error: %s",
                self.model_name,
                exc,
            )

    def infer(self, frame_bgr: np.ndarray, fallback_detections: Optional[List[Dict]] = None) -> List[Dict]:
        if frame_bgr is None or not isinstance(frame_bgr, np.ndarray):
            return fallback_detections or []

        if self.model is None:
            return fallback_detections or []

        try:
            results = self.model.predict(
                source=frame_bgr,
                conf=DETECTION["conf_threshold"],
                iou=DETECTION["iou_threshold"],
                imgsz=DETECTION["img_size"],
                verbose=False,
            )
            parsed: List[Dict] = []
            for r in results:
                boxes = getattr(r, "boxes", None)
                if boxes is None:
                    continue
                for b in boxes:
                    xyxy = b.xyxy[0].tolist()
                    cls_id = int(b.cls[0].item()) if hasattr(b.cls[0], "item") else int(b.cls[0])
                    conf = float(b.conf[0].item()) if hasattr(b.conf[0], "item") else float(b.conf[0])
                    parsed.append(
                        {
                            "object_id": -1,
                            "bbox": [float(x) for x in xyxy],
                            "class_id": cls_id if 0 <= cls_id < len(CLASS_NAMES) else 5,
                            "confidence": conf,
                        }
                    )
            if fallback_detections:
                for i, det in enumerate(parsed):
                    if i < len(fallback_detections):
                        det["object_id"] = fallback_detections[i].get("object_id", -1)
            return parsed if parsed else (fallback_detections or [])
        except Exception as exc:
            LOGGER.error("Inference failed. Using fallback detections. Error: %s", exc)
            return fallback_detections or []


def train_model(data_yaml: Path, project_root: Path, epochs: Optional[int] = None) -> None:
    try:
        from ultralytics import YOLO

        model = YOLO(DETECTION["model_name"])
        model.train(
            data=str(data_yaml),
            epochs=epochs or DETECTION["train_epochs"],
            imgsz=DETECTION["img_size"],
            batch=DETECTION["batch_size"],
            project=str(project_root / "runs"),
            name="mavmrf_yolo_training",
            exist_ok=True,
        )
        LOGGER.info("Training completed successfully")
    except Exception as exc:
        LOGGER.exception("Training failed: %s", exc)
        raise
