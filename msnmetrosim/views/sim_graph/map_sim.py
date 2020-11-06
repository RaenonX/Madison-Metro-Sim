"""Main simulation map."""
from dataclasses import dataclass
from datetime import timedelta
from typing import Tuple, Set, Dict, List

from msnmetrosim.controllers import MMTStopDataController
from msnmetrosim.models import MMTStop
from msnmetrosim.utils import travel_time, distance
from .event_move import MoveEvent, MoveEventType
from .event_static import StaticPoint, ScheduledStop, StopWait
from .map_points import SimulationStaticPoints

__all__ = ("SimulationMap", "SimulationConfig")


@dataclass
class SimulationConfig:
    """
    Configuration for a simulation.

    ``start_coord`` is the coordinate where the simulation starts.

    For movement event - bus trip
    =============================
    ``bus_speed`` is the bus traveling speed in **km/h**.

    For movement event - walk
    =========================
    ``walk_speed`` is the walking speed of an agent in **km/h**.
    ``max_walk_distance`` is the distance that an agent will walk to a stop in **km**.

    For movement event - wait
    =========================
    ``max_wait_time`` is the maximum wait time at a single stop in **seconds**.
    """

    start_coord: Tuple[float, float]

    # Movement - bus trip
    bus_speed: float

    # Movement - walk
    walk_speed: float
    max_walk_distance: float

    # Movement - wait
    max_wait_time: float


