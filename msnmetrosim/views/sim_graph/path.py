"""Implementations of a simulated path on the map."""
from typing import List, Optional, Tuple

from .event_move import MoveEvent
from .event_static import StaticPoint

__all__ = ("SimPath",)


class SimPath:
    """A simulated path."""

    def __init__(self, pts: List[StaticPoint], events: List[Optional[MoveEvent]]):
        self._points: List[StaticPoint] = pts
        self._events: List[Optional[MoveEvent]] = events

    def __str__(self):
        ret: List[str] = []

        for point, event in zip(self._points, self._events):
            ret.extend((str(point), str(event)))

        return " -> ".join(ret)

    def __repr__(self):
        return str(self)

    def get_possible_next_paths(self) -> List["SimPath"]:
        """Get a :class:`list` of :class:`SimPath` of the possible next paths."""
        ret: List[SimPath] = []
        last_pt: StaticPoint = self._points[-1]

        for transition_evt, next_pt in last_pt.next_points:
            ret.append(SimPath(self._points + [next_pt], self._events + [transition_evt]))

        return ret

    @property
    def path_tail_coord(self) -> Tuple[float, float]:
        """Get the coordinate of the point at the path tail."""
        return self._points[-1].coordinate

    @property
    def traveled_distance(self) -> float:
        """Get the total distance traveled in **km**."""
        return sum(event.traveled_dist for event in self._events if event)

    @staticmethod
    def from_single_point(start_pt: StaticPoint) -> "SimPath":
        """Initialize a path from a single starting point."""
        return SimPath([start_pt], [None])
