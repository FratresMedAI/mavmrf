import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List

import numpy as np

from config import CLASS_NAMES, REPORTS_DIR, RESPONSE

LOGGER = logging.getLogger(__name__)


class ResponseEngine:
    def __init__(self):
        self.cfg = RESPONSE
        self.last_notifications = {}
        self.last_bearing_by_track = {}
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _contact_type(class_name: str) -> str:
        # Demo heuristic only — not operational biological/non-biological classification.
        biological_like = {"debris_cluster"}
        if class_name in biological_like:
            return "biological_like"
        if class_name == "unidentified_object":
            return "unknown"
        return "non_biological_like"

    def _operator_metrics(self, obj: Dict) -> Dict:
        x = float(obj.get("fused_x", 0.0))
        y = float(obj.get("fused_y", 0.0))
        bearing = float((np.degrees(np.arctan2(y, x)) + 360.0) % 360.0)
        estimated_range = float(np.hypot(x, y))

        track_id = obj.get("track_id")
        previous_bearing = self.last_bearing_by_track.get(track_id)
        bearing_rate = 0.0 if previous_bearing is None else float(bearing - previous_bearing)
        self.last_bearing_by_track[track_id] = bearing

        return {
            "bearing": bearing,
            "estimated_range": estimated_range,
            "bearing_rate": bearing_rate,
        }

    def _notification_level(self, fused_obj: Dict) -> str:
        distance = float(np.hypot(fused_obj.get("fused_x", 0.0), fused_obj.get("fused_y", 0.0)))
        conf = fused_obj.get("confidence", 0)
        if distance <= self.cfg["proximity_alert_distance"] and conf >= self.cfg["high_confidence"]:
            return "advisory"
        if conf >= 0.45:
            return "notification"
        return "log"

    def evaluate(self, timestamp: float, fused_objects: List[Dict], track_history: List[Dict], changes: List[Dict]) -> Dict:
        # Generates advisories based on proximity and confidence to support safe maritime decision making.
        notifications = []
        enriched_fused_objects = []
        for obj in fused_objects:
            level = self._notification_level(obj)
            class_name = CLASS_NAMES[obj.get("class_id", 5)]
            metrics = self._operator_metrics(obj)
            enriched_obj = {
                **obj,
                **metrics,
                "contact_type": self._contact_type(class_name),
            }
            enriched_fused_objects.append(enriched_obj)
            track_id = obj.get("track_id")
            key = f"{class_name}:{track_id}"
            last_time = self.last_notifications.get(key)
            if last_time is not None and (timestamp - last_time) < self.cfg["notification_cooldown_sec"]:
                continue

            message = f"NOTIFICATION: Observed {class_name} (track={obj.get('track_id', 'n/a')}) for safe operations support"
            self.last_notifications[key] = timestamp
            notifications.append(
                {
                    "timestamp": timestamp,
                    "object_id": obj.get("object_id"),
                    "track_id": track_id,
                    "class": class_name,
                    "level": level,
                    "message": message,
                }
            )

        report = {
            "generated_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "timestamp": timestamp,
            "detections_count": len(fused_objects),
            "changes": changes,
            "fused_objects": enriched_fused_objects,
            "tracks": track_history,
            "notifications": notifications,
        }
        return report

    def save_report(self, report: Dict, frame_id: int) -> Path:
        file_path = REPORTS_DIR / f"report_frame_{frame_id:05d}.json"
        with file_path.open("w", encoding="utf-8") as f:
            json.dump(report, f, indent=2)
        LOGGER.info("Saved monitoring report: %s", file_path)
        return file_path
