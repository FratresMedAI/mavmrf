from typing import Dict, List


def iou(box_a: List[float], box_b: List[float]) -> float:
    x1 = max(box_a[0], box_b[0])
    y1 = max(box_a[1], box_b[1])
    x2 = min(box_a[2], box_b[2])
    y2 = min(box_a[3], box_b[3])

    inter = max(0, x2 - x1) * max(0, y2 - y1)
    area_a = max(0, box_a[2] - box_a[0]) * max(0, box_a[3] - box_a[1])
    area_b = max(0, box_b[2] - box_b[0]) * max(0, box_b[3] - box_b[1])
    denom = area_a + area_b - inter
    return inter / denom if denom > 0 else 0.0


def match_detections(
    primary: List[Dict],
    reference: List[Dict],
    threshold: float = 0.2,
    copy_class_id: bool = True,
) -> List[Dict]:
    """Assign object_id (and optionally class_id) from reference boxes onto primary via IoU."""
    if not primary or not reference:
        return primary

    assigned_refs = set()
    matched: List[Dict] = []

    for det in primary:
        best_idx = -1
        best_score = 0.0
        for idx, ref in enumerate(reference):
            if idx in assigned_refs:
                continue
            score = iou(det.get("bbox", []), ref.get("bbox", []))
            if score > best_score:
                best_score = score
                best_idx = idx

        out = dict(det)
        if best_idx >= 0 and best_score >= threshold:
            ref = reference[best_idx]
            assigned_refs.add(best_idx)
            out["object_id"] = ref.get("object_id", out.get("object_id", -1))
            if copy_class_id and "class_id" in ref:
                out["class_id"] = ref["class_id"]
        matched.append(out)

    return matched


def attach_track_ids(
    fused_objects: List[Dict],
    detections: List[Dict],
    threshold: float = 0.2,
) -> None:
    """Attach track_id from detections to fused objects using IoU (in-place)."""
    assigned = set()
    for obj in fused_objects:
        obj_bbox = obj.get("bbox")
        if not obj_bbox:
            continue

        best_idx = -1
        best_score = 0.0
        for idx, det in enumerate(detections):
            if idx in assigned:
                continue
            score = iou(obj_bbox, det.get("bbox", []))
            if score > best_score:
                best_score = score
                best_idx = idx

        if best_idx >= 0 and best_score >= threshold:
            assigned.add(best_idx)
            obj["track_id"] = detections[best_idx].get("track_id")
