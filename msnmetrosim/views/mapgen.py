"""Functions to generate folium map object."""
from typing import Tuple

from folium import Map as FoliumMap, Icon, Marker, PolyLine, Popup
from folium.plugins import MarkerCluster

from msnmetrosim.controllers import (
    # MMT GTFS data controllers
    MMTRouteDataController, MMTShapeDataController, MMTStopDataController, MMTStopsAtCrossDataController,
    MMTTripDataController,
    # Ridership data controllers
    RidershipByStopController
)
from msnmetrosim.static import MAP_CENTER_COORD, MAP_TILE, MAP_ZOOM_START
from msnmetrosim.utils import temporary_func

__all__ = ("generate_clean_map", "generate_92_wkd_routes_and_stops", "generate_92_wkd_routes_and_grouped_stops")

# Preloading the data - be aware that these should be removed if controllers will perform manipulations

_routes = MMTRouteDataController.load_csv("mmt_gtfs/routes.csv")
_shapes = MMTShapeDataController.load_csv("mmt_gtfs/shapes.csv")
_stops = MMTStopDataController.load_csv("mmt_gtfs/stops.csv")
_stops_cross = MMTStopsAtCrossDataController(_stops)
_trips = MMTTripDataController.load_csv("mmt_gtfs/trips.csv")
_ridership_stop = RidershipByStopController.load_csv("ridership/by_stop.csv")


def plot_stops_by_cross(folium_map: FoliumMap, clustered: bool = True):
    """
    Plot all the stops grouped by its located cross onto ``folium_map``.

    ``clustered`` determines if the stop will be clustered/expanded upon zoom.

    Could use customized color in the future for better rendering effect.
    """
    if clustered:
        parent = MarkerCluster().add_to(folium_map)
    else:
        parent = folium_map

    for stop in _stops_cross.grouped_stops:
        popup = Popup(f"{stop.primary} & {stop.secondary}<br>{stop.name_list_html}",
                      min_width=250, max_width=800)

        Marker(
            stop.coordinate,
            popup=popup,
            icon=Icon(color="green", icon_color="white", icon="bus", angle=0,
                      prefix="fa")
        ).add_to(parent)


def plot_stops(folium_map: FoliumMap, clustered: bool = True):
    """
    Plot all the stops onto ``folium_map``.

    ``clustered`` determines if the stop will be clustered/expanded upon zoom.

    Could use customized color in the future for better rendering effect.
    """
    if clustered:
        parent = MarkerCluster().add_to(folium_map)
    else:
        parent = folium_map

    for stop in _stops.get_all_stops():
        ridership = _ridership_stop.get_stop_data_by_id(stop.stop_id)

        popup = Popup(f"{stop.name}<br>Weekday ridership: {ridership.weekday if ridership else '(unavailable)'}",
                      min_width=250, max_width=800)

        Marker(
            stop.coordinate,
            popup=popup,
            icon=Icon(color="green", icon_color="white", icon="bus", angle=0,
                      prefix="fa")
        ).add_to(parent)


def plot_shape(folium_map: FoliumMap, shape_id: int, shape_popup: str, shape_color: str):
    """
    Plot the shape of ``shape_id`` onto ``folium_map``.

    ``shape_color`` can be any strings that represents color in CSS.
    """
    shape_coords = _shapes.get_shape_coords_by_id(shape_id)
    PolyLine(shape_coords, color=shape_color, popup=shape_popup).add_to(folium_map)


@temporary_func
def plot_92_wkd_routes(folium_map: FoliumMap):
    """Plot all the routes (shapes) available under service ID ``92_WKD`` (Batch #92, weekday plan, presumably)."""
    shapes = _trips.get_shapes_available_in_service("92_WKD")

    for shape_id, last_trip in shapes.items():
        shape_popup = f"{last_trip.route_short_name}<br><b>{last_trip.trip_headsign}</b>"
        shape_color = _routes.get_route_by_route_id(last_trip.route_id).route_color

        plot_shape(folium_map, shape_id, shape_popup, shape_color)


def generate_clean_map(center_coord: Tuple[float, float] = None,
                       tile: str = None,
                       zoom_start: int = None) -> FoliumMap:
    """
    Generate a clean map.

    Default configuration will be applied for each value if not specified.
    """
    return FoliumMap(location=center_coord if center_coord else MAP_CENTER_COORD,
                     tiles=tile if tile else MAP_TILE,
                     zoom_start=zoom_start if zoom_start else MAP_ZOOM_START)


@temporary_func
def generate_92_wkd_routes_and_stops() -> FoliumMap:
    """Generate a map with 92_WKD routes and all stops plotted on the map."""
    folium_map = generate_clean_map()

    plot_stops(folium_map)
    plot_92_wkd_routes(folium_map)

    return folium_map


@temporary_func
def generate_92_wkd_routes_and_grouped_stops() -> FoliumMap:
    """Generate a map with 92_WKD routes and all stops grouped by cross plotted on the map."""
    folium_map = generate_clean_map()

    plot_stops_by_cross(folium_map)
    plot_92_wkd_routes(folium_map)

    return folium_map
