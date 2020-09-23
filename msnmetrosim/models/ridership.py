"""
Models of the ridership data.

Check https://github.com/RaenonX/Madison-Metro-Sim/issues/1 for ridership data in various dimensions.
"""
from dataclasses import dataclass

__all__ = ("RidershipByStop",)

from typing import List


@dataclass
class RidershipByStop:
    """
    An entry of the ridership data grouped by stop.

    Dataset link: https://data-cityofmadison.opendata.arcgis.com/datasets/metro-transit-ridership-by-stop

    .. note::
        (Copied from the webpage of the corresponding dataset)

        Metro Transit ridership by stop in March, 2019.
        Caution should be used with this data.

        Daily bus stop boardings were estimated using a 12-day sample of weekday farebox records and AVL logs,
        and the GTFS file, from March 2015 from Metro Transit.

        Ridership estimates exclude supplemental schooldays routes and paratransit service.

        Caution should be exercised when attempting to compare data from individual stops;
        ridership data should be considered in the context of the system as a whole.

        Bus stops were assigned to each boarding event given the estimated location of the bus
        at the time of the farebox transaction.
    """

    stop_id: int

    weekday: float
    saturday: float
    sunday: float

    @staticmethod
    def parse_from_row(row: List[str]):
        """Parse a single entry into :class:`RidershipByStop` from a row of ``ridership/by_stop.csv``."""
        stop_id = int(row[3])

        weekday = float(row[8])
        saturday = float(row[9])
        sunday = float(row[10])

        return RidershipByStop(stop_id, weekday, saturday, sunday)
