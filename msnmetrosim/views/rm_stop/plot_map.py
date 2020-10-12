"""Functions for creating the map for stops involved in the stop removal reports."""
from typing import List, Tuple

from folium import Map as FoliumMap, Icon, Marker, Popup

from msnmetrosim.models import MMTStopsAtCross
from msnmetrosim.views.mapgen import generate_92_wkd_routes
from .plot_base import get_stops_at_cross
from .static import (
    TOP_12_POSITIVE_DUMMY, TOP_12_NEGATIVE_DUMMY,
    TOP_12_POSITIVE_POP_DENSITY, TOP_12_NEGATIVE_POP_DENSITY
)

__all__ = ("generate_top_12_stops_map_dummy", "generate_top_12_stops_map_pop_density")


def generate_top_stops_map(pos: List[Tuple[str, str]], neg: List[Tuple[str, str]]):
    """Plot the locations of the top positive/negative impactful stops on the map."""
    folium_map = generate_92_wkd_routes()

    stops: List[Tuple[MMTStopsAtCross, bool]] = []
    stops.extend([(stop, True) for stop in get_stops_at_cross(pos)])
    stops.extend([(stop, False) for stop in get_stops_at_cross(neg)])

    # Plot stops onto map
    for stop, is_positive in stops:
        popup = Popup(stop.cross_name, min_width=250, max_width=800)

        Marker(
            stop.coordinate,
            popup=popup,
            icon=Icon(color="green" if is_positive else "red", icon_color="white", icon="bus", angle=0,
                      prefix="fa")
        ).add_to(folium_map)

    return folium_map


def generate_top_12_stops_map_dummy() -> FoliumMap:
    """Plot the locations of the top 12 positive/negative impactful stops using dummy agents on the map."""
    return generate_top_stops_map(TOP_12_POSITIVE_DUMMY, TOP_12_NEGATIVE_DUMMY)


def generate_top_12_stops_map_pop_density() -> FoliumMap:
    """Plot the locations of the top 12 positive/negative impactful stops using population density on the map."""
    return generate_top_stops_map(TOP_12_POSITIVE_POP_DENSITY, TOP_12_NEGATIVE_POP_DENSITY)
