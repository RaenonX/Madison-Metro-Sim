"""Implementations of a simulated path on the map."""
from typing import List, Optional, Tuple

from msnmetrosim.utils import distance
from .event_move import MoveEvent
from .event_static import StaticPoint

__all__ = ("SimPath",)


class SimPath:
    """
    A simulated path.

    A path consists of a series of :class:`StaticPoint` and :class:`MoveEvent`.

    :class:`StaticPoint` can be a stop at a time, or just a random point where an agent can "get in" and "get out."

    :class:`MoveEvent` are the transition events from a :class:`StaticPoint` to another :class:`StaticPoint`.
    For example, an agent can **walk** from a random :class:`StaticPoint` to a stop as :class:`StaticPoint`.

    Check the corresponding documnetations for further details.
    """

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
    def path_head_coord(self) -> Tuple[float, float]:
        """
        Get the coordinate of the point at the path head.

        :raises ValueError: if the path is empty
        """
        if not self._points:
            raise ValueError("Path is empty")

        return self._points[0].coordinate

    @property
    def path_tail_coord(self) -> Tuple[float, float]:
        """
        Get the coordinate of the point at the path tail.

        :raises ValueError: if the path is empty
        """
        if not self._points:
            raise ValueError("Path is empty")

        return self._points[-1].coordinate

    @property
    def traveled_distance(self) -> float:
        """Get the total distance traveled in **km**."""
        return sum(event.traveled_dist for event in self._events if event)

    @property
    def displacement(self) -> float:
        """Get the displacement in **km**."""
        return distance(self.path_head_coord, self.path_tail_coord)

    @staticmethod
    def from_single_point(start_pt: StaticPoint) -> "SimPath":
        """Initialize a path from a single starting point."""
        return SimPath([start_pt], [None])
