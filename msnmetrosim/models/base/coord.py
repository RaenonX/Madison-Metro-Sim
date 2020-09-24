"""Base dataclass for object that contains coordinates."""
from abc import ABC
from dataclasses import dataclass
from math import sin, cos, sqrt, atan2, radians
from typing import Tuple

__all__ = ("Locational",)

EARTH_R = 6373.0
"""Approximate radius of earth in km. Used to calculate the distance."""


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
        """
        Get the distance in km between the point and ``(lat, lon)``.

        Code obtained and modified from https://stackoverflow.com/a/19412565/11571888.
        """
        lat_1 = radians(self.lat)
        lon_1 = radians(self.lon)
        lat_2 = radians(lat)
        lon_2 = radians(lon)

        d_lon = lon_2 - lon_1
        d_lat = lat_2 - lat_1

        a = sin(d_lat / 2) ** 2 + cos(lat_1) * cos(lat_2) * sin(d_lon / 2) ** 2  # pylint: disable=invalid-name
        c = 2 * atan2(sqrt(a), sqrt(1 - a))  # pylint: disable=invalid-name

        return EARTH_R * c
