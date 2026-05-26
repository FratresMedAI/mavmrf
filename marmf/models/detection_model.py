import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np

from config import CLASS_NAMES, DETECTION, TRAINED_WEIGHTS
from utils.bbox import match_detections

LOGGER = logging.getLogger(__name__)


def resolve_model_path(
    weights: Optional[str] = None,
    use_pretrained: bool = False,
    allow_trained: bool = True,
) -> Tuple[Optional[str], str]:
    """Return model path and detection source label, or (None, simulation)."""
    if weights:
        return weights, "explicit"

    if allow_trained and TRAINED_WEIGHTS.exists():
        return str(TRAINED_WEIGHTS), "trained"

    if use_pretrained:
        return DETECTION["model_name"], "pretrained"

    return None, "simulation"


class DetectionModel:
    def __init__(
        self,
        weights: Optional[str] = None,
        use_pretrained: bool = False,
        allow_trained: bool = True,
    ):
        resolved, self.source = resolve_model_path(weights, use_pretrained, allow_trained)
        self.model_name = resolved
        self.model = None
        if self.source == "simulation":
            LOGGER.info("Detection source: simulation (no YOLO model loaded)")
        else:
            self._load_model()

    def _load_model(self) -> None:
        try:
            from ultralytics import YOLO

            self.model = YOLO(self.model_name)
            LOGGER.info("Detection source: %s (%s)", self.source, self.model_name)
        except Exception as exc:
            self.model = None
            self.source = "simulation"
            LOGGER.warning(
                "Unable to load YOLO model (%s). Using simulation detections. Error: %s",
                self.model_name,
                exc,
            )

    def infer(self, frame_bgr: np.ndarray, fallback_detections: Optional[List[Dict]] = None) -> List[Dict]:
        fallback = fallback_detections or []

        if frame_bgr is None or not isinstance(frame_bgr, np.ndarray):
            return fallback

        if self.model is None:
            return fallback

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

            if parsed:
                return match_detections(parsed, fallback)

            return fallback
        except Exception as exc:
            LOGGER.error("Inference failed. Using fallback detections. Error: %s", exc)
            return fallback


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
