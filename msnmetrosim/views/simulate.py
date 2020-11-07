"""Main script to construct and run a simulation."""
from datetime import datetime

from .controllers import ctrl_calendar, ctrl_stops, ctrl_stop_schedule, ctrl_trips
from .sim_graph import SimulationStaticPoints, StaticPointConfig, SimulationMap, SimulationConfig

__all__ = ("test_run",)


def test_run():
    """
    This method is just for demonstration purposes.

    You should be able to find some usages (definitely not all) here.
    """
    # Configure the simulation
    config_points = StaticPointConfig(
        start_dt=datetime(2020, 9, 2, 15),
        max_travel_time=1800
    )
    config_sim = SimulationConfig(
        start_coord=(43.069451, -89.401168),
        bus_speed=30,
        walk_speed=4.2,
        max_walk_distance=1,
        max_wait_time=900
    )

    # Generate static points and the simulation map
    sim_points = SimulationStaticPoints(config_points, ctrl_calendar, ctrl_stops, ctrl_stop_schedule, ctrl_trips)
    sim_map = SimulationMap(config_sim, sim_points, ctrl_stops)

    # Get the possible paths and its related metrics
    possible_paths = sim_map.get_possible_paths()
    metrics = SimulationMap.accessibility_metrics(possible_paths, name="Distance traveled for each simulated path")
    farthest_points = {path.path_tail_coord for path in possible_paths}  # Using set to get distince values

    # Print out the results
    print(f"The map contains {sim_map.point_count} points. There are {len(possible_paths)} possible paths.")
    print()

    metrics.print_stats()

    print("Random 10 farthest points reached among the paths:")
    for _, point in zip(range(10), farthest_points):
        # Refer to the prototype for plotting these points
        #   https://github.com/RaenonX/Madison-Metro-Sim/blob/prototype/Chang/test.ipynb
        #   https://github.com/RaenonX/Madison-Metro-Sim/blob/prototype/Chang/graph.py
        print(point)
