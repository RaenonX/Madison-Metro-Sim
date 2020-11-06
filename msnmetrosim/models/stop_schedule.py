"""
Single entry of stop time schedule data (stop_times.csv) in MMT GTFS dataset.

The complete MMT GTFS dataset can be downloaded here:
http://transitdata.cityofmadison.com/GTFS/mmt_gtfs.zip
"""
from dataclasses import dataclass
from datetime import datetime, time, date
from typing import List, Optional

__all__ = ("MMTStopSchedule", "MMTStopScheduleSim")


@dataclass
class MMTStopSchedule:
    """
    MMT GTFS stop schedule entry.

    .. note::
        `timepoint` means that the bus will depart at the scheduled time if it arrives earlier.
    """

    # pylint: disable=too-many-instance-attributes

    trip_id: int

    stop_sequence: int
    stop_id: int

    arrival_time: time
    departure_time: time

    timepoint: bool

    shape_dist_traveled: float

    @staticmethod
    def parse_from_row(row: List[str]):
        """Parse a single entry into :class:`MMTStopSchedule` from a row of ``mmt_gtfs/stop_times.csv``."""

        # pylint: disable=too-many-instance-attributes

        def parse_time(time_str: str):
            hour, minute, second = time_str.split(":", 2)

            return time(int(hour) % 24, int(minute), int(second))

        trip_id = int(row[0])

        stop_sequence = int(row[1])
        stop_id = int(row[2])

        arrival_time = parse_time(row[5])
        departure_time = parse_time(row[6])

        timepoint = bool(int(row[7]))

        shape_dist_traveled = float(row[9])

        return MMTStopSchedule(
            trip_id, stop_sequence, stop_id, arrival_time, departure_time, timepoint, shape_dist_traveled
        )


@dataclass
class MMTStopScheduleSim(MMTStopSchedule):
    """
    Same as :class:`MMTStopSchedule` with ``arrival_time`` and ``departure_time`` being :class:`datetime`.

    This could be used for actual simulation, since :class:`MMTStopSchedule` does not record the date,
    causing issues when handling the cross-day travel.
    """

    arrival_time: datetime
    departure_time: datetime

    next_stop: "MMTStopScheduleSim"

    @staticmethod
    def from_raw(stop_schedule: MMTStopSchedule, arrival_date: date, departure_date: Optional[date] = None, /,
                 next_stop: Optional["MMTStopScheduleSim"] = None):
        """
        Convert a :class:`MMTStopSchedule` to :class:`MMTStopSchedulSimulated`.

        If ``departure_date`` is ``None``, ``arrival_date`` will be applied for the departure time.
        """
        if not departure_date:
            departure_date = arrival_date

        return MMTStopScheduleSim(
            stop_schedule.trip_id, stop_schedule.stop_sequence, stop_schedule.stop_id,
            datetime.combine(arrival_date, stop_schedule.arrival_time),
            datetime.combine(departure_date, stop_schedule.departure_time),
            stop_schedule.timepoint,
            stop_schedule.shape_dist_traveled,
            next_stop
        )
