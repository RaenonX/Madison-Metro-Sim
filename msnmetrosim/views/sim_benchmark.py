"""Scripts to benchmark the simulation."""
import time
from dataclasses import dataclass
from datetime import datetime
from typing import Tuple, List, Callable, Optional, Iterable

from msnmetrosim.utils import plot_twin_y, plot_single, plot_multiple
from .controllers import ctrl_calendar, ctrl_stops, ctrl_stop_schedule, ctrl_trips
from .sim_graph import SimulationStaticPoints, StaticPointConfig, SimulationMap, SimulationConfig

__all__ = (
    # Benchmarking function
    "benchmark_gen_map",
    # Plotting function
    "plot_travel_time_x_proc_time_n_count", "plot_point_x_proc_time", "plot_point_x_t_each_point",
    "plot_point_count_x_proc_time_detailed", "plot_point_count_x_gen_static",
    # Results
    "gen_map_only_df8d234f"
)


@dataclass
class BenchmarkResult:
    """A single benchmark result."""

    travel_time: float

    point_count: int

    t_gen_static: float
    """Time spent on generating the static points in seconds."""
    t_gen_map: float
    """Time spent on generating the simulation map in seconds."""
    t_map_action: float
    """Time spent on map action (0 if not defined) in seconds."""

    @property
    def t_total(self) -> float:
        """Get the total time spent on the whole simulation process in seconds."""
        return self.t_gen_static + self.t_gen_map + self.t_map_action

    @property
    def t_each_point(self) -> float:
        """Get the average time spent on a single static point in seconds."""
        return self.t_total / self.point_count


# region Benchmark historical data

gen_map_only_df8d234f = [
    BenchmarkResult(600, 27, 0.012966394424438477, 0.19547653198242188, 0.0),
    BenchmarkResult(1200, 645, 0.011996030807495117, 1.0157527923583984, 0.0),
    BenchmarkResult(1800, 1609, 0.014960050582885742, 2.6155025959014893, 0.0),
    BenchmarkResult(2400, 3885, 0.01795196533203125, 5.356820344924927, 0.0),
    BenchmarkResult(3000, 6433, 0.019953012466430664, 9.05177617073059, 0.0),
    BenchmarkResult(3600, 22417, 0.03193473815917969, 30.847532510757446, 0.0),
    BenchmarkResult(4200, 22421, 0.1326141357421875, 33.464784383773804, 0.0),
    BenchmarkResult(4800, 22445, 0.04787158966064453, 33.86271810531616, 0.0),
    BenchmarkResult(5400, 22595, 0.041914939880371094, 37.05706524848938, 0.0),
    BenchmarkResult(6000, 31901, 0.04089713096618652, 53.27586364746094, 0.0),
    BenchmarkResult(6600, 45181, 0.060837507247924805, 72.06372404098511, 0.0),
    BenchmarkResult(7200, 73211, 0.06484675407409668, 112.55039048194885, 0.0),
]
"""
The simulation result of the commit after ``df8d234f``. This only generates the map with different travel time.

The result is based on the following configuration:
- Starting coordinate: (43.069451, -89.401168)
- Starting time: 2020/09/02 PM 3:00 CDT
- Bus Movement Speed: 16.7 km/h (10.38 mi)
- Walking Speed: 4.2 km/h (2.610 mi)
- Max. Walking Distance: 0.7 km (0.435 mi)
- Max. Waiting Time: 900 s (15 mins)
"""


# endregion


def benchmark_gen_map(start_dt: datetime, travel_time_list: Iterable[float], start_coord: Tuple[float, float], /,
                      bus_speed: float = 16.7, walk_speed: float = 4.2, max_walk_distance: float = 0.7,
                      max_wait_time: float = 900, map_action: Optional[Callable[[SimulationMap], None]] = None) \
        -> List[BenchmarkResult]:
    """
    Benchmark the simulation map generation time.

    The key of the return is the travel time used for benchmarking;
    the value of the return is:

    - Time spent on generating static points

    - Time spent on generating the map

    - Time spent on ``map_action`` function execution

    - Total time spent on the whole process

    :param start_dt: simulation starting time.
    :param travel_time_list: list of max travel time to create simulation maps
    :param start_coord: coordinate of the starting point
    :param bus_speed: bus moving speed in km/h
    :param walk_speed: walking speed in km/h
    :param max_walk_distance: maximum walking distance in km
    :param max_wait_time: maximum waiting time in seconds
    :param map_action: action to be executed on the map.
    """
    # pylint: disable=too-many-locals

    result = []

    for travel_time in travel_time_list:
        config_points = StaticPointConfig(start_dt=start_dt, max_travel_time=travel_time)
        config_sim = SimulationConfig(start_coord=start_coord, bus_speed=bus_speed, walk_speed=walk_speed,
                                      max_walk_distance=max_walk_distance, max_wait_time=max_wait_time)

        _start = time.time()
        sim_points = SimulationStaticPoints(config_points, ctrl_calendar, ctrl_stops, ctrl_stop_schedule, ctrl_trips)
        _gen_static = time.time() - _start

        _start = time.time()
        sim_map = SimulationMap(config_sim, sim_points, ctrl_stops)
        _gen_map = time.time() - _start

        _map_act = 0
        if map_action:
            _start = time.time()
            map_action(sim_map)
            _map_act = time.time() - _start

        result.append(BenchmarkResult(travel_time, sim_map.point_count, _gen_static, _gen_map, _map_act))

    return result


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
