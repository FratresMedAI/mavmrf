from response.response_engine import ResponseEngine


def test_response_report_contains_operator_fields():
    engine = ResponseEngine()
    fused = [
        {
            "object_id": 0,
            "class_id": 2,
            "confidence": 0.8,
            "fused_x": 120.0,
            "fused_y": 45.0,
            "depth": 30.0,
            "bbox": [1, 2, 3, 4],
            "track_id": 1,
        }
    ]

    report = engine.evaluate(timestamp=1.0, fused_objects=fused, track_history=[], changes=[])

    obj = report["fused_objects"][0]
    for field in ("bearing", "estimated_range", "bearing_rate", "contact_type"):
        assert field in obj
    assert report["detection_source"] == "simulation"
