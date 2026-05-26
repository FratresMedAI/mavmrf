from utils.bbox import attach_track_ids, iou, match_detections


def test_iou_identical_boxes():
    box = [10.0, 10.0, 30.0, 30.0]
    assert iou(box, box) == 1.0


def test_match_detections_copies_object_id():
    primary = [{"bbox": [10, 10, 20, 20], "object_id": -1, "class_id": 5}]
    reference = [{"bbox": [11, 11, 21, 21], "object_id": 2, "class_id": 3}]

    matched = match_detections(primary, reference, threshold=0.2)

    assert matched[0]["object_id"] == 2
    assert matched[0]["class_id"] == 3


def test_attach_track_ids_by_iou():
    fused = [{"bbox": [10, 10, 20, 20]}]
    detections = [{"bbox": [10.5, 10.5, 20.5, 20.5], "track_id": 7}]

    attach_track_ids(fused, detections, threshold=0.2)

    assert fused[0]["track_id"] == 7
