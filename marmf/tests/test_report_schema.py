from models.detection_model import DetectionModel
from response.response_engine import ResponseEngine
from sensors.fusion import MultiSensorFusion
from sensors.preprocessing import SensorPreprocessor
from sensors.simulation import MultiSensorSimulator
from tracking.tracker import SortStyleTracker
from utils.bbox import attach_track_ids


def test_report_schema_from_single_frame():
    sim = MultiSensorSimulator(seed=11)
    frame = next(sim.stream(duration_sec=1, num_objects=2))

    pre = SensorPreprocessor()
    prepared = pre.preprocess(frame, previous_frame=None)

    detector = DetectionModel(use_pretrained=False, allow_trained=False)
    tracker = SortStyleTracker()
    fusion = MultiSensorFusion()
    responder = ResponseEngine()

    detections = detector.infer(
        prepared["optical_frame"],
        fallback_detections=prepared.get("optical_detections", []),
    )
    detections = tracker.update(detections, timestamp=prepared["timestamp"])
    fused = fusion.fuse(prepared, detections)
    attach_track_ids(fused, detections)

    report = responder.evaluate(
        timestamp=prepared["timestamp"],
        fused_objects=fused,
        track_history=tracker.export_track_history(),
        changes=prepared.get("changes", []),
        detection_source=detector.source,
    )

    for key in ("detection_source", "fused_objects", "tracks", "notifications", "changes"):
        assert key in report

    assert report["detection_source"] == "simulation"
    assert report["fused_objects"]

    obj = report["fused_objects"][0]
    for field in ("bearing", "estimated_range", "bearing_rate", "contact_type"):
        assert field in obj
