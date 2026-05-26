import pytest

from sensors.simulation import MultiSensorSimulator


def test_simulator_stream_yields_required_keys():
    sim = MultiSensorSimulator(seed=1)
    frame = next(sim.stream(duration_sec=1, num_objects=2))

    for key in ("timestamp", "frame_id", "sonar", "acoustic", "magnetic", "optical_frame", "optical_detections"):
        assert key in frame

    assert len(frame["sonar"]) >= 1
    assert len(frame["optical_detections"]) >= 1
    assert frame["optical_frame"].shape == (640, 640, 3)
