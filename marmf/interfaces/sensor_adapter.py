"""Open-architecture sensor integration contracts.

MAVMRF's monitor pipeline consumes a stream of normalized frames. Live or
recorded sensors plug in here -- simulation and JSON replay are the built-in
paths; AIS / radar / acoustic adapters are the intended next step for
literature-aligned multi-modal replay (see `docs/RELATED_WORK.md`).
"""

from abc import ABC, abstractmethod
from typing import Dict, Generator


class SensorAdapter(ABC):
    """Contract for fixed or mobile sensor feeds into the monitor pipeline.

    Implementations should yield dict frames compatible with
    `SensorPreprocessor` / `DetectionModel` / `MultiSensorFusion`.

    Planned real-world adapters (not shipped -- extension points):

    * **AIS replay** -- decode NMEA/JSON AIS tracks into bearing/range or
      geo-referenced contacts, time-aligned with optical frames when present.
    * **Radar replay** -- CFAR or tracklet lists (range, azimuth, Doppler)
      mapped into the same contact space used by fusion.
    * **Multi-rate sync** -- buffer asynchronous AIS/radar vs optical using
      timestamps; associate with bearing-range gates rather than 2D IoU alone.

    Until those exist, use `JsonFileSensorAdapter` with
    `incoming_data/samples/` (optional `optical_image` sidecar) or the
    built-in `MultiSensorSimulator` stream from `main.py`.
    """

    @abstractmethod
    def stream(self) -> Generator[Dict, None, None]:
        """Yield normalized sensor frames compatible with the monitor pipeline."""
        raise NotImplementedError


class JsonFileSensorAdapter(SensorAdapter):
    """Replay JSON frames from disk (or any pre-built frame generator).

    Suitable for recorded optical + metadata fixtures today. Future AIS/radar
    dumps can use the same pattern: one JSON record per time step with
    sensor-specific lists under `sonar` / `acoustic` / `magnetic` and
    optional `optical_frame` / `optical_detections` / `optical_image`.
    """

    def __init__(self, frame_generator: Generator[Dict, None, None]):
        self._frame_generator = frame_generator

    def stream(self) -> Generator[Dict, None, None]:
        yield from self._frame_generator
