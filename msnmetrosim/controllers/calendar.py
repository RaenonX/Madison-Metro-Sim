"""
Controller of the MMT GTFS service calendar data.

The complete MMT GTFS dataset can be downloaded here:
http://transitdata.cityofmadison.com/GTFS/mmt_gtfs.zip
"""
from datetime import datetime, date
from typing import List, Dict, Union

from msnmetrosim.models import MMTCalendar
from .base import CSVLoadableController

__all__ = ("MMTCalendarController",)


class MMTCalendarController(CSVLoadableController):
    """
    MMT service calendar data controller.

    Data file that will use this controller:
    - mmt_gtfs/calendar.csv
    """

    def _init_by_serv_id(self, calendars: List[MMTCalendar]):
        for calendar in calendars:
            self._by_serv_id[calendar.service_id] = calendar

    def _init_by_date(self, calendars: List[MMTCalendar]):
        for calendar in calendars:
            for running_date in calendar.running_dates:
                if running_date not in self._by_date:
                    self._by_date[running_date] = [calendar]
                else:
                    self._by_date[running_date].append(calendar)

    def __init__(self, calendars: List[MMTCalendar]):
        super().__init__(calendars)

        self._by_serv_id: Dict[str, MMTCalendar] = {}
        self._init_by_serv_id(calendars)

        self._by_date: Dict[date, List[MMTCalendar]] = {}
        self._init_by_date(calendars)

    def get_services_by_date(self, date_: Union[date, datetime]) -> List[MMTCalendar]:
        """
        Get the services that are running at ``date_``.

        Returns an empty list if no service data is found or running at that date.
        """
        if isinstance(date_, datetime):
            date_ = date_.date()

        return self._by_date.get(date_, [])

    @staticmethod
    def on_row_read(row: List[str]) -> object:
        return MMTCalendar.parse_from_row(row)
