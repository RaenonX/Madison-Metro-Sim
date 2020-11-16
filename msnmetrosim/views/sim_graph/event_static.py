"""Implementations of the event which the agents does **NOT** move."""
from datetime import datetime
from typing import List, Optional, Tuple

from msnmetrosim.models import MMTStopScheduleSim
from msnmetrosim.utils import TimeableMixin
from .event_move import MoveEvent

__all__ = ("StaticPoint", "ScheduledStop", "StopWait", "StopBase")


class StaticPoint(TimeableMixin):
    """
    A static point for the simulation.

    This serves as a node of the graph of :class:`SimulationMap`.
    """

    @property
    def time_spent(self) -> float:
        return (self._dt_out - self._dt_in).total_seconds()

    @property
    def next_points(self) -> List[Tuple[MoveEvent, "StaticPoint"]]:
        """Get a :class:`list` of the next points with its corresponding movement event."""
        return self._next_points

    @property
    def coordinate(self) -> Tuple[float, float]:
        """Get the coordinate of the stop."""
        return self._coordinate

    @property
    def dt_in(self) -> datetime:
        """Get the timestamp of an agent get into this point."""
        return self._dt_in

    @property
    def dt_out(self) -> datetime:
        """Get the timestamp of an agent get out of this point."""
        return self._dt_out

    def __init__(self, dt_in: datetime, dt_out: datetime, coordinate: Tuple[float, float],
                 next_points: Optional[List[Tuple[MoveEvent, "StaticPoint"]]] = None):
        self._dt_in: datetime = dt_in
        self._dt_out: datetime = dt_out
        self._coordinate = coordinate
        self._next_points: List[Tuple[MoveEvent, StaticPoint]] = next_points or []

    def __hash__(self):
        return id(self)

    def __str__(self):
        return f"<Static - {self._dt_in} ~ {self._dt_out} / Next: ({len(self._next_points)})>"

    def __repr__(self):
        return self.__str__()

    def add_next_point(self, event_move: MoveEvent, point: "StaticPoint"):
        """Add the next :class:`StaticPoint` transitioned by the movement event ``event_move``."""
        self._next_points.append((event_move, point))


class StopBase(StaticPoint):
    """
    Base class for a stop in a certain time range.

    This serves as a node of the graph of :class:`SimulationMap`, especially as a bus stop at a moment,
    according to the schedule of MMT GTFS.
    """

    @property
    def trip_id(self) -> int:
        """Get the trip ID."""
        return self._stop_sim.trip_id

    @property
    def stop_id(self) -> int:
        """Get the stop ID."""
        return self._stop_sim.stop_id

    @property
    def stop_sim(self) -> MMTStopScheduleSim:
        """Get :class:`MMTStopScheduleSim` of this scheduled stop."""
        return self._stop_sim

    def __init__(self, dt_in: datetime, dt_out: datetime, stop_sim: MMTStopScheduleSim,
                 coordinate: Tuple[float, float], next_points: Optional[List["StaticPoint"]] = None):
        super().__init__(dt_in, dt_out, coordinate, next_points)

        self._stop_sim: MMTStopScheduleSim = stop_sim

    def __str__(self):
        return f"<Static - Stop #{self.stop_id} - {self._dt_in} ~ {self._dt_out} " \
               f"/ Next: ({len(self._next_points)})>"

    def __repr__(self):
        return self.__str__()

    def is_same_stop(self, other: StaticPoint):
        """Check if ``other`` is the same stop as this stop by checking the type of ``other`` and its stop ID."""
        return isinstance(other, StopBase) and other.stop_id == self.stop_id


class ScheduledStop(StopBase):
    """
    A stop at a moment which a bus will arrive.

    This serves as a node of the graph of :class:`SimulationMap`, especially as a bus stop at a moment,
    according to the schedule of MMT GTFS.
    """

    def __str__(self):
        return f"<Static - Stop (Schedule) #{self.stop_id} - {self._dt_in} ~ {self._dt_out} " \
               f"/ Next: ({len(self._next_points)})>"

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def from_stop_schedule_sim(stop_schedule: MMTStopScheduleSim, coordinate: Tuple[float, float]) -> "StaticPoint":
        """Create a :class:`StaticPoint` from :class:`MMTStopScheduleSim`."""
        return ScheduledStop(stop_schedule.arrival_time, stop_schedule.departure_time, stop_schedule, coordinate)


class StopWait(StopBase):
    """
    Static point event of an agent waiting at the stop.

    This serves as a node of the graph of :class:`SimulationMap`, especially as a bus stop at a moment,
    according to the schedule of MMT GTFS.
    """

    def __str__(self):
        return f"<Static - Stop (Wait) #{self.stop_id} - {self._dt_in} ~ {self._dt_out} " \
               f"/ Next: ({len(self._next_points)})>"

    def __repr__(self):
        return self.__str__()
