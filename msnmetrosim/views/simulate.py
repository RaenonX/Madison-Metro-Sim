"""Main script to construct and run a simulation."""
from datetime import datetime

from .controllers import ctrl_calendar, ctrl_stops, ctrl_stop_schedule, ctrl_trips
from .sim_graph import SimulationStaticPoints, StaticPointConfig, SimulationMap, SimulationConfig

__all__ = ("test_run",)


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
