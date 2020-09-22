"""
Single entry of shape data (shapes.csv) in MMT GTFS dataset.

The complete MMT GTFS dataset can be downloaded here:
http://transitdata.cityofmadison.com/GTFS/mmt_gtfs.zip
"""
from dataclasses import dataclass
from typing import List

from .base import Locational

__all__ = ("MMTShape",)


@dataclass
class MMTShape(Locational):
    """
    MMT GTFS shape entry.

    .. note::
        ``shape_id`` is a unique ID whereas ``shape_code`` acts the route name.

        There will be some cases that the two different ``shape_id`` are sharing the same ``shape_code``.
    """

    lat: float
    lon: float

    shape_id: int
    shape_code: str

    seq_num: int
    dist_traveled: float

    @staticmethod
    def parse_from_row(row: List[str]):
        """Parse a single entry into :class:`MMTShape` from a csv row."""
        shape_id = int(row[0])
        shape_code = row[1]

        lat, lon = float(row[2]), float(row[3])

        seq_num = int(row[4])
        dist_traveled = float(row[5])

        return MMTShape(lat, lon, shape_id, shape_code, seq_num, dist_traveled)
