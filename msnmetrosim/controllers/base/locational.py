"""Base controller class for locational data."""
from abc import ABC
from dataclasses import dataclass, InitVar, field
from math import isqrt
from typing import List, Tuple, TypeVar, Optional, Generator, Set

from msnmetrosim.models.base import LocationalModelBase
from msnmetrosim.utils import DataMetrics
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

    def get_distance_metrics_to_closest(self, coords: List[Tuple[float, float]], /,
                                        weights: Optional[List[float]] = None, name: Optional[str] = None) \
            -> DataMetrics:
        """
        Get the distance metrics of ``coords`` to the closest data.

        Each ``weight`` corresponds to a ``coord``,
        so the length of ``coords`` must equal to the length of ``weights``.

        ``weights`` will be rounded during the calculation.

        If ``weights`` is ``None``, it will be 1 for all ``coords``.

        :raises ValueError: if the length of `coords` and `weights` are not the same
        """
        # Auto-fill weights if not specified
        if not weights:
            weights = [1] * len(list(coords))
        elif len(list(coords)) != len(list(weights)):
            raise ValueError(f"The length of `coords` ({len(list(coords))}) "
                             f"is not the same as `weights` ({len(list(weights))})")

        # Get the distances from the coords to the closest location/data
        distances = []

        for coord, weight in zip(coords, weights):
            distances.extend([self.find_closest_data(*coord).distance] * round(weight))

        # Calculate and metrics
        return DataMetrics(distances, name=name)

    def find_data_order_by_dist(self, lat: float, lon: float) -> Generator[ClosestDataResult, None, None]:
        """
        Find the data sorted by the distance from the data itself to ``(lat, lon)``.

        Immediately stops if the data is not loaded.
        """
        if not self._data:
            return

        # Set the initial search range to be 0.002 deg of latitude (~0.222 km / ~0.138 mi)
        search_range = 0.002

        # Find the candidate data
        candidates: List[T] = self.get_data_within_range(lat, lon, search_range)

        # Set for preventing returning duplicated data
        candidate_data_ids: Set[int] = {id(candidate) for candidate in candidates}

        # Expand the search range by the 1.5x each iteration
        while candidates:
            # Cast to :class:`ClosestDataResult` for later sorting
            candidates: List[ClosestDataResult] = [ClosestDataResult(data, lat, lon) for data in candidates]

            # Iterate through data
            for candidate in sorted(candidates, key=lambda data: data.distance):
                yield candidate

            # Expand search range
            search_range *= 1.5

            # Search for new candidate data
            candidates: List[T] = [data for data in self.get_data_within_range(lat, lon, search_range)
                                   if id(data) not in candidate_data_ids]
            candidate_data_ids.update({id(candidate) for candidate in candidates})

    def find_closest_data_num(self, lat: float, lon: float, count: int) -> List[ClosestDataResult]:
        """
        Find the ``count`` closest data to the location at ``(lat, lon)``.

        :raises ValueError: if no locational data is loaded
        """
        # Early terminate on no valid locational data loaded (not possible to find the closest data)
        if not self._data:
            raise ValueError("No locational data loaded")

        return [data for _, data in zip(range(count), self.find_data_order_by_dist(lat, lon))]

    def find_closest_data(self, lat: float, lon: float) -> ClosestDataResult:
        """
        Find the data closest to the location at ``(lat, lon)``.

        :raises ValueError: if no locational data is loaded
        """
        return self.find_closest_data_num(lat, lon, 1)[0]
