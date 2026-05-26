import logging
from dataclasses import asdict, dataclass
from typing import Dict, Generator, List, Optional, Tuple

import cv2
import numpy as np

from config import CLASS_NAMES, SIMULATION

LOGGER = logging.getLogger(__name__)


@dataclass
class SimObject:
    object_id: int
    class_id: int
    x: float
    y: float
    depth: float
    vx: float
    vy: float
    size: float


class MultiSensorSimulator:
    def __init__(self, seed: Optional[int] = 42):
        self.cfg = SIMULATION
        self.rng = np.random.default_rng(seed)
        self.width = float(self.cfg["world_width"])
        self.height = float(self.cfg["world_height"])
        self.depth_min = float(self.cfg["depth_min"])
        self.depth_max = float(self.cfg["depth_max"])

    def _spawn_objects(self, num_objects: int) -> List[SimObject]:
        objects: List[SimObject] = []
        pad = float(self.cfg["object_spawn_padding"])
        for i in range(max(1, int(num_objects))):
            speed = float(self.rng.uniform(self.cfg["min_speed_mps"], self.cfg["max_speed_mps"]))
            heading = float(self.rng.uniform(0, 2 * np.pi))
            objects.append(
                SimObject(
                    object_id=i,
                    class_id=int(self.rng.integers(0, len(CLASS_NAMES))),
                    x=float(self.rng.uniform(pad, self.width - pad)),
                    y=float(self.rng.uniform(pad, self.height - pad)),
                    depth=float(self.rng.uniform(self.depth_min, self.depth_max)),
                    vx=float(np.cos(heading) * speed),
                    vy=float(np.sin(heading) * speed),
                    size=float(self.rng.uniform(10.0, 35.0)),
                )
            )
        LOGGER.info("Spawned %s objects for live simulation", len(objects))
        return objects

    def _step_objects(self, objects: List[SimObject], dt: float) -> None:
        for obj in objects:
            obj.vx += float(self.rng.normal(0, 0.04))
            obj.vy += float(self.rng.normal(0, 0.04))
            speed = float(np.hypot(obj.vx, obj.vy))
            max_speed = float(self.cfg["max_speed_mps"])
            if speed > max_speed:
                ratio = max_speed / speed
                obj.vx *= ratio
                obj.vy *= ratio

            obj.x += obj.vx * dt
            obj.y += obj.vy * dt
            obj.depth = float(np.clip(obj.depth + self.rng.normal(0, 0.15), self.depth_min, self.depth_max))

            if obj.x < 0.0 or obj.x > self.width:
                obj.vx *= -1.0
                obj.x = float(np.clip(obj.x, 0.0, self.width))
            if obj.y < 0.0 or obj.y > self.height:
                obj.vy *= -1.0
                obj.y = float(np.clip(obj.y, 0.0, self.height))

    def _sonar_readings(self, objects: List[SimObject]) -> List[Dict]:
        out: List[Dict] = []
        for obj in objects:
            out.append(
                {
                    "object_id": obj.object_id,
                    "x": float(obj.x + self.rng.normal(0, self.cfg["sonar_noise_std"])),
                    "y": float(obj.y + self.rng.normal(0, self.cfg["sonar_noise_std"])),
                    "depth": float(obj.depth + self.rng.normal(0, 1.1)),
                    "intensity": float(max(0.05, 1.0 - (obj.depth / self.depth_max))),
                }
            )
        return out

    def _acoustic_readings(self, objects: List[SimObject]) -> List[Dict]:
        out: List[Dict] = []
        for obj in objects:
            speed = float(np.hypot(obj.vx, obj.vy))
            base_sig = np.array(
                [
                    speed / max(float(self.cfg["max_speed_mps"]), 1e-6),
                    obj.size / 40.0,
                    obj.depth / self.depth_max,
                ],
                dtype=float,
            )
            sig = (base_sig + self.rng.normal(0, self.cfg["acoustic_noise_std"], size=3)).clip(0, 1)
            out.append(
                {
                    "object_id": obj.object_id,
                    "signature": sig.tolist(),
                    "estimated_speed": float(max(0.0, speed + self.rng.normal(0, 0.2))),
                }
            )
        return out

    def _magnetic_readings(self, objects: List[SimObject]) -> List[Dict]:
        out: List[Dict] = []
        for obj in objects:
            metallic_bias = 0.6 if CLASS_NAMES[obj.class_id] in {"large_uuv", "commercial_drone"} else 0.25
            out.append(
                {
                    "object_id": obj.object_id,
                    "field_strength": float(max(0.0, metallic_bias + self.rng.normal(0, self.cfg["magnetic_noise_std"]))),
                }
            )
        return out

    def _optical_frame(self, objects: List[SimObject], frame_size: Tuple[int, int] = (640, 640)):
        h, w = frame_size
        frame = np.zeros((h, w, 3), dtype=np.uint8)
        frame[:] = (12, 18, 24)
        sx = w / self.width
        sy = h / self.height
        detections: List[Dict] = []

        for obj in objects:
            cx = int(np.clip(obj.x * sx, 0, w - 1))
            cy = int(np.clip(obj.y * sy, 0, h - 1))
            radius = int(max(4, obj.size * 0.24 + self.rng.normal(0, self.cfg["optical_noise_std"] * 0.1)))
            color = (30, int(100 + 15 * obj.class_id) % 255, int(160 + 10 * obj.class_id) % 255)
            cv2.circle(frame, (cx, cy), radius, color, -1)

            x1 = float(max(0, cx - radius))
            y1 = float(max(0, cy - radius))
            x2 = float(min(w - 1, cx + radius))
            y2 = float(min(h - 1, cy + radius))
            detections.append(
                {
                    "object_id": obj.object_id,
                    "bbox": [x1, y1, x2, y2],
                    "class_id": obj.class_id,
                    "confidence": float(self.rng.uniform(0.65, 0.98)),
                }
            )

        noise = self.rng.normal(0, self.cfg["optical_noise_std"], size=frame.shape).astype(np.int16)
        frame = np.clip(frame.astype(np.int16) + noise, 0, 255).astype(np.uint8)
        return frame, detections

    def stream(self, duration_sec: int, num_objects: int) -> Generator[Dict, None, None]:
        fps = int(max(1, self.cfg["fps"]))
        dt = 1.0 / float(fps)
        total_frames = max(1, int(duration_sec * fps))
        objects = self._spawn_objects(num_objects)

        for frame_id in range(total_frames):
            self._step_objects(objects, dt)
            optical_frame, optical_detections = self._optical_frame(objects)
            yield {
                "timestamp": float(frame_id * dt),
                "frame_id": frame_id,
                "sonar": self._sonar_readings(objects),
                "acoustic": self._acoustic_readings(objects),
                "magnetic": self._magnetic_readings(objects),
                "optical_frame": optical_frame,
                "optical_detections": optical_detections,
                "ground_truth": [asdict(x) for x in objects],
            }

    def batch(self, duration_sec: int, num_objects: int) -> List[Dict]:
        return list(self.stream(duration_sec=duration_sec, num_objects=num_objects))
