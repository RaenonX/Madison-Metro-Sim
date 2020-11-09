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

    # Get the possible paths
    possible_paths = sim_map.get_possible_paths()

    print(f"The map contains {sim_map.point_count} points. There are {len(possible_paths)} possible paths.")
    print()

    # Get distance metrics and print it
    name_dist = "Distance traveled for each simulated path"
    metrics_dist = SimulationMap.distance_metrics(possible_paths, name=name_dist)
    metrics_dist.print_stats()

    # ---- > 1 km only
    name_dist += " (> 1 km)"
    metrics_dist = metrics_dist.filtered(lambda data: data >= 1, name_dist)
    metrics_dist.print_stats()

    # Get displacement metrics and print it
    name_disp = "Displacement for each simulated path"
    metrics_disp = SimulationMap.displacement_metrics(possible_paths, name=name_disp)
    metrics_disp.print_stats()

    # ---- > 1 km only
    name_disp += " (> 1 km)"
    metrics_disp = metrics_disp.filtered(lambda data: data >= 1, name_disp)
    metrics_disp.print_stats()
