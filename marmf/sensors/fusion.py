from typing import Dict, List

import numpy as np

from config import SIMULATION


class MultiSensorFusion:
    def __init__(self):
        self.weights = SIMULATION["sensor_weights"]
        self.world_w = float(SIMULATION["world_width"])
        self.world_h = float(SIMULATION["world_height"])

    def _optical_to_world(self, bbox: List[float], frame_w: int = 640, frame_h: int = 640) -> np.ndarray:
        cx = (bbox[0] + bbox[2]) / 2.0
        cy = (bbox[1] + bbox[3]) / 2.0
        return np.array([(cx / frame_w) * self.world_w, (cy / frame_h) * self.world_h], dtype=float)

    def _estimate_position_from_acoustic(self, acoustic: Dict) -> np.ndarray:
        speed = float(acoustic.get("estimated_speed", 0.0))
        signature = acoustic.get("signature", [0.0, 0.0, 0.0])
        x_hint = speed * 15.0 + (float(signature[0]) if signature else 0.0) * 50.0
        y_hint = speed * 10.0 + (float(signature[1]) if len(signature) > 1 else 0.0) * 50.0
        return np.array([x_hint, y_hint], dtype=float)

    def _estimate_position_from_magnetic(self, magnetic: Dict) -> np.ndarray:
        strength = float(magnetic.get("field_strength", 0.0))
        return np.array([strength * self.world_w * 0.05, strength * self.world_h * 0.05], dtype=float)

    def fuse(self, frame: Dict, detections: List[Dict]) -> List[Dict]:
        sonar_map = {s.get("object_id"): s for s in frame.get("sonar", [])}
        acoustic_map = {a.get("object_id"): a for a in frame.get("acoustic", [])}
        magnetic_map = {m.get("object_id"): m for m in frame.get("magnetic", [])}

        fused: List[Dict] = []
        for det in detections:
            obj_id = det.get("object_id", -1)
            sonar = sonar_map.get(obj_id, {})
            acoustic = acoustic_map.get(obj_id, {})
            magnetic = magnetic_map.get(obj_id, {})

            bbox = det.get("bbox", [0.0, 0.0, 0.0, 0.0])
            optical_world = self._optical_to_world(bbox)
            sonar_world = np.array([float(sonar.get("x", 0.0)), float(sonar.get("y", 0.0))], dtype=float)
            acoustic_world = self._estimate_position_from_acoustic(acoustic)
            magnetic_world = self._estimate_position_from_magnetic(magnetic)

            fused_xy = (
                self.weights["optical"] * optical_world
                + self.weights["sonar"] * sonar_world
                + self.weights["acoustic"] * acoustic_world
                + self.weights["magnetic"] * magnetic_world
            )

            fused.append(
                {
                    "object_id": obj_id,
                    "class_id": int(det.get("class_id", 5)),
                    "confidence": float(det.get("confidence", 0.0)),
                    "fused_x": float(fused_xy[0]),
                    "fused_y": float(fused_xy[1]),
                    "depth": float(sonar.get("depth", 0.0)),
                    "acoustic_signature": acoustic.get("signature", [0.0, 0.0, 0.0]),
                    "magnetic_strength": float(magnetic.get("field_strength", 0.0)),
                    "bbox": bbox,
                    "track_id": det.get("track_id"),
                }
            )

        return fused
