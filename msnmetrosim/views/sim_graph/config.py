"""Simulation config objects."""
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Tuple, Optional

__all__ = ("SimulationConfig", "PathDiscoveryConfig", "StaticPointConfig")


@dataclass
class SimulationConfig:
    """
    Configuration for a simulation.

    ``start_coord`` is the coordinate where the simulation starts.

    ``with_detoured`` determines if the result should include any detouring paths.

        The definition of a detouring path is ``travel distance > displacement x 2``,
        because in general, people won't have a long traveling distance to only have a small displacement.

    ``prune_non_sense`` determines if the non-sense paths should be pruned.

        Path that matches any of the conditions below will be pruned:

        - Same stop appearing twice or more in a path

        - Consecutively waiting at the stop twice

        - Waiting at the stop then walk to the next closest stop

        - Consecutively walk to the next closest stop twice

    For movement event - bus trip
    =============================
    ``max_transfer`` is the max transfers allowed.

    For movement event - walk
    =========================
    ``walk_speed`` is the walking speed of an agent in **km/h**.

    ``max_walk_distance`` is the distance that an agent will walk to a stop in **km**.

    For movement event - wait
    =========================
    ``max_wait_time`` is the maximum wait time at a single stop in **seconds**.

    .. note::
        Bus speed is not included because it's determined by the schedule.
    """

    start_coord: Tuple[float, float]
    prune_non_sense: bool = True
    with_detoured: bool = False

    # Movement - bus trip
    max_transfer: int = -1  # -1 means unlimited

    # Movement - walk
    walk_speed: float = 4.2
    max_walk_distance: float = 1

    # Movement - wait
    max_wait_time: float = 900


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


@dataclass
class PathDiscoveryConfig:
    """
    Config for path discovery.

    ``prune_non_sense`` determines if the non-sense paths should be pruned.

    - Check the documentation of :class:`SimulationConfig` for the pruning criteria.

    ``with_detoured`` determines if the detouring paths should be included.

    - Check the documentation of :class:`SimulationConfig` for the detouring definition.

    ``max_transfer`` will limit the transfer count if this is set to a positive number.

    - ``-1`` means unlimited.

    ``no_walk_transfer`` determines if walking to the closest stop for transfer is allowed.
    """

    # Path
    prune_non_sense: Optional[bool] = None
    with_detoured: Optional[bool] = None

    # Bus trip related
    max_transfer: Optional[int] = -1

    def update_with_sim_config(self, config: SimulationConfig):
        """
        Update the path discovery config with the simulation config.

        If the value is not set (``None`` or ``-1``), the value in ``config`` will be used.

        Otherwise, the value in this config will be used.
        """
        self.prune_non_sense = config.prune_non_sense if self.prune_non_sense is None else self.prune_non_sense
        self.with_detoured = config.with_detoured if self.with_detoured is None else self.with_detoured
        self.max_transfer = self.max_transfer if self.max_transfer > 0 else config.max_transfer
