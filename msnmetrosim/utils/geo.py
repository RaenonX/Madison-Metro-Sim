"""Geographical helper functions."""
from math import sin, cos, sqrt, atan2, radians
from typing import Tuple

__all__ = ("distance",)

EARTH_R = 6378.137
"""Approximate radius of earth in km. Used to calculate the distance."""


def distance(p1: Tuple[float, float], p2: Tuple[float, float]):  # pylint: disable=invalid-name
    """
    Get the distance between the coordinates ``p1`` and ``p2`` in **km**.

    Both ``p1`` and ``p2`` should be in the format of ``(lat, lon)``.

    This is using Haversine formula.

    .. note::
        The reason of not using ``geopy.distance.distance`` is because that
        it takes 10 ms to calculate 100 distances, while this formula only takes 1 ms.

        Code obtained and modified from https://stackoverflow.com/a/19412565/11571888.
    """
    lat_1 = radians(p1[0])
    lon_1 = radians(p1[1])
    lat_2 = radians(p2[0])
    lon_2 = radians(p2[1])

    d_lon = lon_2 - lon_1
    d_lat = lat_2 - lat_1

    a = sin(d_lat / 2) ** 2 + cos(lat_1) * cos(lat_2) * sin(d_lon / 2) ** 2  # pylint: disable=invalid-name
    c = 2 * atan2(sqrt(a), sqrt(1 - a))  # pylint: disable=invalid-name

    return EARTH_R * c
