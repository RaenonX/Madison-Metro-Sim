"""Controller of the MMT GTFS stops grouped by its located cross."""
from typing import Dict, Optional

from msnmetrosim.models import MMTStopsAtCross
from .base import LocationalDataController
from .stop import MMTStopDataController

__all__ = ("MMTStopsAtCrossDataController",)


class MMTStopsAtCrossDataController(LocationalDataController):
    """Controller of the MMT GTFS stops grouped by its located cross."""

    def _init_dict_street(self, stop_ctrl: MMTStopDataController):
        # Create an intermediate grouping dict
        temp = {}

        for stop in stop_ctrl.all_data:
            cross_id = stop.unique_cross_id
            if cross_id not in temp:
                temp[cross_id] = []

            temp[cross_id].append(stop)

        for cross_id, stops in temp.items():
            self._dict_street[cross_id] = MMTStopsAtCross(stops[0].primary, stops[0].secondary, stops)

    def __init__(self, stop_ctrl: MMTStopDataController):
        self._dict_street: Dict[int, MMTStopsAtCross] = {}
        self._init_dict_street(stop_ctrl)

        super().__init__(list(self._dict_street.values()))

    def get_grouped_stop_by_street_names(self, street_1: str, street_2: str) -> Optional[MMTStopsAtCross]:
        """
        Get the stop located at the cross of ``street_1`` and ``street_2``.

        Returns ``None`` if not found.
        """
        return self._dict_street.get(MMTStopsAtCross.calculate_hash(street_1, street_2))
