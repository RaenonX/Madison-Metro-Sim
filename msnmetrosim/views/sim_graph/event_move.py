"""Implementations of a simulated movement event."""
from dataclasses import dataclass
from enum import Enum, auto

from msnmetrosim.utils import TimeableMixin

__all__ = ("MoveEvent", "MoveEventType")


class MoveEventType(Enum):
    """Type of the movement event."""

    WAIT = auto()
    WALK = auto()
    BUS_TRIP = auto()


@dataclass
class MoveEvent(TimeableMixin):
    """
    A simulation event which the agent moves.

    This serves as an edge of the graph of :class:`SimulationStaticPoints`.

    ``event_time`` is the time spent on the movement in seconds.

    ``traveled_dist`` is the distance traveled in km.

    If ``event_type`` is ``MoveEventType.WAIT`` and ``event_time`` is ``60``,
    then this means that the agent waited for 60 seconds.
    """

    event_type: MoveEventType

    event_time: float
    traveled_dist: float

    def __post_init__(self):
        if self.event_type == MoveEventType.WAIT and self.traveled_dist > 0:
            raise ValueError(f"Wait event should not have a distance traveled > 0 ({self.traveled_dist})")

    @property
    def time_spent(self) -> float:
        return self.event_time

    def __str__(self):
        return f"<Move - {self.event_type} - {self.traveled_dist:.3f} km in {self.event_time:.2f} secs>"

    def __repr__(self):
        return self.__str__()
