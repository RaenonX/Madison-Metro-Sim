"""
Functions for generating various base maps.

Maps that contain additional information rather than bus routes and stops should be inside a different file.
"""
from typing import Tuple, List, Optional

from folium import Map as FoliumMap, Icon, Marker, Circle, PolyLine, Popup
from folium.plugins import MarkerCluster

from msnmetrosim.models import MMTStopsAtCross
from msnmetrosim.static import MAP_MADISON_CENTER_COORD, MAP_TILE, MAP_ZOOM_START, CONTROL_SCALE
from msnmetrosim.utils import temporary_func
from .controllers import ctrl_ridership_stop, ctrl_routes, ctrl_shapes, ctrl_stops, ctrl_stops_cross, ctrl_trips

__all__ = ("generate_clean_map", "generate_map_with_points", "generate_map_given_stops_with_color",
           "generate_92_wkd_routes", "generate_92_wkd_routes_and_stops", "generate_92_wkd_routes_and_grouped_stops",)


def plot_stops_by_cross(folium_map: FoliumMap, /, clustered: bool = True, use_marker: bool = True):
    """
    Plot all the stops grouped by its located cross onto ``folium_map``.

    ``clustered`` determines if the stop will be clustered/expanded upon zooming.

    ``use_marker`` determines if the stop will be rendered using :class:`Marker`.
    If ``false``, use :class:`Circle` instead.

    Could use customized color in the future for better rendering effect.
    """
    if clustered:
        parent = MarkerCluster().add_to(folium_map)
    else:
        parent = folium_map

    for stop in ctrl_stops_cross.all_data:
        popup = Popup(f"{stop.primary} & {stop.secondary}<br>{stop.name_list_html}",
                      min_width=250, max_width=800)

        if stop.wheelchair_accessible:
            color = "green"
        else:
            color = "lightred"

        if use_marker:
            icon = Icon(color=color, icon_color="white", icon="bus", angle=0, prefix="fa")

            Marker(stop.coordinate, popup=popup, icon=icon).add_to(parent)
        else:
            Circle(stop.coordinate, 2, popup=popup, color=color).add_to(parent)


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

    for stop in ctrl_stops.all_data:
        ridership = ctrl_ridership_stop.get_stop_data_by_id(stop.stop_id)

        popup = Popup(f"{stop.name}<br>Weekday ridership: {ridership.weekday if ridership else '(unavailable)'}"
                      f"<br>Wheelchair Accessible: {stop.wheelchair_accessible}",
                      min_width=250, max_width=800)

        if stop.wheelchair_accessible:
            icon_c = "green"
        else:
            icon_c = "lightred"

        Marker(
            stop.coordinate,
            popup=popup,
            icon=Icon(color=icon_c, icon_color="white", icon="bus", angle=0,
                      prefix="fa")
        ).add_to(parent)


def plot_stops_given_with_color(folium_map: FoliumMap, stops: List[Tuple[MMTStopsAtCross, Optional[str]]]):
    """
    Plot ``stops`` as markers onto ``folium_map``.

    The :class:`str` in the sub-element is the color to be used on the stop marker.
    If this is ``None``, then "blue" will be used.
    """
    for stop, color in stops:
        popup = Popup(stop.cross_name, min_width=250, max_width=800)

        Marker(
            stop.coordinate,
            popup=popup,
            icon=Icon(color=color or "blue", icon_color="white", icon="bus", angle=0, prefix="fa")
        ).add_to(folium_map)


def plot_shape(folium_map: FoliumMap, shape_id: int, shape_popup: str, shape_color: str):
    """
    Plot the shape of ``shape_id`` onto ``folium_map``.

    ``shape_color`` can be any strings that represents color in CSS.
    """
    shape_coords = ctrl_shapes.get_shape_coords_by_id(shape_id)
    PolyLine(shape_coords, color=shape_color, popup=shape_popup).add_to(folium_map)


def plot_point(folium_map: FoliumMap, coord: Tuple[float, float]):
    """Plot points at ``coord`` on ``folium_map``."""
    Circle(coord, 2).add_to(folium_map)


@temporary_func
def plot_92_wkd_routes(folium_map: FoliumMap):
    """Plot all the routes (shapes) available under service ID ``92_WKD`` (Batch #92, weekday plan, presumably)."""
    serv_shapes = ctrl_trips.get_shapes_available_in_service("92_WKD")

    for shape_id, last_trip in serv_shapes.items():
        shape_popup = f"{last_trip.route_short_name}<br><b>{last_trip.trip_headsign}</b>"
        shape_color = ctrl_routes.get_route_by_route_id(last_trip.route_id).route_color

        plot_shape(folium_map, shape_id, shape_popup, shape_color)


def generate_map_given_stops_with_color(stops: List[Tuple[MMTStopsAtCross, Optional[str]]]):
    """
    Generate a map with ``stops`` plotted on it.

    The :class:`str` in the sub-element is the color to be used on the stop marker.
    If this is ``None``, then "blue" will be used.
    """
    folium_map = generate_92_wkd_routes()

    plot_stops_given_with_color(folium_map, stops)
    plot_stops_by_cross(folium_map, use_marker=False)

    return folium_map


def generate_map_with_points(coords: List[Tuple[float, float]],
                             center_coord: Tuple[float, float] = None,
                             tile: str = None,
                             zoom_start: int = None,
                             control_scale: str = None) -> FoliumMap:
    """Generate a clean map with ``coords`` as points on it."""
    folium_map = generate_clean_map(center_coord, tile, zoom_start, control_scale)

    for coord in coords:
        plot_point(folium_map, coord)

    return folium_map


def generate_clean_map(center_coord: Tuple[float, float] = None,
                       tile: str = None,
                       zoom_start: int = None,
                       control_scale: str = None) -> FoliumMap:
    """
    Generate a clean map.

    Default configuration will be applied for each value if not specified.
    """
    return FoliumMap(location=center_coord if center_coord else MAP_MADISON_CENTER_COORD,
                     tiles=tile if tile else MAP_TILE,
                     zoom_start=zoom_start if zoom_start else MAP_ZOOM_START,
                     control_scale=control_scale if control_scale else CONTROL_SCALE)


@temporary_func
def generate_92_wkd_routes() -> FoliumMap:
    """Generate a map with 92_WKD routes plotted on the map."""
    folium_map = generate_clean_map()

    plot_92_wkd_routes(folium_map)

    return folium_map


@temporary_func
def generate_92_wkd_routes_and_stops() -> FoliumMap:
    """Generate a map with 92_WKD routes and all stops plotted on the map."""
    folium_map = generate_92_wkd_routes()

    plot_stops(folium_map)

    return folium_map


@temporary_func
def generate_92_wkd_routes_and_grouped_stops() -> FoliumMap:
    """Generate a map with 92_WKD routes and all stops grouped by cross plotted on the map."""
    folium_map = generate_92_wkd_routes()

    plot_stops_by_cross(folium_map)

    return folium_map
