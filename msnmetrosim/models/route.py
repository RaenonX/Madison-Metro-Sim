"""
Single entry of route data (routes.csv) in MMT GTFS dataset.

The complete MMT GTFS dataset can be downloaded here:
http://transitdata.cityofmadison.com/GTFS/mmt_gtfs.zip
"""
from dataclasses import dataclass
from typing import List

__all__ = ("MMTRoute",)


@dataclass
class MMTRoute:
    """
    MMT GTFS route entry.

    .. note::
        ``route_short_name`` is the router number in daily use.

        ``service_id`` is the service plan ID.

        - This only contains the batch number (for example, ``92`` or ``93``).

        - ``service_id`` of :class:`MMTTrip` is slightly different from this.
          The ``service_id`` there includes codes, which corresponds to the operational dates and plans recorded in
          ``calendar.csv`` and ``calendar_dates.csv``.

        Original ``route_color`` and ``route_text_color`` are HEX colors without "#".
        After parsing, these will be prefixed with "#".
    """

    route_id: int

    service_id: int

    route_short_name: str

    route_color: str
    route_text_color: str

    @staticmethod
    def parse_from_row(row: List[str]):
        """Parse a single entry into :class:`MMTRoute` from a csv row."""
        route_id = int(row[0])

        service_id = int(row[1])

        route_short_name = row[3]

        route_color = f"#{row[9]}"
        route_text_color = f"#{row[10]}"

        return MMTRoute(route_id, service_id, route_short_name, route_color, route_text_color)
