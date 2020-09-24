"""Base dataclass for object that contains coordinates."""
from abc import ABC
from dataclasses import dataclass
from typing import Tuple

from msnmetrosim.utils import distance

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

    def distance(self, lat: float, lon: float) -> float:
        """Get the distance in km between the point and ``(lat, lon)``."""
        return distance((self.lat, self.lon), (lat, lon))
