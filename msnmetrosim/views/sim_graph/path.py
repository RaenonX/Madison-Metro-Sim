"""Implementations of a simulated path on the map."""
from collections import Counter
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from msnmetrosim.utils import distance
from .config import PathDiscoveryConfig
from .event_move import MoveEvent, MoveEventType
from .event_static import StaticPoint, ScheduledStop, StopBase

__all__ = ("SimPath", "PathDiscoveryResult")


@dataclass
class PathDiscoveryResult:
    """Result of a path discovery."""

    paths: List["SimPath"] = field(default_factory=list)
    pruned: int = 0

    def add_path(self, sim_path: "SimPath"):
        """Add ``sim_path`` as a newly discovered path."""
        self.paths.append(sim_path)


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

        self._counter_evt = Counter([event.event_type for event in events if event])

    def __str__(self):
        ret: List[str] = []

        for point, event in zip(self._points, self._events):
            ret.extend((str(point), str(event)))

        return " -> ".join(ret)

    def __repr__(self):
        return str(self)

    def get_possible_next_paths(self, config: PathDiscoveryConfig) \
            -> PathDiscoveryResult:
        """
        Get the possible next paths and the relative stats as a :class:`PathDiscoveryResult`.

        :param config: path discovery config
        """
        result: PathDiscoveryResult = PathDiscoveryResult()

        last_pt: StaticPoint = self._points[-1]
        last_evt: MoveEvent = self._events[-1]

        for transition_evt, next_pt in last_pt.next_points:
            # Prune non-sense paths
            if config.prune_non_sense:
                if last_evt:  # Root point does not have previous event
                    if transition_evt.event_type == MoveEventType.WAIT and last_evt.event_type == MoveEventType.WAIT:
                        # Waiting at the bus stop twice doesn't make sense
                        result.pruned += 1
                        continue
                    if transition_evt.event_type == MoveEventType.WALK and last_evt.event_type == MoveEventType.WAIT:
                        # Waiting the bus but then walk to the next closest stop doesn't make sense
                        result.pruned += 1
                        continue
                    if transition_evt.event_type == MoveEventType.WALK and last_evt.event_type == MoveEventType.WALK:
                        # Walk to the closest stop but then walk to the next closest doesn't make sense
                        result.pruned += 1
                        continue
                if any(isinstance(pt, ScheduledStop) and pt.is_same_stop(next_pt) for pt in self._points):
                    # Same stop appearing twice in the path
                    result.pruned += 1
                    continue

            path = SimPath(self._points + [next_pt], self._events + [transition_evt])

            # Max transfer check
            if 0 <= config.max_transfer < path.trip_count - 1:
                # Beyond the max transfer limit
                continue

            # Detouring path inclusion check
            if config.with_detoured or not path.detouring:
                result.add_path(path)

        return result

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

    @property
    def detouring(self) -> bool:
        """
        Check if the path is detouring.

        Check the documentation of :class:`SimulationConfig` for the definition of detouring.
        """
        return self.traveled_distance > self.displacement * 3

    @property
    def event_counter(self) -> Counter:
        """Get the distribution of the move event of this path."""
        return self._counter_evt

    @property
    def trip_count(self):
        """Get the count of bus trips included in this path."""
        return len(set(pt.trip_id for pt in self._points if isinstance(pt, StopBase)))

    @staticmethod
    def from_single_point(start_pt: StaticPoint) -> "SimPath":
        """Initialize a path from a single starting point."""
        return SimPath([start_pt], [None])
