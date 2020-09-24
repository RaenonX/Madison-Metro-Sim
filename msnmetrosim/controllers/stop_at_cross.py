"""Controller of the MMT GTFS stops grouped by its located cross."""
from typing import Dict

from msnmetrosim.models import MMTStopsAtCross
from .base import DataListHolder
from .stop import MMTStopDataController

__all__ = ("MMTStopsAtCrossDataController",)


class MMTStopsAtCrossDataController(DataListHolder):
    """Controller of the MMT GTFS stops grouped by its located cross."""

    # To be removed after adding more public methods
    # pylint: disable=too-few-public-methods

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
