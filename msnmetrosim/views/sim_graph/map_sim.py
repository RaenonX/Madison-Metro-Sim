"""Main simulation map."""
from collections import Counter
from dataclasses import dataclass, field
from datetime import timedelta, datetime
from typing import Set, Dict, List, Optional, Counter as CounterType

from msnmetrosim.controllers import MMTStopDataController
from msnmetrosim.models import MMTStop
from msnmetrosim.utils import travel_time, distance, normalize_cumulate_vector, DataMetrics
from .config import SimulationConfig, PathDiscoveryConfig
from .event_move import MoveEvent, MoveEventType
from .event_static import StaticPoint, ScheduledStop, StopWait
from .map_points import SimulationStaticPoints
from .path import SimPath, PathDiscoveryResult as SimPathDiscoveryResult

__all__ = ("SimulationMap", "PathDiscoveryResult")


@dataclass
class PathDiscoveryResult:
    """Result of the path discovery of a :class:`SimulationMap`."""

    # pylint: disable=too-many-instance-attributes

    paths: List[SimPath] = field(default_factory=list)
    path_move_distribution: CounterType[MoveEventType] = field(default_factory=Counter)
    trip_count_distribution: CounterType[int] = field(default_factory=Counter)

    count_discovered: int = 0
    count_frontier: int = 0

    total_pruned: int = 0
    total_detoured: int = -1  # -1 means not completed. This will only being updated upon completed (attach_path)

    prev_discovered: int = field(init=False, default=0)
    prev_frontier: int = field(init=False, default=0)

    @property
    def trip_count_distribution_cdf(self):
        """Get the trip count distribution as CDF data in ``(X_ARRAY, Y_ARRAY)`` for plotting."""
        x_array = list(range(max(self.trip_count_distribution) + 1))
        y_array = [self.trip_count_distribution[trip_count] for trip_count in x_array]

        return x_array, normalize_cumulate_vector(y_array)

    def __repr__(self):
        edge_count = sum(self.path_move_distribution.values())

        struct_entries = [f'- {move_event}: {count} ({count / edge_count:.2%})'
                          for move_event, count in self.path_move_distribution.items()]
        struct_str = '\n'.join(struct_entries)

        return (f"{self.count_discovered} paths discovered.\t"
                f"{self.total_pruned} paths pruned.\t"
                f"{self.total_detoured} paths are detouring.\n"
                "------------------------------------------\n"
                f"Move event ratio:\n{struct_str}")

    def print_result(self, in_progress: bool = True):
        """Print the result. ``in_progress`` indicates if the discovery is still in progress."""
        if in_progress:
            self.print_in_progress()
        else:
            self.print_completed()

    def print_in_progress(self):
        """Print method to be called if the discovery is still in progress."""
        print(f"{self.count_discovered} paths discovered.\t"
              f"{self.count_frontier} paths in the frontier.\t"
              f"{self.count_discovered + self.count_frontier} paths guaranteed to be returned.\t"
              f"{self.total_pruned} paths pruned.")

    def print_completed(self):
        """Print method to be called if the discovery is completed."""
        print(self)

    def complete(self, paths: List[SimPath]):
        """
        Method to be called upon completion.

        This method will record the ``paths`` discovered and update some statistical parameters.
        """
        self.paths = paths

        self.count_discovered = len(paths)
        self.count_frontier = 0

        # Update path moving structure
        for path in paths:
            self.path_move_distribution.update(path.event_counter)
            self.trip_count_distribution[path.trip_count] += 1

        # Update detouring count
        self.total_detoured = sum(path.detouring for path in self.paths)

    def update(self, result: SimPathDiscoveryResult):
        """
        Update the path discovery result.

        This should be executed for each sim path discovery.
        """
        self.total_pruned += result.pruned

    def update_print(self, discovered: int, frontier: int, result: SimPathDiscoveryResult):
        """
        Update the path discovery result and print the result.

        This should be executed each time the result should be printed.

        The updated things are **not** overlapped with ``update()``, which means that if the result
        should be updated and printed, both this method and ``update()`` should be called.
        """
        self.prev_discovered = self.count_discovered
        self.prev_frontier = self.count_frontier

        self.count_discovered = discovered
        self.count_frontier = frontier

        self.total_pruned += result.pruned

        self.print_result(in_progress=True)

    @property
    def code_stats(self) -> str:
        """
        Get the code to recover this result for statistical purposes.

        The code assumes the discovery has been completed, and no actual paths will be included.
        """
        move_counter_item_str = [f"MoveEventType.{event_type.name}: {count}"
                                 for event_type, count in self.path_move_distribution.items()]
        move_counter = f"Counter({{{', '.join(move_counter_item_str)}}})"

        trip_counter_item_str = [f'{trip_count}: {path_count}'
                                 for trip_count, path_count in self.trip_count_distribution.items()]
        trip_counter = f"Counter({{{', '.join(trip_counter_item_str)}}})"

        return f"PathDiscoveryResult(" \
               f"path_move_distribution={move_counter}, trip_count_distribution={trip_counter}, " \
               f"count_discovered={self.count_discovered}, " \
               f"total_pruned={self.total_pruned}, total_detoured={self.total_detoured}" \
               f")"


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

    @property
    def point_count(self) -> int:
        """Get the estimated count of points in the map."""
        return self._point_count

    def _init_frontier_sequential(self, start_dt: datetime, end_dt: datetime, stop: ScheduledStop,
                                  static_points: SimulationStaticPoints, ctrl_stop: MMTStopDataController) \
            -> Dict[int, ScheduledStop]:
        ret: Dict[int, ScheduledStop] = {}

        if next_stop := stop.stop_sim.next_stop:
            next_stop_data = ctrl_stop.get_stop_by_id(next_stop.stop_id)
            if not next_stop_data:
                raise ValueError(f"Record of the stop ID {next_stop.stop_id} not exists")

            if next_scheduled_stop := static_points.get_next_scheduled_stop(start_dt, end_dt, next_stop.stop_id):
                # Unit in speed is km/h, but the distance traveled here is mile
                move_dist = (next_stop.shape_dist_traveled - stop.stop_sim.shape_dist_traveled) * 1.609

                trip_event = MoveEvent(
                    MoveEventType.BUS_TRIP,
                    (next_scheduled_stop.dt_in - stop.dt_out).total_seconds(),
                    move_dist
                )

                stop.add_next_point(trip_event, next_scheduled_stop)
                self._point_count += 1
                ret[id(next_scheduled_stop)] = next_scheduled_stop

        return ret

    def _init_frontier_wait(self, start_dt: datetime, end_dt: datetime, stop: ScheduledStop,
                            config: SimulationConfig, static_points: SimulationStaticPoints) \
            -> Dict[int, ScheduledStop]:
        ret: Dict[int, ScheduledStop] = {}

        wait_end_dt = min(
            stop.stop_sim.departure_time + timedelta(seconds=config.max_wait_time),
            end_dt
        )
        if scheduled_stop := static_points.get_next_scheduled_stop(start_dt, wait_end_dt, stop.stop_id):
            wait_time = (scheduled_stop.stop_sim.arrival_time - stop.stop_sim.arrival_time).total_seconds()

            if 0 < wait_time < config.max_wait_time:
                # The agent wait at the same place and ready to take the next bus
                stop.add_next_point(MoveEvent(MoveEventType.WAIT, wait_time, 0), scheduled_stop)
                self._point_count += 1

                ret[id(scheduled_stop)] = scheduled_stop

        return ret

    def _init_frontier_closest(self, start_dt: datetime, end_dt: datetime, stop: ScheduledStop,
                               config: SimulationConfig, static_points: SimulationStaticPoints,
                               ctrl_stop: MMTStopDataController) \
            -> Dict[int, ScheduledStop]:
        # pylint: disable=too-many-locals

        ret: Dict[int, ScheduledStop] = {}

        for stop_dist_data in ctrl_stop.find_data_order_by_dist(*stop.coordinate):
            if stop_dist_data.distance > config.max_walk_distance:
                break  # Beyond max walking distance

            if stop_dist_data.distance == 0:
                continue  # No need to walk

            scheduled_stop = static_points.get_next_scheduled_stop(start_dt, end_dt, stop_dist_data.data.stop_id)
            if not scheduled_stop:
                continue  # Next scheduled stop unavailable

            walk_time = travel_time(config.walk_speed, stop_dist_data.distance)

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
                stop.add_next_point(MoveEvent(MoveEventType.WALK, walk_time, stop_dist_data.distance), stop_wait)
                self._point_count += 1

            parent_pt.add_next_point(wait_event, scheduled_stop)
            self._point_count += 1
            ret[id(scheduled_stop)] = scheduled_stop

        return ret

    def _init_handle_frontier_stop(self, stop: ScheduledStop, config: SimulationConfig,
                                   static_points: SimulationStaticPoints, ctrl_stop: MMTStopDataController) \
            -> Dict[int, ScheduledStop]:
        ret: Dict[int, ScheduledStop] = {}

        start_dt = stop.stop_sim.departure_time
        end_dt = static_points.config.end_dt

        # Path discovery pruning will not be performed here.
        # Instead, the pruning process will be executed during ``get_possible_paths_top_down()``.

        # Sequential (on bus to next)
        ret.update(self._init_frontier_sequential(start_dt, end_dt, stop, static_points, ctrl_stop))

        # Wait until the next bus
        ret.update(self._init_frontier_wait(start_dt, end_dt, stop, config, static_points))

        # Walk to closest
        ret.update(self._init_frontier_closest(start_dt, end_dt, stop, config, static_points, ctrl_stop))

        return ret

    def _init_starting_frontier(self, config: SimulationConfig, static_points: SimulationStaticPoints,
                                ctrl_stop: MMTStopDataController):
        frontier: Dict[int, StaticPoint] = {}

        starting_stops: List[MMTStop] = ctrl_stop.get_stops_within_range(*config.start_coord, config.max_walk_distance)

        # Agents walk to the stops and wait for the bus
        # -- Even if the starting point is right on a stop, a walking event will still being created
        for stop in starting_stops:
            walk_distance = distance(config.start_coord, stop.coordinate)
            walk_time = travel_time(config.walk_speed, walk_distance)

            stop_arrival_dt = static_points.start_dt + timedelta(seconds=walk_time)
            end_dt = static_points.config.end_dt

            if next_scheduled_stop := static_points.get_next_scheduled_stop(stop_arrival_dt, end_dt, stop.stop_id):
                next_scheduled_stop: ScheduledStop

                # Wait parameters
                stop_wait = StopWait(stop_arrival_dt, next_scheduled_stop.stop_sim.arrival_time,
                                     next_scheduled_stop.stop_sim, next_scheduled_stop.coordinate)
                wait_time = (next_scheduled_stop.stop_sim.arrival_time - stop_arrival_dt).total_seconds()

                # The agent walks to the stop
                self._start.add_next_point(MoveEvent(MoveEventType.WALK, walk_time, walk_distance), stop_wait)

                # The agent waits at the stop
                stop_wait.add_next_point(MoveEvent(MoveEventType.WAIT, wait_time, 0), next_scheduled_stop)

                frontier[id(next_scheduled_stop)] = next_scheduled_stop

        return frontier

    def __init__(self, config: SimulationConfig, static_points: SimulationStaticPoints,
                 ctrl_stop: MMTStopDataController):
        self._start = StaticPoint(static_points.start_dt, static_points.start_dt, config.start_coord)

        self._point_count = 1  # For statistical purpose only

        self._config = config

        # Get the starting stops of the simulation
        frontier: Dict[int, StaticPoint] = self._init_starting_frontier(config, static_points, ctrl_stop)
        frontier_past: Set[int] = set(frontier.keys())

        counter: int = 0  # For progress reporting

        # Generate other edges
        while frontier:
            if counter % 20 == 0:  # Report every 20 iterations
                print(f"Generating the map... (#{counter} / {len(frontier)} in frontier)")

            _, stop = frontier.popitem()

            if isinstance(stop, ScheduledStop):
                frontiers = self._init_handle_frontier_stop(stop, config, static_points, ctrl_stop)

                # Remove already-traversed entries
                for id_past in frontier_past:
                    frontiers.pop(id_past, None)

                frontier_past.update(frontiers.keys())  # Record that the frontiers are traversed
                frontier.update(frontiers)

            counter += 1

    def __str__(self):
        return f"<Simulation map: {self._point_count}>"

    def __repr__(self):
        return str(self)

    def get_possible_paths_top_down(self, /, config: Optional[PathDiscoveryConfig] = None) \
            -> PathDiscoveryResult:
        """
        Get all possible paths of the map.

        Path discovery will be executed top-down, which means that the path discovery starts from the root.

        Advantages:

        - All paths are guaranteed to be found.

        Disadvantages:

        - Expensive.

        :param config: path discovery config
        """
        discovery_result = PathDiscoveryResult()

        # Build config
        if not config:
            config = PathDiscoveryConfig()
        config.update_with_sim_config(self._config)

        # BFS is used
        ret: List[SimPath] = []
        cur: List[SimPath] = [SimPath.from_single_point(self._start)]

        counter = 0  # Iteration counter

        while cur:
            cur_path = cur.pop(0)

            # Find paths
            result = cur_path.get_possible_next_paths(config)

            # Add paths
            if result.paths:
                cur.extend(result.paths)
            else:
                ret.append(cur_path)

            # Progress reporting
            discovery_result.update(result)

            if counter % 2000 == 0:
                discovery_result.update_print(len(ret), len(cur), result)
            counter += 1

        # Attach paths to the result to be returned
        discovery_result.complete(ret)

        return discovery_result

    @staticmethod
    def distance_metrics(paths: List[SimPath], /, name: Optional[str] = None) -> DataMetrics:
        """
        Get the metrics of the traveled distance.

        .. note::
            The difference between distance and displacement is that distance counts for every bends, whereas
            displacement only calculates the distance between the start point and the end point.

            Demo image: https://i.imgur.com/gORT9Sy.png
        """
        return DataMetrics([path.traveled_distance for path in paths], name)

    @staticmethod
    def displacement_metrics(paths: List[SimPath], /, name: Optional[str] = None) -> DataMetrics:
        """
        Get the metrics of the displacements of the paths.

        .. note::
            The difference between distance and displacement is that distance counts for every bends, whereas
            displacement only calculates the distance between the start point and the end point.

            Demo image: https://i.imgur.com/gORT9Sy.png
        """
        return DataMetrics([path.displacement for path in paths], name)
