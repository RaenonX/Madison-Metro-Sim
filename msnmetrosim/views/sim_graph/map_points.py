"""Classes for the simluation map containing stop schedules at a moment."""
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import List, Optional

from msnmetrosim.controllers import (
    MMTCalendarController, MMTStopScheduleController, MMTTripDataController, MMTStopDataController
)
from .event_static import StaticPoint, ScheduledStop

__all__ = ("SimulationStaticPoints", "StaticPointConfig")


@dataclass
class StaticPointConfig:
    """
    Configurations for initializing simulation static points.

    ``start_dt`` is the starting time in the simulation. This is **NOT** the simulation execution starting time.

    ``max_travel_time`` is the maximum travel time for the whole trip in seconds.
    """

    start_dt: datetime

    max_travel_time: float

    @property
    def end_dt(self) -> datetime:
        """
        Get the ending time in the simulation.

        This is **NOT** the simulation execution ending time.
        """
        return self.start_dt + timedelta(seconds=self.max_travel_time)


class SimulationStaticPoints:
    """
    A middleware holding simulation stop schedules for generating a map.

    The map itself is a graph, events are the edges of the map and the stops at a moment of a time as the nodes.
    This class only contains "nodes." Related image: https://i.imgur.com/qHnM8YV.jpeg.

    Check the documentation of :class:`SimulationMap` for the complete usage.

    .. note::
        To let the users have the ability to change the travel settings without re-generating the whole map,
        stop schedules are separated from the main simulation map.

        Stop schedules are in :class:`SimulationStaticPoints`;
        the actual simulation map containing the events is :class:`SimulationMap`.
    """

    @property
    def config(self) -> StaticPointConfig:
        """Get the static point template configuration."""
        return self._config

    @property
    def start_dt(self) -> datetime:
        """The starting datetime of the simulation."""
        return self._config.start_dt

    def _init_static_points(self, config: StaticPointConfig, ctrl_calendar: MMTCalendarController,
                            ctrl_stop: MMTStopDataController, ctrl_stop_schedule: MMTStopScheduleController,
                            ctrl_trips: MMTTripDataController):
        # Get the running service on the date
        services = ctrl_calendar.get_services_by_date(config.start_dt)
        if not services:
            raise ValueError(f"No service plan found on {config.start_dt}")

        # Get the available trip IDs of the service plan
        trip_ids = ctrl_trips.get_trip_ids([service.service_id for service in services])

        # Get the stop schedules as :class:`ScheduledStop` (nodes)
        stop_schedules_sim = ctrl_stop_schedule.get_stop_schedule_sim_by_arrival(
            config.start_dt, config.max_travel_time, trip_ids=trip_ids)

        for stop_schedule_sim in stop_schedules_sim:
            stop_data = ctrl_stop.get_stop_by_id(stop_schedule_sim.stop_id)
            if not stop_data:
                raise ValueError(f"Stop data of ID {stop_schedule_sim.stop_id} not found")

            self._static_points.append(ScheduledStop.from_stop_schedule_sim(stop_schedule_sim, stop_data.coordinate))

    def _init_stop_by_arrival_hr(self):
        # Put the data into the "boxes"
        for static_point in self._static_points:
            if isinstance(static_point, ScheduledStop):
                self._stop_by_arrival_hr[static_point.stop_sim.arrival_time.hour].append(static_point)

        # Sort the data in the "boxes"
        for hour in range(24):
            self._stop_by_arrival_hr[hour] = list(sorted(self._stop_by_arrival_hr[hour],
                                                         key=lambda data: data.stop_sim.arrival_time))

    def __init__(self, config: StaticPointConfig, ctrl_calendar: MMTCalendarController,
                 ctrl_stop: MMTStopDataController, ctrl_stop_schedule: MMTStopScheduleController,
                 ctrl_trips: MMTTripDataController):
        self._config = config

        self._static_points: List[StaticPoint] = []
        self._init_static_points(config, ctrl_calendar, ctrl_stop, ctrl_stop_schedule, ctrl_trips)

        self._stop_by_arrival_hr: List[List[ScheduledStop]] = [[] for _ in range(24)]
        self._init_stop_by_arrival_hr()

    def __str__(self):
        return f"<Sim Static Points: {len(self._static_points)}>"

    def __repr__(self):
        return self.__str__()

    def get_next_scheduled_stop(self, start_dt: datetime, end_dt: datetime, stop_id: int) -> Optional[ScheduledStop]:
        """
        Get the next scheduled stop that arrives between ``start_dt`` and ``end_dt`` at ``stop_id``.

        Returns ``None`` if not found with the given conditions.
        """
        current_dt = start_dt

        while current_dt <= end_dt:
            for scheduled_stop in self._stop_by_arrival_hr[current_dt.hour]:
                if start_dt <= scheduled_stop.stop_sim.arrival_time <= end_dt and scheduled_stop.stop_id == stop_id:
                    return scheduled_stop

            current_dt += timedelta(hours=1)

        return None
