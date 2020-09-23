"""
Controller of the MMT GTFS route data.

The complete MMT GTFS dataset can be downloaded here:
http://transitdata.cityofmadison.com/GTFS/mmt_gtfs.zip
"""
from typing import List, Dict

from msnmetrosim.controllers.base import CSVLoadableController
from msnmetrosim.models import MMTRoute

__all__ = ("MMTRouteDataController", "RouteIdNotFoundError")


class RouteIdNotFoundError(KeyError):
    """Raised if the given route ID is not found in the loaded data."""

    def __init__(self, route_id: int):
        super().__init__(f"Data of route ID <{route_id}> not found")


class MMTRouteDataController(CSVLoadableController):
    """MMT route data controller."""

    def _init_dict_by_rid(self, route: MMTRoute):
        # This assumes that `route_id` in the original data is unique
        self._dict_by_rid[route.route_id] = route

    def __init__(self, routes: List[MMTRoute]):
        super().__init__(routes)

        self._dict_by_rid: Dict[int, MMTRoute] = {}

        # Create a dict with route ID as key and route data entry as value
        for route in routes:
            self._init_dict_by_rid(route)

    def get_route_by_route_id(self, route_id: int) -> MMTRoute:
        """
        Get a :class:`MMTRoute` by ``route_id``.

        :raise ServiceIdNotFoundError: if `route_id` is not in the loaded data
        """
        if route_id not in self._dict_by_rid:
            raise RouteIdNotFoundError(route_id)

        return self._dict_by_rid[route_id]

    @staticmethod
    def on_row_read(row: List[str]) -> object:
        return MMTRoute.parse_from_row(row)
