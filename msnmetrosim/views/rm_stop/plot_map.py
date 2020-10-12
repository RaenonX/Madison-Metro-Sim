"""Functions for creating the map for stops involved in the stop removal reports."""
from folium import Map as FoliumMap, Icon, Marker, Popup

from msnmetrosim.views.controllers import ctrl_stops_cross
from msnmetrosim.views.mapgen import generate_92_wkd_routes
from .static import TOP_12_POSITIVE_DUMMY, TOP_12_NEGATIVE_DUMMY


def generate_top_12_stops_map_dummy() -> FoliumMap:
    """Plot the locations of the top 12 positive/negative impactful stops using dummy agents on the map."""
    folium_map = generate_92_wkd_routes()

    # Getting the stop first so that if any of the stop does not exist, it fails faster
    stops = []
    for pos, neg in zip(TOP_12_POSITIVE_DUMMY, TOP_12_NEGATIVE_DUMMY):
        primary, secondary = pos

        stop = ctrl_stops_cross.get_grouped_stop_by_street_names(primary, secondary)
        if not stop:
            raise ValueError(f"Grouped stop of {primary} & {secondary} not found")
        stops.append((stop, True))

        primary, secondary = neg

        stop = ctrl_stops_cross.get_grouped_stop_by_street_names(primary, secondary)
        if not stop:
            raise ValueError(f"Grouped stop of {primary} & {secondary} not found")
        stops.append((stop, False))

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
