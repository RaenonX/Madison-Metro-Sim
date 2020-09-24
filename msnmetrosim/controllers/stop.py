"""
Controller of the MMT GTFS stop data.

The complete MMT GTFS dataset can be downloaded here:
http://transitdata.cityofmadison.com/GTFS/mmt_gtfs.zip
"""
from dataclasses import dataclass, field, InitVar
from math import isqrt
from typing import List, Dict, Tuple

from msnmetrosim.controllers.base import CSVLoadableController
from msnmetrosim.models import MMTStop

__all__ = ("MMTStopDataController",)


@dataclass
class ClosestStopResult:
    """Result of finding the closest stop."""

    stop: MMTStop

    lat: InitVar[float]
    lon: InitVar[float]

    distance: float = field(init=False)
    """Distance of the stop from ``(lat, lon)`` in km."""

    def __post_init__(self, lat: float, lon: float):
        self.distance = self.stop.distance(lat, lon)


class MMTStopDataController(CSVLoadableController):
    """
    MMT stop data controller.

    Data file that will use this controller:
    - mmt_gtfs/stops.csv
    """

    def _init_dict_by_id(self, stop: MMTStop):
        # Assuming ``stop_id`` is unique
        self._dict_by_id[stop.stop_id] = stop

    def _init_lat_idx(self, interval: int):
        # Find the starting points and its index
        starting_points = []

        for idx, stop in enumerate(self._data):
            if idx % interval == 0:
                starting_points.append((stop.lat, idx))

        # Get the starting and ending index for the corresponding starting latitude
        for idx in range(len(starting_points) - 1):
            starting_lat, starting_idx = starting_points[idx]
            _, ending_idx = starting_points[idx + 1]
            self._lat_idx.append((starting_lat, (starting_idx, ending_idx)))

        last_starting_lat, last_idx = starting_points[-1]
        self._lat_idx.append((last_starting_lat, (last_idx, len(self._data))))

    def __init__(self, stops: List[MMTStop]):
        # Sort the data by lat, lon
        stops = list(sorted(stops, key=lambda stop_data: stop_data.lat))

        super().__init__(stops)

        self._dict_by_id: Dict[int, MMTStop] = {}

        # Create a dict with ID as key and stop data entry as value
        for stop in stops:
            self._init_dict_by_id(stop)

        # Store the latitude-idx relationship for faster stop searching
        # elem #1: starting latitude
        # elem #2-1: starting index of `self._data` (inclusive)
        # elem #2-2: ending index `self._data` (exclusive)
        self._lat_idx: List[Tuple[float, Tuple[int, int]]] = []

        # Let the partition size and count to be as close as possible to maximize the efficiency on partitioned search
        # -------------------------------
        # Partition on 100 data
        #
        # Count # | Size # | Worst count of traversals
        #     100 |      1 |                       101
        #      50 |      2 |                        52
        #      25 |      4 |                        29
        #      20 |      5 |                        25
        #      10 |     10 |                        20
        #       5 |     20 |                        25
        #       4 |     25 |                        29
        #       2 |     50 |                        52
        #       1 |    100 |                       101
        self._init_lat_idx(isqrt(len(stops)))

    def get_stops_within_range(self, center_lat: float, center_lon: float, search_range: float) \
            -> List[MMTStop]:
        """
        Form a search box and return the stops inside it, including the stop right on the border of the box.

        The search box will be centered at ``(center_lat, center_lon)``,
        with the offset of ``search_range`` degree at max.

        Unit of ``search_range`` is degree (in latitude and longitude).
        """
        # Calculate the bounds
        lower_lat = center_lat - search_range
        upper_lat = center_lat + search_range
        lower_lon = center_lon - search_range
        upper_lon = center_lon + search_range

        # Get the partitioned stops for search
        stops_to_search: List[MMTStop] = []

        for start_lat, idx in self._lat_idx:
            start_idx, end_idx = idx

            if start_lat >= lower_lat:
                # Starting latitude fall within the lower latitude of the search box
                stops_to_search.extend(self._data[start_idx:end_idx])
            elif start_lat > upper_lat:
                # Early termination of the for-loop because the starting latitude
                # goes beyond the upper latitude of the search box
                break

        # Get the stops inside the search box
        stops_in_box: List[MMTStop] = []

        for stop in stops_to_search:
            if lower_lat <= stop.lat <= upper_lat and lower_lon <= stop.lon <= upper_lon:
                stops_in_box.append(stop)

        return stops_in_box

    def find_closest_stop(self, lat: float, lon: float) -> ClosestStopResult:
        """Find the closest stop around the location at ``(lat, lon)``."""
        # Early terminate on no valid stop data loaded (not possible to find the closest stop)
        if not self._data:
            raise ValueError("No stops loaded")

        # Set the initial search range to be 0.002 deg of latitude (~0.222 km / ~0.138 mi)
        search_range = 0.002

        # Find the candidate stops
        candidate_stops: List[MMTStop] = self.get_stops_within_range(lat, lon, search_range)

        # Expand the search range by the 1.5x of the original range if no valid candidate stops found
        while not candidate_stops:
            search_range *= 1.5
            candidate_stops = self.get_stops_within_range(lat, lon, search_range)

        # Get the shortest stop and return it as a result object
        return ClosestStopResult(min(candidate_stops, key=lambda stop: stop.distance(lat, lon)), lat, lon)

    @staticmethod
    def on_row_read(row: List[str]) -> object:
        return MMTStop.parse_from_row(row)
