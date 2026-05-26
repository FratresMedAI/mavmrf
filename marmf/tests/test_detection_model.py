import numpy as np

from models.detection_model import DetectionModel


def test_detection_model_loads_or_falls_back_gracefully():
    model = DetectionModel()
    frame = np.zeros((640, 640, 3), dtype=np.uint8)
    fallback = [
        {"bbox": [10, 10, 20, 20], "class_id": 1, "confidence": 0.9, "object_id": 0},
    ]

    detections = model.infer(frame, fallback_detections=fallback)
    assert len(detections) >= 1
