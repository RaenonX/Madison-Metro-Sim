"""
Controller of the MMT GTFS stop data.

The complete MMT GTFS dataset can be downloaded here:
http://transitdata.cityofmadison.com/GTFS/mmt_gtfs.zip
"""
from typing import List, Dict, Optional

from msnmetrosim.models import MMTStop
from .base import CSVLoadableController, LocationalDataController

__all__ = ("MMTStopDataController",)


class MMTStopDataController(LocationalDataController, CSVLoadableController):
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

    def get_stops_within_range(self, center_lat: float, center_lon: float, range_km: float) \
            -> List[MMTStop]:
        """
        Form a search box and return the stops inside it, including the stop right on the border of the box.

        The search box will be centered at ``(center_lat, center_lon)``,
        with the offset of ``search_range`` degree at max.

        Unit of ``range_km`` is **km**.
        """
        ret: List[MMTStop] = []

        for close_data in self.find_data_order_by_dist(center_lat, center_lon):
            if close_data.distance > range_km:
                break
            ret.append(close_data.data)

        return ret

    def get_stop_by_id(self, stop_id: int) -> Optional[MMTStop]:
        return self._dict_by_id.get(stop_id)

    def find_closest_stop(self, lat: float, lon: float):
        """Find the closest stop around the location at ``(lat, lon)``."""
        return self.find_closest_data(lat, lon)

    @staticmethod
    def on_row_read(row: List[str]) -> object:
        return MMTStop.parse_from_row(row)
