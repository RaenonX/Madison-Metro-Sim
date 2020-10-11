"""Controller of the MMT GTFS stops grouped by its located cross."""
from typing import Dict, Optional, List, Tuple, Iterable

from msnmetrosim.models import MMTStop, MMTStopsAtCross
from msnmetrosim.models.results import CrossStopRemovalResult
from msnmetrosim.utils import generate_points
from .base import LocationalDataController
from .stop import MMTStopDataController

__all__ = ("MMTStopsAtCrossDataController",)


class MMTStopsAtCrossDataController(LocationalDataController):
    """Controller of the MMT GTFS stops grouped by its located cross."""

    def _init_dict_street(self, stop_data: List[MMTStop]):
        # Create an intermediate grouping dict
        temp = {}

        for stop in stop_data:
            cross_id = stop.unique_cross_id
            if cross_id not in temp:
                temp[cross_id] = []

            temp[cross_id].append(stop)

        for cross_id, stops in temp.items():
            self._dict_street[cross_id] = MMTStopsAtCross(stops[0].primary, stops[0].secondary,
                                                          stops[0].wheelchair_accessible, stops)

    def __init__(self, stop_data: List[MMTStop]):
        self._dict_street: Dict[int, MMTStopsAtCross] = {}
        self._init_dict_street(stop_data)

        super().__init__(list(self._dict_street.values()))

    def get_grouped_stop_by_street_names(self, street_1: str, street_2: str) -> Optional[MMTStopsAtCross]:
        """
        Get the stop located at the cross of ``street_1`` and ``street_2``.

        Returns ``None`` if not found.
        """
        return self._dict_street.get(MMTStopsAtCross.calculate_hash(street_1, street_2))

    def get_metrics_of_single_stop_removal(self, street_1: str, street_2: str, agents: Iterable[Tuple[float, float]]) \
            -> CrossStopRemovalResult:
        """
        Get the accessibility difference metrics of removing a single stop at ``(street_1, street_2)``.

        ``agents`` is a list of coordinates representing each agent for calculating the distance metrics.

        :raises ValueError: if no stop is located at `(street_1, street_2)`
        """
        # Get the stop to be removed
        target_stop = self.get_grouped_stop_by_street_names(street_1, street_2)
        if not target_stop:
            raise ValueError(f"There are no stops located near the cross of {street_1} & {street_2}")

        self_no_target = self.duplicate(lambda data: data.unique_cross_id != target_stop.unique_cross_id)

        # Get the distance metrics
        metrics_before = self.get_distance_metrics_to_closest(
            agents, f"Before removing {target_stop.cross_name}")
        metrics_after = self_no_target.get_distance_metrics_to_closest(
            agents, f"After removing {target_stop.cross_name}")

        return CrossStopRemovalResult(target_stop, metrics_before, metrics_after)

    def get_all_stop_remove_results(self, range_km: float, interval_km: float) -> List[CrossStopRemovalResult]:
        """
        Try to remove each stops one by one, and return the results of the removal.

        This function uses ``msnmetrosim.utils.generate_points()``
         to generate simulated agents and to calculate the accessibility impact.

        The ``center_coord`` of ``msnmetrosim.utils.generate_points()`` will be the coordinates of the stop.

        Check the documentation of ``msnmetrosim.utils.generate_points()``
        for more information on ``range_km`` and ``interval_km``.

        WARNING: This method could be very expensive.

        For 1153 records, it takes ~5 mins to run.
        """
        # ThreadPoolExecutor won't help on performance boosting
        # OPTIMIZE: Try to reduce the calculation time of this
        #   - Each agent is expanding its circle to find the closest stop
        #   - Change the above to each stop expanding its circle to "touch" the closest agent instead?
        ret: List[CrossStopRemovalResult] = []

        total_count = len(self.all_data)

        for idx, stop in enumerate(self.all_data):
            print(f"{idx} / {total_count} ({idx / total_count:.2%})")

            stop: MMTStopsAtCross
            agents = generate_points(stop.coordinate, range_km, interval_km)

            rm_result = self.get_metrics_of_single_stop_removal(stop.primary, stop.secondary, agents)

            ret.append(rm_result)

        return ret

    @staticmethod
    def from_stop_controller(stop_ctrl: MMTStopDataController):
        """Create an :class:`MMTStopsAtCrossDataController` from :class:`MMTStopDataController`."""
        return MMTStopsAtCrossDataController(stop_ctrl.all_data)
