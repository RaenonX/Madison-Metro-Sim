"""
Controller of the MMT GTFS trip data.

The complete MMT GTFS dataset can be downloaded here:
http://transitdata.cityofmadison.com/GTFS/mmt_gtfs.zip
"""
from typing import List, Dict, Set, Union

from msnmetrosim.controllers.base import CSVLoadableController
from msnmetrosim.models import MMTTrip
from msnmetrosim.utils import temporary_func

__all__ = ("MMTTripDataController", "ServiceIdNotFoundError")


class ServiceIdNotFoundError(KeyError):
    """Raised if the given service ID is not found in the loaded data."""

    def __init__(self, service_id: str):
        super().__init__(f"Data of service ID <{service_id}> not found")


class MMTTripDataController(CSVLoadableController):
    """
    MMT trip data controller.

    Data file that will use this controller:
    - mmt_gtfs/trips.csv
    """

    def _init_dict_by_serv_id(self, trip: MMTTrip):
        sid = trip.service_id

        if sid not in self._dict_by_serv_id:
            self._dict_by_serv_id[sid] = []

        self._dict_by_serv_id[sid].append(trip)

    def __init__(self, trips: List[MMTTrip]):
        super().__init__(trips)

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

    def get_trip_ids(self, service_ids: Union[List[str], str]) -> Set[int]:
        """Get all the trip IDs of service plans ``service_ids``."""
        if isinstance(service_ids, str):
            service_ids = [service_ids]

        return {trip.trip_id for service_id in service_ids for trip in self._dict_by_serv_id[service_id]}

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
    def on_row_read(row: List[str]) -> object:
        return MMTTrip.parse_from_row(row)
