import numpy as np

from models.detection_model import DetectionModel


def test_simulation_mode_returns_fallback():
    model = DetectionModel(use_pretrained=False, allow_trained=False)
    fallback = [{"bbox": [1, 2, 3, 4], "object_id": 0, "class_id": 1, "confidence": 0.9}]
    frame = np.zeros((640, 640, 3), dtype=np.uint8)

    detections = model.infer(frame, fallback_detections=fallback)

    assert detections == fallback
