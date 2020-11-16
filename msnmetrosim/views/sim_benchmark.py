"""Scripts to benchmark the simulation."""
import time
from collections import Counter
from dataclasses import dataclass
from datetime import datetime
from typing import Tuple, List, Callable, Optional, Iterable

from msnmetrosim.utils import plot_twin_y, plot_single, plot_multiple, plot_discrete_distribution_normalized
from .controllers import ctrl_calendar, ctrl_stops, ctrl_stop_schedule, ctrl_trips
from .sim_graph import (
    StaticPointConfig, SimulationConfig,
    SimulationStaticPoints, SimulationMap,
    PathDiscoveryResult, MoveEventType
)

__all__ = (
    # Benchmarking function
    "benchmark_map_construction",
    # Plotting function
    "plot_travel_time_x_proc_time_n_count", "plot_point_x_proc_time", "plot_point_x_t_each_point",
    "plot_point_count_x_proc_time_detailed", "plot_point_count_x_gen_static",
    "plot_path_distribution", "plot_path_move_event_distribution", "plot_trip_count_cdf",
    # Historical data
    "post_152f1000_pruned_no_detouring"
)


@dataclass
class BenchmarkResult:
    """A single benchmarking result."""

    travel_time: float

    point_count: int
    path_top_down: PathDiscoveryResult

    t_gen_static: float
    """Time spent on generating the static points in seconds."""
    t_gen_map: float
    """Time spent on generating the simulation map in seconds."""
    t_path_top_down: float
    """Time spent on generating the paths (top-down) in seconds."""
    t_map_action: float
    """Time spent on map action (0 if not defined) in seconds."""

    def __repr__(self):
        return f"Benchmarking result @ travel time = {self.travel_time} secs\n" \
               f"\n" \
               f"# Summary\n" \
               f"\n" \
               f"- Map point #: {self.point_count}\n" \
               f"- Map path # (top-down): {len(self.path_top_down.paths)}\n" \
               f"- T point generation: {self.t_gen_static:.6f} secs\n" \
               f"- T map generation: {self.t_gen_map:.6f} secs\n" \
               f"- T path generation (top-down): {self.t_path_top_down:.6f} secs\n" \
               f"- T map action: {self.t_map_action:.6f} secs\n" \
               f"- T total: {self.t_total:.6f} secs\n" \
               f"- T for each point: {self.t_each_point:.6f} secs\n" \
               f"- T for each path: {self.t_each_path_top_down:.6f} secs\n" \
               f"\n" \
               f"# Path discovery result (top-down)\n" \
               f"\n" \
               f"{self.path_top_down}\n" \
               f"\n" \
               f"Easycode: " \
               f"BenchmarkResult(" \
               f"{self.travel_time}, {self.point_count}, {self.path_top_down.code_stats}, " \
               f"{self.t_gen_static}, {self.t_gen_map}, {self.t_path_top_down}, {self.t_map_action}" \
               f")"

    @property
    def t_total(self) -> float:
        """Get the total time spent on the whole simulation process in seconds."""
        return self.t_gen_static + self.t_gen_map + self.t_map_action

    @property
    def t_each_point(self) -> float:
        """Get the average time spent on a single static point in seconds."""
        return self.t_total / self.point_count

    @property
    def t_each_path_top_down(self) -> float:
        """Get the average time spent on generating a single top-down path in seconds."""
        return self.t_path_top_down / len(self.path_top_down.paths)


# region Benchmark historical data

post_152f1000_pruned_no_detouring = BenchmarkResult(
    2700, 11524,
    PathDiscoveryResult(
        path_move_distribution=Counter({
            MoveEventType.WALK: 992585, MoveEventType.WAIT: 992585, MoveEventType.BUS_TRIP: 2917370
        }),
        trip_count_distribution=Counter({
            1: 19, 2: 1904, 3: 23313, 4: 60674, 5: 66791, 6: 45409, 7: 12185, 8: 3715, 9: 2707, 10: 127
        }),
        count_discovered=216844, total_pruned=257809, total_detoured=0),
    0.024932146072387695, 18.663077116012573, 46.5826051235199, 0
)

# endregion


