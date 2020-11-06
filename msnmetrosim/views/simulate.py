"""Main script to construct and run a simulation."""
import time
from datetime import datetime
from typing import Tuple, List, Dict, Callable, Optional

from .controllers import ctrl_calendar, ctrl_stops, ctrl_stop_schedule, ctrl_trips
from .sim_graph import SimulationStaticPoints, StaticPointConfig, SimulationMap, SimulationConfig

__all__ = ("test_run", "benchmark_map")


def test_run():
    """
    This is a useless method which creates some static points and a simulation map.

    This also prints the object ``repr`` of the simulation map, which gives you nothing informational.

    Alright, I will say this method is just for demonstration purposes.
    """
    config_points = StaticPointConfig(
        start_dt=datetime(2020, 11, 5, 20),
        max_travel_time=3600
    )
    config_sim = SimulationConfig(
        start_coord=(43.073249, -89.399256),
        bus_speed=30,
        walk_speed=4.2,
        max_walk_distance=1,
        max_wait_time=1800
    )

    sim_points = SimulationStaticPoints(config_points, ctrl_calendar, ctrl_stops, ctrl_stop_schedule, ctrl_trips)
    sim_map = SimulationMap(config_sim, sim_points, ctrl_stops)

    # TODO: simulate something?

    print(sim_map)


def benchmark_map(start_dt: datetime, travel_time_list: List[float], start_coord: Tuple[float, float], /,
                  bus_speed: float = 16.7, walk_speed: float = 4.2, max_walk_distance: float = 0.7,
                  max_wait_time: float = 900, map_action: Optional[Callable[[SimulationMap], None]] = None) \
        -> Dict[float, Tuple[float, float, float, float]]:
    """
    Benchmark the simulation map creation time and return the result.

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
    result = {}

    for travel_time in travel_time_list:
        config_points = StaticPointConfig(start_dt=start_dt, max_travel_time=travel_time)
        config_sim = SimulationConfig(start_coord=start_coord, bus_speed=bus_speed, walk_speed=walk_speed,
                                      max_walk_distance=max_walk_distance, max_wait_time=max_wait_time)

        _start = time.time()
        sim_points = SimulationStaticPoints(config_points, ctrl_calendar, ctrl_stops, ctrl_stop_schedule, ctrl_trips)
        _static_points = time.time() - _start

        _start = time.time()
        sim_map = SimulationMap(config_sim, sim_points, ctrl_stops)
        _map_gen = time.time() - _start

        _map_act = 0
        if map_action:
            _start = time.time()
            map_action(sim_map)
            _map_act = time.time() - _start

        result[travel_time] = (_static_points, _map_gen, _map_act, _static_points + _map_gen + _map_act)

    return result
