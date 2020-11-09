"""Functions for creating the map for stops involved in the stop removal reports."""
from typing import List, Tuple

from folium import Map as FoliumMap

from msnmetrosim.models import MMTStopsAtCross
from msnmetrosim.views.mapgen import generate_map_given_stops_with_color
from .plot_base import get_stops_at_cross
from .static import (
    TOP_12_POSITIVE_DUMMY, TOP_12_NEGATIVE_DUMMY,
    TOP_12_POSITIVE_POP_DENSITY, TOP_12_NEGATIVE_POP_DENSITY
)

__all__ = ("generate_top_12_removal_map_dummy", "generate_top_12_removal_map_pop_density",
           "generate_top_12_removal_map_mixed")


def generate_top_12_removal_map_dummy() -> FoliumMap:
    """Generate a map with top 12 positive/negative impactful stop removals using dummy agents plotted on it."""
    stops: List[Tuple[MMTStopsAtCross, str]] = []
    stops.extend([(stop, "green") for stop in get_stops_at_cross(TOP_12_POSITIVE_DUMMY)])
    stops.extend([(stop, "red") for stop in get_stops_at_cross(TOP_12_NEGATIVE_DUMMY)])

    return generate_map_given_stops_with_color(stops)


def generate_top_12_removal_map_pop_density() -> FoliumMap:
    """Generate a map with top 12 positive/negative impactful stop removals using population density plotted on it."""
    stops: List[Tuple[MMTStopsAtCross, str]] = []
    stops.extend([(stop, "blue") for stop in get_stops_at_cross(TOP_12_POSITIVE_POP_DENSITY)])
    stops.extend([(stop, "red") for stop in get_stops_at_cross(TOP_12_NEGATIVE_POP_DENSITY)])

    return generate_map_given_stops_with_color(stops)


def generate_top_12_removal_map_mixed() -> FoliumMap:
    """
    Generate a map with both top 12 pos/neg stop removals using pop density/dummy agents plotted on it.

    Points using population density will be rendered in green/red;
    dummy agents will be rendered in lightgreen/lightred.
    """
    stops: List[Tuple[MMTStopsAtCross, str]] = []
    stops.extend([(stop, "blue") for stop in get_stops_at_cross(TOP_12_POSITIVE_POP_DENSITY)])
    stops.extend([(stop, "red") for stop in get_stops_at_cross(TOP_12_NEGATIVE_POP_DENSITY)])
    stops.extend([(stop, "lightblue") for stop in get_stops_at_cross(TOP_12_POSITIVE_DUMMY)])
    stops.extend([(stop, "lightred") for stop in get_stops_at_cross(TOP_12_NEGATIVE_DUMMY)])

    return generate_map_given_stops_with_color(stops)
