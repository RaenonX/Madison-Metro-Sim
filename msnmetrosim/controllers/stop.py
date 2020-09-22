"""
Controller of the MMT GTFS stop data.

The complete MMT GTFS dataset can be downloaded here:
http://transitdata.cityofmadison.com/GTFS/mmt_gtfs.zip
"""
import csv
from typing import List, Dict, Generator

from msnmetrosim.models import MMTStop

__all__ = ("MMTStopDataController",)


class MMTStopDataController:
    """MMT stop data controller."""

    def _init_dict_by_id(self, stop: MMTStop):
        # Assuming ``stop_id`` is unique
        self._dict_by_id[stop.stop_id] = stop

    def __init__(self, stops: List[MMTStop]):
        self._dict_by_id: Dict[int, MMTStop] = {}

        # Create a dict with ID as key and stop data entry as value
        for stop in stops:
            self._init_dict_by_id(stop)

    def get_all_stops(self) -> Generator[MMTStop, None, None]:
        """Get all the stops in the loaded data."""
        for stop in self._dict_by_id.values():
            yield stop

    @staticmethod
    def load_from_file(file_path: str):
        """
        Load the stop data from stop data file.

        This file should be a csv with the following schema:

            (
                stop_id,
                stop_code,
                stop_name,
                stop_desc,
                stop_lat,
                stop_lon,
                agency_id,
                jurisdiction_id,
                location_type,
                parent_station,
                relative_position,
                cardinal_direction,
                wheelchair_boarding,
                primary_street,
                address_range,
                cross_location
            )

        This file could be found in the MMT GTFS dataset with the name ``stops.csv``.
        """
        stops = []

        with open(file_path, "r") as stops_file:
            csv_reader = csv.reader(stops_file, delimiter=",")
            next(csv_reader, None)  # Dump header

            for row in csv_reader:
                stops.append(MMTStop.parse_from_row(row))

        return MMTStopDataController(stops)
