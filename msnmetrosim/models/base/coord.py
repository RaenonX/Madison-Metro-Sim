"""Base dataclass for object that contains coordinates."""
from abc import ABC
from dataclasses import dataclass
from typing import Tuple

__all__ = ("Locational",)


@dataclass
class Locational(ABC):
    """Interface for the data entry which contains coordinates."""

    lat: float
    lon: float

    @property
    def coordinate(self) -> Tuple[float, float]:
        """Coordinate in ``tuple`` of the stop."""
        return self.lat, self.lon
