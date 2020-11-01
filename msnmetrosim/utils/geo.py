"""Geographical helper functions."""
from decimal import Decimal
from math import asin, sin, cos, sqrt, atan2, radians, degrees
from typing import Tuple, List, Set

__all__ = ("distance", "offset", "generate_points")

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


def offset(coord: Tuple[float, float], offset_km: float, bearing: float) -> Tuple[float, float]:
    """
    Calculate the new coordinate offset from ``coord`` by ``offset_dist`` km with ``bearing`` degree.

    This is using Haversine formula.

    .. note::
        Code obtained and modified from https://stackoverflow.com/a/7835325/11571888
    """
    lat_1 = radians(coord[0])
    lon_1 = radians(coord[1])

    bearing_rad = radians(bearing)

    lat_2 = asin(sin(lat_1) * cos(offset_km / EARTH_R) + cos(lat_1) * sin(offset_km / EARTH_R) * cos(bearing_rad))
    lon_2 = lon_1 + atan2(sin(bearing_rad) * sin(offset_km / EARTH_R) * cos(lat_1),
                          cos(offset_km / EARTH_R) - sin(lat_1) * sin(lat_2))

    return degrees(lat_2), degrees(lon_2)


def generate_points(center_coord: Tuple[float, float], range_km: float, interval_km: float) \
        -> List[Tuple[float, float]]:
    """
    Generates coordinates within ``range_km`` km centered at ``center_coord`` in ``interval_km``.

    The generated points will circle around ``center_coord``.

    Count of the points of each layer of the circle
    will be **n * 8** where **n** is the current layer starting from 0 (center),
    except that the center point will also being included.

    Requirements
    ============

    Both ``range_km`` and ``interval_km`` must be > 0.

    If ``interval_km`` > ``range_km``, a set containing only the center coordinates will be returned.

    :raises ValueError: if either ``range_km`` or ``interval_km`` is not > 0.
    """
    if range_km <= 0:
        raise ValueError(f"`range_km` should be > 0: {range_km}")

    if interval_km <= 0:
        raise ValueError(f"`interval_km` should be > 0: {interval_km}")

    center_lat, center_lon = center_coord

    ret: Set[Tuple[float, float]] = {center_coord}  # Duplicated points might be generated

    # Using/casting numbers to :class:`Decimal` to prevent precision lose on generating the circle
    range_km = Decimal(str(range_km))

    cur_range = Decimal(str(interval_km))
    cur_layer = 1

    while cur_range <= range_km:
        cur_bearing = 0
        cur_pt_count = cur_layer * 8
        cur_bearing_interval = 360 / cur_pt_count

        while cur_bearing < 360:
            ret.add(offset((center_lat, center_lon), cur_layer * interval_km, cur_bearing))
            cur_bearing += cur_bearing_interval

        cur_range += Decimal(str(interval_km))
        cur_layer += 1

    return list(ret)