def benchmark_map_construction(start_dt: datetime, travel_time_list: Iterable[float],
                               start_coord: Tuple[float, float], /,
                               prune_non_sense: bool = True, with_detoured: bool = False,
                               max_transfer: int = -1,
                               walk_speed: float = 4.2, max_walk_distance: float = 0.7,
                               max_wait_time: float = 900,
                               map_action: Optional[Callable[[SimulationMap], None]] = None) \
        -> List[BenchmarkResult]:
    """
    Benchmark the simulation map construction time.

    :param start_dt: simulation starting time.
    :param travel_time_list: list of max travel time to create simulation maps
    :param start_coord: coordinate of the starting point
    :param prune_non_sense: prune any non-sense paths. Check the doc of :class:`SimulationConfig` for the definition
    :param with_detoured: if the detouring paths should be included
    :param max_transfer: max # of transfers allowed
    :param walk_speed: walking speed in km/h
    :param max_walk_distance: maximum walking distance in km
    :param max_wait_time: maximum waiting time in seconds
    :param map_action: action to be executed on the map
    """
    # pylint: disable=too-many-locals

    result = []

    for travel_time in travel_time_list:
        config_points = StaticPointConfig(start_dt=start_dt, max_travel_time=travel_time)
        config_sim = SimulationConfig(
            start_coord=start_coord, prune_non_sense=prune_non_sense, with_detoured=with_detoured,
            max_transfer=max_transfer,
            walk_speed=walk_speed, max_walk_distance=max_walk_distance,
            max_wait_time=max_wait_time,
        )

        # Point generation
        _start = time.time()
        print("Generating the points...")
        sim_points = SimulationStaticPoints(config_points, ctrl_calendar, ctrl_stops, ctrl_stop_schedule, ctrl_trips)
        _gen_static = time.time() - _start

        # Map generation
        _start = time.time()
        print("Generating the map...")
        sim_map = SimulationMap(config_sim, sim_points, ctrl_stops)
        _gen_map = time.time() - _start

        # Path generation
        _start = time.time()
        print("Generating the paths...")
        path_top_down = sim_map.get_possible_paths_top_down()
        _gen_path_top_down = time.time() - _start

        # Map action
        _map_act = 0
        if map_action:
            _start = time.time()
            print("Executing the map action...")
            map_action(sim_map)
            _map_act = time.time() - _start

        # Additional prints
        print()
        print("Path discovery result (top-down)")
        print(path_top_down)
        print()

        result.append(BenchmarkResult(travel_time, sim_map.point_count, path_top_down,
                                      _gen_static, _gen_map, _gen_path_top_down, _map_act))

    return result


# region Plotting functions


def plot_travel_time_x_proc_time_n_count(results: List[BenchmarkResult]):
    """Generate a plot which X is the travel time and Y is the benchmarking time and the point count."""
    # Sort data
    travel_time = []
    total_time = []
    point_count = []

    for result in results:
        travel_time.append(result.travel_time)
        total_time.append(result.t_total)
        point_count.append(result.point_count)

    # Plot data
    plot_twin_y(travel_time, "Max. Travel Time (s)", point_count, "Point count", total_time, "Process Time (s)",
                title="Travel Time x (Process Time & Point Count)")


def plot_point_x_proc_time(results: List[BenchmarkResult]):
    """Generate a plot which X is the point count and Y is the time spent on the whole benchmarking process."""
    # Sort data
    point_count = []
    total_time = []

    for result in results:
        total_time.append(result.t_total)
        point_count.append(result.point_count)

    # Plot data
    plot_single(point_count, "Point count", total_time, "Process Time (s)")


def plot_point_x_t_each_point(results: List[BenchmarkResult]):
    """Generate a plot which X is the point count and Y is the average time spent on a single point."""
    # Sort data
    point_count = []
    each_point = []

    for result in results:
        point_count.append(result.point_count)
        each_point.append(result.t_each_point)

    # Plot data
    plot_single(point_count, "Point count", each_point, "Time on each point (s)")


def plot_point_count_x_proc_time_detailed(results: List[BenchmarkResult]):
    """Generate a plot which X is the point count and Y is the benchmarking time in details."""
    # Sort data
    point_count = []
    t_static = []
    t_map = []
    t_total = []

    for result in results:
        point_count.append(result.point_count)
        t_static.append(result.t_gen_static)
        t_map.append(result.t_gen_map)
        t_total.append(result.t_total)

    # Plot data
    plot_multiple(
        point_count, "Point count",
        [
            ("Generate static points", "dashdot", t_static),
            ("Generate simulation map", "dashed", t_map),
            ("Total processing time", "solid", t_total)
        ],
        "Time spent (s)", "Processing Step", (0.6, 0.3),
        title="Processing time breakdown"
    )


def plot_point_count_x_gen_static(results: List[BenchmarkResult]):
    """Generate a plot which X is the point count and Y is time spent on generating static points."""
    # Sort data
    travel_time = []
    t_static = []

    for result in results:
        travel_time.append(result.travel_time)
        t_static.append(result.t_gen_static)

    # Plot data
    plot_single(
        travel_time, "Max. Travel Time (s)",
        t_static, "Time (s)",
        title="Time spent on generating static points"
    )


def plot_path_distribution(results: List[BenchmarkResult], names: List[str]):
    """Plot the path distribution across results as a normalized discrete distribution chart."""
    categories = [
        "Discovered #",
        "Pruned #",
        "Detoured #"
    ]

    plot_discrete_distribution_normalized(
        categories,
        {
            name: [
                result.path_top_down.count_discovered,
                result.path_top_down.total_pruned,
                result.path_top_down.total_detoured
            ]
            for result, name in zip(results, names)
        }
    )


def plot_path_move_event_distribution(results: List[BenchmarkResult], names: List[str]):
    """Plot the path distribution across results as a normalized discrete distribution chart."""
    categories = [
        "Walk",
        "Wait",
        "Bus Trip"
    ]

    plot_discrete_distribution_normalized(
        categories,
        {
            name: [
                result.path_top_down.path_move_distribution[MoveEventType.WALK],
                result.path_top_down.path_move_distribution[MoveEventType.WAIT],
                result.path_top_down.path_move_distribution[MoveEventType.BUS_TRIP]
            ]
            for result, name in zip(results, names)
        }
    )


def plot_trip_count_cdf(result: BenchmarkResult):
    """Plot the total trip count of paths in ``result`` as CDF."""
    trip_counts, percentiles = result.path_top_down.trip_count_distribution_cdf

    plot_single(trip_counts, "Trip Count #", percentiles, "Percentile", title="Trip Count # in paths")

# endregion
