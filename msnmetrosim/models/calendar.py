"""
Single entry of service calendar data (calendar.csv) in MMT GTFS dataset.

The complete MMT GTFS dataset can be downloaded here:
http://transitdata.cityofmadison.com/GTFS/mmt_gtfs.zip
"""
from dataclasses import dataclass
from datetime import datetime, date, timedelta
from typing import List

__all__ = ("MMTCalendar",)


@dataclass
class MMTCalendar:
    """
    MMT GTFS service calendar entry.

    .. note::
        `service_id` service ID contains special characters like "#" and "=".
    """

    # pylint: disable=too-many-instance-attributes

    service_id: str
    service_name: str

    running_dates: List[date]

    start_date: date
    end_date: date

    @staticmethod
    def _parse_running_dates(row: List[str], start_date: date, end_date: date) -> List[date]:
        ret: List[date] = []
        weekdays = [bool(int(wd)) for wd in row[2:9]]

        current_date = start_date
        while current_date <= end_date:
            if weekdays[current_date.weekday()]:
                ret.append(current_date)

            current_date += timedelta(days=1)

        return ret

    @classmethod
    def parse_from_row(cls, row: List[str]):
        """Parse a single entry into :class:`MMTCalendar` from a row of ``mmt_gtfs/calendar.csv``."""
        # pylint: disable=too-many-instance-attributes
        service_id = row[0]
        service_name = row[1]

        start_date = datetime.strptime(row[9], "%Y%m%d").date()
        end_date = datetime.strptime(row[10], "%Y%m%d").date()

        running_dates = cls._parse_running_dates(row, start_date, end_date)

        return MMTCalendar(service_id, service_name, running_dates, start_date, end_date)
