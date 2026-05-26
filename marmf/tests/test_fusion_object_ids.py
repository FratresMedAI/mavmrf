from models.detection_model import DetectionModel
from sensors.fusion import MultiSensorFusion
from sensors.simulation import MultiSensorSimulator
from utils.bbox import match_detections


def test_fusion_receives_sonar_depth_after_yolo_match():
    sim = MultiSensorSimulator(seed=3)
    frame = next(sim.stream(duration_sec=1, num_objects=2))

    fallback = frame["optical_detections"]
    yolo_like = [
        {
            "bbox": list(fallback[0]["bbox"]),
            "object_id": -1,
            "class_id": 99,
            "confidence": 0.95,
        }
    ]
    matched = match_detections(yolo_like, fallback)

    fusion = MultiSensorFusion()
    fused = fusion.fuse(frame, matched)

    assert fused
    assert fused[0]["object_id"] == fallback[0]["object_id"]
    assert fused[0]["depth"] > 0


def test_detection_model_simulation_mode_without_weights():
    model = DetectionModel(use_pretrained=False, allow_trained=False)
    assert model.source == "simulation"
    assert model.model is None
