"""Data controller for the ridership data grouped by stop."""
from typing import List, Dict, Optional

from msnmetrosim.controllers.base import CSVLoadableController
from msnmetrosim.models import RidershipByStop

__all__ = ("RidershipByStopController",)


class RidershipByStopController(CSVLoadableController):
    """
    Controller of the data of ridership by stop.

    Data file that will use this controller:
    - ridership/by_stop.csv
    """

    def _init_dict_by_id(self, stop_data: RidershipByStop):
        self._dict_by_id[stop_data.stop_id] = stop_data

    def __init__(self, stop_data_list: List[RidershipByStop]):
        super().__init__(stop_data_list)

        self._dict_by_id: Dict[int, RidershipByStop] = {}

        # Create a dict with stop ID as key and ridership data entry as value
        for stop_data in stop_data_list:
            self._init_dict_by_id(stop_data)

    def get_stop_data_by_id(self, stop_id: int) -> Optional[RidershipByStop]:
        """
        Get a stop data by its ID.

        Returns ``None`` if the data is not found.
        """
        return self._dict_by_id.get(stop_id)

    @staticmethod
    def on_row_read(row: List[str]) -> object:
        return RidershipByStop.parse_from_row(row)
