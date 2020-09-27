"""Model of the MMT GTFS stops grouped by its located cross."""
from dataclasses import dataclass, field
from typing import List

from .base import LocationalModelBase, HasCrossModelBase
from .stop import MMTStop

__all__ = ("MMTStopsAtCross",)


@dataclass
class MMTStopsAtCross(LocationalModelBase, HasCrossModelBase):
    """
    MMT GTFS stops grouped by the cross of the stops.

    .. note::
        Check the documentation of ``MMTStop`` for more information.
    """

    primary: str
    secondary: str
    wheelchair_accessible: bool

    stops: List[MMTStop]

    lat: float = field(init=False)
    lon: float = field(init=False)

    def __post_init__(self):
        total_lat = 0
        total_lon = 0
        total_count = len(self.stops)

        for stop in self.stops:
            total_lat += stop.lat
            total_lon += stop.lon

        self.lat = total_lat / total_count
        self.lon = total_lon / total_count

    @property
    def name_list_html(self) -> str:
        """Get the list of stops in HTML."""
        ret = ["<ul>"]

        for stop in self.stops:
            self.wheelchair_accessible = stop.wheelchair_accessible
            ret.append(f"<li>{stop.name}</li>")
            ret.append(f"<li>Wheelchair Accessible: {self.wheelchair_accessible}</li>")

        ret.append("</ul>")

        return "".join(ret)

    @property
    def wheelchair_accessibility(self) -> bool:
        """return if wheelchair boarding is available at a given stop"""
        return self.wheelchair_accessible