class SimulationMap:
    """
    A map for running the simulation with the given ``config``.

    The map itself is a graph, events are the edges of the map and the stops at a moment of a time as the nodes.
    This class only contains "nodes." Related image: https://i.imgur.com/qHnM8YV.jpeg.

    .. note::
        To let the users have the ability to change the travel settings without re-generating the whole map,
        stop schedules are separated from the main simulation map.

        Stop schedules are in :class:`SimulationStaticPoints`;
        the actual simulation map containing the events is :class:`SimulationMap`.
    """

    def _init_handle_frontier_stop(self, stop: ScheduledStop, config: SimulationConfig,
                                   static_points: SimulationStaticPoints, ctrl_stop: MMTStopDataController) \
            -> Dict[int, ScheduledStop]:
        ret: Dict[int, ScheduledStop] = {}

        start_dt = stop.stop_sim.departure_time
        end_dt = static_points.config.end_dt

        # Sequential (on bus to next)
        if next_stop := stop.stop_sim.next_stop:
            next_stop_data = ctrl_stop.get_stop_by_id(next_stop.stop_id)
            if not next_stop_data:
                raise ValueError(f"Record of the stop ID {next_stop.stop_id} not exists")

            if next_scheduled_stop := static_points.get_next_scheduled_stop(start_dt, end_dt, next_stop.stop_id):
                # Unit in speed is km/h, but the distance traveled here is mile
                move_dist = (next_stop.shape_dist_traveled - stop.stop_sim.shape_dist_traveled) * 1.609

                trip_event = MoveEvent(MoveEventType.BUS_TRIP, travel_time(config.bus_speed, move_dist), move_dist)

                stop.add_next_point(trip_event, next_scheduled_stop)
                self._point_count += 2
                ret[id(next_scheduled_stop)] = next_scheduled_stop

        # Wait until the next bus
        wait_end_dt = min(
            stop.stop_sim.departure_time + timedelta(seconds=config.max_wait_time),
            static_points.config.end_dt
        )
        if scheduled_stop := static_points.get_next_scheduled_stop(start_dt, wait_end_dt, stop.stop_id):
            wait_time = (scheduled_stop.stop_sim.arrival_time - stop.stop_sim.arrival_time).total_seconds()

            if 0 < wait_time < config.max_wait_time:
                # The agent wait at the same place and ready to take the next bus
                stop_wait = StopWait(stop.stop_sim.arrival_time, scheduled_stop.stop_sim.arrival_time,
                                     stop.stop_sim, stop.coordinate)

                stop.add_next_point(MoveEvent(MoveEventType.WALK, 0, 0), stop_wait)
                stop_wait.add_next_point(MoveEvent(MoveEventType.WAIT, wait_time, 0), scheduled_stop)
                self._point_count += 2

                ret[id(scheduled_stop)] = scheduled_stop

        # Walk to closest
        for stop_dist_data in ctrl_stop.find_data_order_by_dist(*stop.coordinate):
            if stop_dist_data.distance > config.max_walk_distance:
                break  # Beyond max walking distance

            if stop_dist_data.distance == 0:
                continue  # No need to walk

            scheduled_stop = static_points.get_next_scheduled_stop(start_dt, end_dt, stop_dist_data.data.stop_id)
            if not scheduled_stop:
                continue  # Next scheduled stop unavailable

            walk_time = travel_time(config.walk_speed, stop_dist_data.distance)
            walk_event = MoveEvent(MoveEventType.WALK, walk_time, stop_dist_data.distance)

            # Time of the agent arrived at the closest stop
            stop_arrival_dt = stop.stop_sim.departure_time + timedelta(seconds=walk_time)

            if stop_arrival_dt > static_points.config.end_dt:
                continue  # Beyond max travel time

            if stop_arrival_dt > scheduled_stop.stop_sim.arrival_time:
                continue  # Walked to the stop but the bus already departed

            wait_time = (scheduled_stop.stop_sim.arrival_time - stop_arrival_dt).total_seconds()

            if wait_time > config.max_wait_time:
                continue  # Beyond the max wait time

            wait_event = None
            parent_pt = stop
            if wait_time > 0:
                # Agent waits for some time
                wait_event = MoveEvent(MoveEventType.WAIT, wait_time, 0)
                stop_wait = StopWait(stop_arrival_dt, scheduled_stop.stop_sim.arrival_time,
                                     scheduled_stop.stop_sim, scheduled_stop.coordinate)

                parent_pt = stop_wait
                stop.add_next_point(walk_event, stop_wait)
                self._point_count += 1

            parent_pt.add_next_point(wait_event, scheduled_stop)
            self._point_count += 1
            ret[id(scheduled_stop)] = scheduled_stop

        return ret

    def __init__(self, config: SimulationConfig, static_points: SimulationStaticPoints,
                 ctrl_stop: MMTStopDataController):
        self._start = StaticPoint(static_points.start_dt, static_points.start_dt)

        self._point_count = 1  # For statistical purpose only

        # Get the starting stops of the simulation
        starting_stops: List[MMTStop] = ctrl_stop.get_stops_within_range(*config.start_coord, config.max_walk_distance)
        frontier_past: Set[int] = set()
        frontier: Dict[int, StaticPoint] = {}

        # Agents walk to the stops and wait for the bus
        # -- Even if the starting point is right on a stop, a walking event will still being created
        for stop in starting_stops:
            walk_distance = distance(config.start_coord, stop.coordinate)
            walk_time = travel_time(config.walk_speed, walk_distance)

            stop_arrival_dt = static_points.start_dt + timedelta(seconds=walk_time)
            end_dt = static_points.config.end_dt

            if next_scheduled_stop := static_points.get_next_scheduled_stop(stop_arrival_dt, end_dt, stop.stop_id):
                next_scheduled_stop: ScheduledStop

                # Walk parameters
                walk_event = MoveEvent(MoveEventType.WALK, walk_time, walk_distance)

                # Wait parameters
                stop_wait = StopWait(stop_arrival_dt, next_scheduled_stop.stop_sim.arrival_time,
                                     next_scheduled_stop.stop_sim, next_scheduled_stop.coordinate)
                wait_time = (next_scheduled_stop.stop_sim.arrival_time - stop_arrival_dt).total_seconds()
                wait_event = MoveEvent(MoveEventType.WAIT, wait_time, 0)

                # The agent walks to the stop
                self._start.add_next_point(walk_event, stop_wait)

                # The agent waits at the stop
                stop_wait.add_next_point(wait_event, next_scheduled_stop)

                frontier[id(next_scheduled_stop)] = next_scheduled_stop

        # Generate other edges
        while frontier:
            _, stop = frontier.popitem()

            if isinstance(stop, ScheduledStop):
                frontiers = self._init_handle_frontier_stop(stop, config, static_points, ctrl_stop)
                [frontiers.pop(id_past, None) for id_past in frontier_past]  # Remove already-traversed entries

                frontier_past.update(frontiers.keys())  # Record that the frontiers are traversed
                frontier.update(frontiers)

    def __str__(self):
        return f"<Simulation map: {self._point_count}>"

    def __repr__(self):
        return str(self)
