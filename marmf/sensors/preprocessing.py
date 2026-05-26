import logging
from typing import Dict, List, Optional

import cv2
import numpy as np

from config import SIMULATION

LOGGER = logging.getLogger(__name__)


class SensorPreprocessor:
    def __init__(self, filter_sensitivity: Optional[str] = None):
        sensitivity = (filter_sensitivity or SIMULATION.get("default_filter_sensitivity", "medium")).lower()
        scale_map = SIMULATION.get("filter_sensitivity_scale", {"low": 1.4, "medium": 1.0, "high": 0.65})
        scale = float(scale_map.get(sensitivity, 1.0))
        self.threshold = float(SIMULATION["change_detection_threshold"]) * scale
        self.filter_sensitivity = sensitivity

    @staticmethod
    def _normalize(values: np.ndarray) -> np.ndarray:
        if values.size == 0:
            return values
        vmin = float(np.min(values))
        vmax = float(np.max(values))
        if np.isclose(vmin, vmax):
            return np.zeros_like(values, dtype=float)
        return (values - vmin) / (vmax - vmin)

    def _preprocess_optical(self, frame_bgr: np.ndarray) -> np.ndarray:
        if frame_bgr is None or not isinstance(frame_bgr, np.ndarray) or frame_bgr.size == 0:
            return np.zeros((640, 640, 3), dtype=np.uint8)
        blurred = cv2.GaussianBlur(frame_bgr, (3, 3), 0)
        return cv2.convertScaleAbs(blurred, alpha=1.05, beta=2)

    def preprocess(self, frame: Dict, previous_frame: Optional[Dict] = None) -> Dict:
        sonar = frame.get("sonar", [])
        acoustic = frame.get("acoustic", [])
        magnetic = frame.get("magnetic", [])

        sonar_xyz = np.array([[s.get("x", 0.0), s.get("y", 0.0), s.get("depth", 0.0)] for s in sonar], dtype=float)
        if sonar_xyz.size:
            sonar_xyz[:, 0] = self._normalize(sonar_xyz[:, 0])
            sonar_xyz[:, 1] = self._normalize(sonar_xyz[:, 1])
            sonar_xyz[:, 2] = self._normalize(sonar_xyz[:, 2])
            for idx, row in enumerate(sonar_xyz.tolist()):
                sonar[idx]["x_n"], sonar[idx]["y_n"], sonar[idx]["depth_n"] = row

        for acoustic_item in acoustic:
            sig = np.array(acoustic_item.get("signature", [0.0, 0.0, 0.0]), dtype=float)
            acoustic_item["signature_norm"] = self._normalize(sig).tolist() if sig.size else [0.0, 0.0, 0.0]

        magnetic_vals = np.array([m.get("field_strength", 0.0) for m in magnetic], dtype=float)
        magnetic_norm = self._normalize(magnetic_vals) if magnetic_vals.size else np.array([])
        for idx, norm_v in enumerate(magnetic_norm.tolist() if magnetic_norm.size else []):
            magnetic[idx]["field_strength_norm"] = float(norm_v)

        frame["optical_frame"] = self._preprocess_optical(frame.get("optical_frame"))
        frame["filter_sensitivity"] = self.filter_sensitivity
        frame["changes"] = self.detect_changes(frame, previous_frame)
        return frame

    def detect_changes(self, current: Dict, previous: Optional[Dict]) -> List[Dict]:
        if previous is None:
            return []

        prev_map = {item.get("object_id"): item for item in previous.get("sonar", [])}
        changes: List[Dict] = []
        for now in current.get("sonar", []):
            object_id = now.get("object_id")
            prev = prev_map.get(object_id)
            if prev is None:
                changes.append({"object_id": object_id, "change_type": "new"})
                continue

            move_dist = float(np.hypot(now.get("x", 0.0) - prev.get("x", 0.0), now.get("y", 0.0) - prev.get("y", 0.0)))
            depth_change = float(abs(now.get("depth", 0.0) - prev.get("depth", 0.0)))
            if move_dist >= self.threshold or depth_change >= (self.threshold * 0.3):
                changes.append(
                    {
                        "object_id": object_id,
                        "change_type": "moving",
                        "distance": move_dist,
                        "depth_delta": depth_change,
                    }
                )

        return changes
