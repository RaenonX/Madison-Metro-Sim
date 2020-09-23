"""
Single entry of trip data (trips.csv) in MMT GTFS dataset.

The complete MMT GTFS dataset can be downloaded here:
http://transitdata.cityofmadison.com/GTFS/mmt_gtfs.zip
"""
from dataclasses import dataclass
from datetime import time
from enum import Enum, auto
from typing import List

from msnmetrosim.utils import time_from_seconds

__all__ = ("MMTTrip", "MMTTripType")


class MMTTripType(Enum):
    """
    Enum to represent MMT trip type.

    .. note::
        Documentations except ``MMTTripType.MMTTripType`` are
        copied from ``extended_data_dictionary.txt`` of MMT GTFS dataset.
    """

    ALL_DATES = auto()
    """Trip generally operates on all service dates - including weekday/weekend/holiday service dates."""

    NO_HOLIDAY = auto()
    """Trip generally operates on all service dates - except Holiday service dates."""

    WEEKEND_HOLIDAY = auto()
    """Trip generally operates on Weekend and Holiday service dates only."""

    WEEKDAY = auto()
    """Trip generally operates on Weekday service dates only."""

    FRIDAY = auto()
    """Trip only operates on Friday Standard service dates."""

    RECESS = auto()
    """Trip only operates on Recess service dates."""

    UNKNOWN = auto()
    """Sentinel value for empty code."""

    @staticmethod
    def parse_from_data(code: str):
        """Parse the trip type from the original data."""
        # pylint: disable=too-many-return-statements

        if not code:
            return MMTTripType.UNKNOWN

        if code == "D":
            return MMTTripType.ALL_DATES

        if code == "H":
            return MMTTripType.NO_HOLIDAY

        if code == "S":
            return MMTTripType.WEEKEND_HOLIDAY

        if code == "W":
            return MMTTripType.WEEKDAY

        if code == "F":
            return MMTTripType.FRIDAY

        if code == "R":
            return MMTTripType.RECESS

        return ValueError(f"Unknown trip type code: {code}")


@dataclass
class MMTTrip:
    """
    MMT GTFS trip entry.

    .. note::
        ``route_id`` and ``route_short_name`` mimics the data in ``routes.csv``.

        - Also will be as same as the field name of :class:`MMTRoute`.

        ``service_id`` is the service plan ID **PLUS** the service days code.

        - The ``service_id`` here corresponds to the data in ``calendar.csv`` and ``calendar_dates.csv``.

        ``shape_id`` and ``shape_code`` mimics the data in ``shapes.csv``.

        - Also will be as same as the field name of :class:`MMTShape`.

        ``trip_sort`` in the original data file / ``trip_departure`` after parse is the scheduled departure time.

        - ``trip_sort`` scheduled departure time counting from 12 AM in seconds

        - ``trip_departure`` is the parsed ``trip_sort`` in :class:`datetime.time`.

        Currently not sure about the meaning of ``block_id``. Awaiting investigation.
    """

    # pylint: disable=too-many-instance-attributes

    route_id: int
    route_short_name: str

    service_id: str

    trip_id: id
    trip_headsign: str

    trip_direction_id: int
    trip_direction_name: str

    block_id: int
    shape_id: int
    shape_code: str

    trip_type: MMTTripType
    trip_departure: time

    @staticmethod
    def parse_from_row(row: List[str]):
        """Parse a single entry into :class:`MMTTrip` from a row of ``mmt_gtfs/trips.csv``."""
        route_id = int(row[0])
        route_short_name = row[1]

        service_id = row[2]

        trip_id = int(row[3])
        trip_headsign = row[4]

        trip_direction_id = int(row[5])
        trip_direction_name = row[6]

        block_id = int(row[7])
        shape_id = int(row[8])
        shape_code = row[9]

        trip_type = MMTTripType.parse_from_data(row[10])
        trip_departure = time_from_seconds(int(row[11]))

        return MMTTrip(route_id, route_short_name, service_id, trip_id, trip_headsign,
                       trip_direction_id, trip_direction_name, block_id, shape_id, shape_code,
                       trip_type, trip_departure)
