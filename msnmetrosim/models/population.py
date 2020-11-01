"""Single entry of a population data."""
from dataclasses import dataclass
from typing import List

from .base import LocationalModelBase

__all__ = ("PopulationWard",)


@dataclass
class PopulationWard(LocationalModelBase):
    """
    A single population ward entry.

    .. note::
        ``stop_code`` mostly is just a padded ``stop_id``.

        For example, if ``stop_id`` is ``12``, then ``stop_code`` is ``0012``.

        There are exceptional cases for this.

        If the stop is a transfer point, ``stop_code`` will be the abbreviation instead.

        For example, the ``stop_code`` of *South Transfer Point* is ``SoTP`` instead of ``4000``,
        which is its ``stop_id``.
    """

    # pylint: disable=too-many-instance-attributes

    lat: float
    lon: float

    total: float

    @staticmethod
    def parse_from_row(row: List[str]):
        """Parse a single entry into :class:`PopulationWard` from a row of ``population.csv``."""
        lat, lon = float(row[37]), float(row[38])

        total = float(row[43])

        return PopulationWard(lat, lon, total)
