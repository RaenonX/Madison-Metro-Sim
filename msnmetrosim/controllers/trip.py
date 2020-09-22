"""
Controller of the MMT GTFS trip data.

The complete MMT GTFS dataset can be downloaded here:
http://transitdata.cityofmadison.com/GTFS/mmt_gtfs.zip
"""
import csv
from typing import List, Dict

from msnmetrosim.models import MMTTrip
from msnmetrosim.utils import temporary_func

__all__ = ("MMTTripDataController", "ServiceIdNotFoundError")


class ServiceIdNotFoundError(KeyError):
    """Raised if the given service ID is not found in the loaded data."""

    def __init__(self, service_id: str):
        super().__init__(f"Data of service ID <{service_id}> not found")


class MMTTripDataController:
    """MMT trip data controller."""

    def _init_dict_by_serv_id(self, trip: MMTTrip):
        sid = trip.service_id

        if sid not in self._dict_by_serv_id:
            self._dict_by_serv_id[sid] = []

        self._dict_by_serv_id[sid].append(trip)

    def __init__(self, trips: List[MMTTrip]):
        self._core: List[MMTTrip] = trips
        self._dict_by_serv_id: Dict[str, List[MMTTrip]] = {}

        # Create a dict with service ID as key and trip data entry as value
        for trip in trips:
            self._init_dict_by_serv_id(trip)

    @temporary_func
    def get_shapes_available_in_service(self, service_id: str) -> Dict[int, MMTTrip]:
        """
        Get all shapes that will be ran at least once in a service plan.

        The key of the return is ``shape_id``;
        the value of the return is the last trip of the day ran in ``shape_id``.

        ------

        This is temporary and should be removed later because:

        - This includes routes / trips that will run for the last schedule of a day

        - Does not have the ability to reflect on the route redundancy

        :raises ServiceIdNotFoundError: `service_id` not found in the loaded data
        """
        if service_id not in self._dict_by_serv_id:
            raise ServiceIdNotFoundError(service_id)

        ret = {}

        for trip in self._dict_by_serv_id[service_id]:
            ret[trip.shape_id] = trip

        return ret

    def get_all_service_ids(self) -> Dict[str, int]:
        """
        Get all available service IDs and the corresponding count of trips.

        This function is slightly expensive because it iterate through all the trips for each call of this function.
        """
        ret = {}

        for trip in self._core:
            sid = trip.service_id
            if sid not in ret:
                ret[sid] = 0

            ret[sid] += 1

        return ret

    @staticmethod
    def load_from_file(file_path: str):
        """
        Load the trip data from trip data file.

        This file should be a csv with the following schema:

            (
                route_id,
                route_short_name,
                service_id,
                trip_id,
                trip_headsign,
                direction_id,
                direction_name,
                block_id,
                shape_id,
                shape_code,
                trip_type,
                trip_sort,
                wheelchair_accessible,
                bikes_allowed
            )

        This file could be found in the MMT GTFS dataset with the name ``trips.csv``.
        """
        trips = []

        with open(file_path, "r") as trips_file:
            csv_reader = csv.reader(trips_file, delimiter=",")
            next(csv_reader, None)  # Dump header

            for row in csv_reader:
                trips.append(MMTTrip.parse_from_row(row))

        return MMTTripDataController(trips)
