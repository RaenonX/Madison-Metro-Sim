"""
Controller of the MMT GTFS stop data.

The complete MMT GTFS dataset can be downloaded here:
http://transitdata.cityofmadison.com/GTFS/mmt_gtfs.zip
"""
from typing import List, Dict, Generator

from msnmetrosim.controllers.base import CSVLoadableController
from msnmetrosim.models import MMTStop

__all__ = ("MMTStopDataController",)


class MMTStopDataController(CSVLoadableController):
    """
    MMT stop data controller.

    Data file that will use this controller:
    - mmt_gtfs/stops.csv
    """

    def _init_dict_by_id(self, stop: MMTStop):
        # Assuming ``stop_id`` is unique
        self._dict_by_id[stop.stop_id] = stop

    def __init__(self, stops: List[MMTStop]):
        super().__init__(stops)

        self._dict_by_id: Dict[int, MMTStop] = {}

        # Create a dict with ID as key and stop data entry as value
        for stop in stops:
            self._init_dict_by_id(stop)

    def get_all_stops(self) -> Generator[MMTStop, None, None]:
        """Get all the stops in the loaded data."""
        for stop in self._dict_by_id.values():
            yield stop

    @staticmethod
    def on_row_read(row: List[str]) -> object:
        return MMTStop.parse_from_row(row)
