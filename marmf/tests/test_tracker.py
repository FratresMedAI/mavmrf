from tracking.tracker import SortStyleTracker


def test_tracker_assigns_persistent_ids():
    tracker = SortStyleTracker()
    detections_a = [
        {"bbox": [10.0, 10.0, 30.0, 30.0], "class_id": 1, "confidence": 0.9, "object_id": 0},
    ]
    detections_b = [
        {"bbox": [12.0, 12.0, 32.0, 32.0], "class_id": 1, "confidence": 0.88, "object_id": 0},
    ]

    out_a = tracker.update(detections_a, timestamp=0.0)
    out_b = tracker.update(detections_b, timestamp=0.2)

    assert out_a[0]["track_id"] == out_b[0]["track_id"]
