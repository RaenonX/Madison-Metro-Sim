"""
Single entry of stop data (stops.csv) in MMT GTFS dataset.

The complete MMT GTFS dataset can be downloaded here:
http://transitdata.cityofmadison.com/GTFS/mmt_gtfs.zip
"""
from dataclasses import dataclass
from typing import List

from .base import LocationalModelBase, HasCrossModelBase

__all__ = ("MMTStop",)


@dataclass
class MMTStop(HasCrossModelBase, LocationalModelBase):
    """
    MMT GTFS stop entry.

    .. note::
        ``stop_code`` mostly is just a padded ``stop_id``.

        For example, if ``stop_id`` is ``12``, then ``stop_code`` is ``0012``.

        There are exceptional cases for this.

        If the stop is a transfer point, ``stop_code`` will be the abbreviation instead.

        For example, the ``stop_code`` of *South Transfer Point* is ``SoTP`` instead of ``4000``,
        which is its ``stop_id``.
    """

    lat: float
    lon: float

    primary: str
    secondary: str

    stop_id: int
    stop_code: str
    stop_name: str

    wheelchair_accessible: bool

    @property
    def name(self) -> str:
        """
        Formatted name of the stop.

        The return will be <stop_name> (<stop_code>).
        """
        return f"{self.stop_name} ({self.stop_code})"

    @staticmethod
    def parse_from_row(row: List[str]):
        """Parse a single entry into :class:`MMTStop` from a row of ``mmt_gtfs/stops.csv``."""
        stop_id = int(row[0])
        stop_code = row[1]
        stop_name = row[2]

        lat, lon = float(row[4]), float(row[5])

        primary_street = row[13]
        cross_location = row[15]
        wheelchair_accessible = bool(int(row[12]))

        return MMTStop(lat, lon, primary_street, cross_location, stop_id, stop_code, stop_name, wheelchair_accessible)
