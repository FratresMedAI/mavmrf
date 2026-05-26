import json
from pathlib import Path

import cv2
import numpy as np

from main import load_file_stream


def test_optical_replay_fixture_loads_image():
    samples = Path(__file__).resolve().parents[1] / "incoming_data" / "samples"
    optical_frame = next(
        frame["optical_frame"]
        for frame in load_file_stream(samples)
        if frame.get("optical_image") == "frame_optical_000.jpg"
    )

    assert optical_frame.shape == (640, 640, 3)
    assert int(np.sum(optical_frame)) > 0


def test_optical_fixture_json_references_sidecar():
    samples = Path(__file__).resolve().parents[1] / "incoming_data" / "samples"
    payload = json.loads((samples / "frame_optical_000.json").read_text(encoding="utf-8"))
    assert payload.get("optical_image") == "frame_optical_000.jpg"
    assert (samples / "frame_optical_000.jpg").exists()
    loaded = cv2.imread(str(samples / "frame_optical_000.jpg"))
    assert loaded is not None
