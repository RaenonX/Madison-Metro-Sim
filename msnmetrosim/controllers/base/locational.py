"""Base controller class for locational data."""
from abc import ABC
from dataclasses import dataclass, InitVar, field
from math import isqrt
from typing import List, Tuple, TypeVar

from msnmetrosim.models.base import LocationalModelBase
from .holder import DataListHolder

__all__ = ("ClosestDataResult", "LocationalDataController")

T = TypeVar("T", bound=LocationalModelBase)


@dataclass
class ClosestDataResult:
    """Result of finding the data closest to the given location at ``(lat, lon)``."""

    data: T

    lat: InitVar[float]
    lon: InitVar[float]

    distance: float = field(init=False)
    """Distance between ``source`` and ``(lat, lon)`` in km."""

    def __post_init__(self, lat: float, lon: float):
        self.distance = self.data.distance(lat, lon)


class LocationalDataController(DataListHolder, ABC):
    """Base class location data controller."""

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

    def __init__(self, data: List[T]):
        # Sort the data by lat, lon
        data = list(sorted(data, key=lambda location_data: location_data.lat))

        super().__init__(data)

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
        self._init_lat_idx(isqrt(len(data)))

    def get_data_within_range(self, center_lat: float, center_lon: float, search_range: float) -> List[T]:
        """
        Form a search box and return the coordinates inside or on it.

        The search box will be centered at ``(center_lat, center_lon)``, with the offset of ``search_range`` at max.

        Unit of ``search_range`` is degree (in latitude and longitude).
        """
        # Calculate the bounds
        lower_lat = center_lat - search_range
        upper_lat = center_lat + search_range
        lower_lon = center_lon - search_range
        upper_lon = center_lon + search_range

        # Get the partitioned data for search
        data_to_search: List[T] = []

        for start_lat, idx in self._lat_idx:
            start_idx, end_idx = idx

            if start_lat >= lower_lat:
                # Starting latitude fall within the lower latitude of the search box
                data_to_search.extend(self._data[start_idx:end_idx])
            elif start_lat > upper_lat:
                # Early termination of the for-loop because the starting latitude
                # goes beyond the upper latitude of the search box
                break

        # Get the data inside the search box
        data_in_box: List[T] = []

        for stop in data_to_search:
            if lower_lat <= stop.lat <= upper_lat and lower_lon <= stop.lon <= upper_lon:
                data_in_box.append(stop)

        return data_in_box

    def find_closest_data(self, lat: float, lon: float) -> ClosestDataResult:
        """Find the data closest to the location at ``(lat, lon)``."""
        # Early terminate on no valid locational data loaded (not possible to find the closest data)
        if not self._data:
            raise ValueError("No locational data loaded")

        # Set the initial search range to be 0.002 deg of latitude (~0.222 km / ~0.138 mi)
        search_range = 0.002

        # Find the candidate stops
        candidate_data: List[T] = self.get_data_within_range(lat, lon, search_range)

        # Expand the search range by the 1.5x of the original range if no valid candidate data found
        while not candidate_data:
            search_range *= 1.5
            candidate_data = self.get_data_within_range(lat, lon, search_range)

        # Get the closest data and return it as a result object
        candidate_data: List[ClosestDataResult] = [ClosestDataResult(candidate, lat, lon)
                                                   for candidate in candidate_data]
        return min(candidate_data, key=lambda data: data.distance)
