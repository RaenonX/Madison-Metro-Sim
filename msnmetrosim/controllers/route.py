"""
Controller of the MMT GTFS route data.

The complete MMT GTFS dataset can be downloaded here:
http://transitdata.cityofmadison.com/GTFS/mmt_gtfs.zip
"""
import csv
from typing import List, Dict

from msnmetrosim.models import MMTRoute

__all__ = ("MMTRouteDataController", "RouteIdNotFoundError")


class RouteIdNotFoundError(KeyError):
    """Raised if the given route ID is not found in the loaded data."""

    def __init__(self, route_id: int):
        super().__init__(f"Data of route ID <{route_id}> not found")


class MMTRouteDataController:
    """MMT route data controller."""

    def _init_dict_by_rid(self, route: MMTRoute):
        # This assumes that `route_id` in the original data is unique
        self._dict_by_rid[route.route_id] = route

    def __init__(self, routes: List[MMTRoute]):
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
    def load_from_file(file_path: str):
        """
        Load the route data from route data file.

        This file should be a csv with the following schema:

            (
                route_id,
                service_id,
                agency_id,
                route_short_name,
                route_long_name,
                route_service_name,
                route_desc,
                route_type,
                route_url,
                route_color,
                route_text_color,
                bikes_allowed
            )

        This file could be found in the MMT GTFS dataset with the name ``routes.csv``.
        """
        routes = []

        with open(file_path, "r") as routes_file:
            csv_reader = csv.reader(routes_file, delimiter=",")
            next(csv_reader, None)  # Dump header

            for row in csv_reader:
                routes.append(MMTRoute.parse_from_row(row))

        return MMTRouteDataController(routes)
