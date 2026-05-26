from abc import ABC, abstractmethod
from typing import Dict, Generator


class SensorAdapter(ABC):
    """Open-architecture contract for fixed/mobile sensor integration."""

    @abstractmethod
    def stream(self) -> Generator[Dict, None, None]:
        """Yield normalized sensor frames compatible with the monitor pipeline."""
        raise NotImplementedError


class JsonFileSensorAdapter(SensorAdapter):
    """Example adapter interface for external file-based integration flows."""

    def __init__(self, frame_generator: Generator[Dict, None, None]):
        self._frame_generator = frame_generator

    def stream(self) -> Generator[Dict, None, None]:
        yield from self._frame_generator
