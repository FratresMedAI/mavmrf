from dataclasses import dataclass, field
from typing import Dict, List

from config import TRACKING
from utils.bbox import iou


@dataclass
class Track:
    track_id: int
    bbox: List[float]
    class_id: int
    confidence: float
    age: int = 0
    hits: int = 1
    history: List[Dict] = field(default_factory=list)


class SortStyleTracker:
    def __init__(self):
        self.cfg = TRACKING
        self.next_id = 1
        self.tracks: List[Track] = []

    def update(self, detections: List[Dict], timestamp: float) -> List[Dict]:
        if not detections:
            for track in self.tracks:
                track.age += 1
            self.tracks = [t for t in self.tracks if t.age <= self.cfg["max_age"]]
            return detections

        assigned = set()
        for track in self.tracks:
            best_idx, best_iou = -1, 0.0
            for idx, det in enumerate(detections):
                if idx in assigned:
                    continue
                score = iou(track.bbox, det["bbox"])
                if score > best_iou:
                    best_iou = score
                    best_idx = idx

            if best_idx >= 0 and best_iou >= self.cfg["iou_match_threshold"]:
                det = detections[best_idx]
                assigned.add(best_idx)
                track.bbox = det["bbox"]
                track.class_id = det.get("class_id", track.class_id)
                track.confidence = det.get("confidence", track.confidence)
                track.age = 0
                track.hits += 1
                track.history.append(
                    {
                        "timestamp": timestamp,
                        "bbox": det["bbox"],
                        "confidence": det.get("confidence", 0.0),
                        "class_id": det.get("class_id", track.class_id),
                    }
                )
                det["track_id"] = track.track_id
            else:
                track.age += 1

        for idx, det in enumerate(detections):
            if idx in assigned:
                continue
            tr = Track(
                track_id=self.next_id,
                bbox=det["bbox"],
                class_id=det.get("class_id", 5),
                confidence=det.get("confidence", 0.0),
                history=[
                    {
                        "timestamp": timestamp,
                        "bbox": det["bbox"],
                        "confidence": det.get("confidence", 0.0),
                    }
                ],
            )
            det["track_id"] = tr.track_id
            self.next_id += 1
            self.tracks.append(tr)

        self.tracks = [t for t in self.tracks if t.age <= self.cfg["max_age"]]
        return detections

    def export_track_history(self) -> List[Dict]:
        return [
            {
                "track_id": t.track_id,
                "class_id": t.class_id,
                "confidence": t.confidence,
                "history": t.history,
                "hits": t.hits,
            }
            for t in self.tracks
            if t.hits >= self.cfg["min_hits"]
        ]
