"""Functions for viewing the data of stop removal."""
from datetime import datetime
from typing import List, Tuple

import matplotlib.pyplot as plt
from folium import Map as FoliumMap, Icon, Marker, Popup

from msnmetrosim.models.results import CrossStopRemovalResult
from msnmetrosim.utils import generate_points
from .controllers import ctrl_stops_cross
from .mapgen import generate_92_wkd_routes

__all__ = ("generate_stop_removal_report", "generate_top_12_stops_map",
           "plot_top_12_positive_impact_results", "plot_top_12_negative_impact_results")

# region Static info


TOP_12_POSITIVE = [
    ("W Terrace", "5117"),
    ("N Thompson", "Jana"),
    ("W Terrace", "Eastpark"),
    ("N Thompson", "Westwynn"),
    ("S Whitney", "Gilbert"),
    ("Hathaway", "Greenwich"),
    ("Commercial", "North Lawn"),
    ("Oak", "E Washington"),
    ("S Gammon", "Gammon"),
    ("Fish Hatchery", "W Badger"),
    ("Caddis", "Cahill"),
    ("Anniversary", "Forest Run")
]

TOP_12_NEGATIVE = [
    ("Starr Grass", "S High Point"),
    ("Pinehurst", "S Greenview"),
    ("Mckee", "Seminole"),
    ("Mckee", "Commerce Park"),
    ("Cremer", "Park And Ride"),
    ("Mid Town", "Hawks Landing"),
    ("Moorland", "Manor"),
    ("E Verona", "Maple Grove"),
    ("Airport", "Terminal Door 6"),
    ("W Verona", "Westridge"),
    ("Woods", "Mid Town"),
    ("Northern Lights", "Epic Staff C"),
]


# endregion


# region Report generating


def generate_stop_removal_report(range_km: float, interval_km: float,
                                 report_path: str = "../reports/0921-report.txt"):
    """
    Generate a stop removal report with impact index included.

    This uses ``msnmetrosim.utils.generate_points()`` to generate dummy agents
    for simulating the accessibility difference,

    The report will be output to ``report_path``.
    """
    # Get a list of results of removing each stops
    results = ctrl_stops_cross.get_all_stop_remove_results(range_km, interval_km)

    # Generate the report to `reports/0921-report.txt`
    with open(report_path, "w") as f:
        f.write(f"Report on {datetime.now()} (CDT)\n")
        f.write("\n")
        f.write(f"Range: {range_km} km / Interval: {interval_km} km\n")

        # Get each removal results and sort them by impact index
        # Check the documentation of `impact_index` to get more information
        for rank, result in enumerate(sorted(results, key=lambda r: r.impact_index, reverse=True), start=1):
            f.write(f"#{rank} - Remove {result.stop_removed.cross_name}\n")
            f.write(f"Impact index: {result.impact_index:.4f}\n")


# endregion


# region Difference histogram plotting


def plot_stop_accessibility_diff(subplot, result: CrossStopRemovalResult):
    """Plot the accessibility difference in ``result`` as a subplot onto ``subplot``."""
    # ----- Plot histogram
    # https://datavizpyr.com/overlapping-histograms-with-matplotlib-in-python/

    # Configure plot
    subplot.set_xlabel("Distance to stop (km)", size=14)
    subplot.set_ylabel("Agent count", size=14)
    subplot.set_title(f"Distance to stop between before and after removing {result.stop_removed.cross_name}")

    # Plot histograms
    subplot.hist(result.metrics_before.data, bins=20, alpha=0.5, label="Before")
    subplot.hist(result.metrics_after.data, bins=20, alpha=0.5, label="After")

    # Post-configure the plot
    subplot.legend(loc="upper right")


def generate_accessibility_change_plots(plot_x: int, plot_y: int, results: List[CrossStopRemovalResult],
                                        fig_size: int = 6):
    """
    Generate a ``plot_x`` x ``plot_y`` figure containing the difference information in ``results`` and return that.

    ``plot_x`` x ``plot_y`` must equal to the data count in ``results``.

    The metrics of the before and the after in each entry of ``results`` will be plotted to a single subplot.

    .. note::
        https://matplotlib.org/3.1.0/gallery/subplots_axes_and_figures/subplots_demo.html
    """
    figure, axs = plt.subplots(plot_x, plot_y, figsize=(plot_x * fig_size, plot_y * fig_size))

    # pylint: disable=invalid-name

    for x in range(plot_x):
        for y in range(plot_y):
            plot_stop_accessibility_diff(axs[x, y], results[x * plot_y + y])

    return figure


def plot_accessibility_impact_results(stops_name: List[Tuple[str, str]], plot_x: int, plot_y: int,
                                      range_km: float, interval_km: float, title: str):
    """
    Plot the accessibility difference of before and after removing the stops onto a figure and return it.

    Each element of ``stops_name`` contains the first and second street (order doesn't matter) name.

    ``plot_x`` x ``plot_y`` must equal to the count of ``stops_cross``.

    :param stops_name: street pair of the stops to be removed
    :param plot_x: count of plots on x axis
    :param plot_y: count of plots on y axis
    :param range_km: range for the dummy agents to generate in km
    :param interval_km: dummy agents interval in km
    :param title: title of the main plot
    """
    # pylint: disable=too-many-arguments

    # Get the stops by its streets
    stops_at_cross = []

    for primary, secondary in stops_name:
        print(f"Getting the stop of {primary} & {secondary}")
        grouped_stop = ctrl_stops_cross.get_grouped_stop_by_street_names(primary, secondary)
        if not grouped_stop:
            raise ValueError(f"Grouped stop of {primary} & {secondary} not found")

        stops_at_cross.append(grouped_stop)

    # Get metrics between before and after removing the stop
    results: List[CrossStopRemovalResult] = []

    for stop in stops_at_cross:
        print(f"Getting the metrics of {stop.cross_name}")
        agents = generate_points(stop.coordinate, range_km, interval_km)

        result = ctrl_stops_cross.get_metrics_of_single_stop_removal(stop.primary, stop.secondary, agents)
        results.append(result)

    # Plot the data
    figure = generate_accessibility_change_plots(plot_x, plot_y, results)
    figure.suptitle(title, y=0.99, fontsize=20)  # Enlarging the text and slightly reposition the title

    return figure


def plot_top_12_positive_impact_results():
    """
    Plot and show the top 12 positive impact results.

    ``range_km`` is set to **0.6** and ``interval_km`` is set to **0.05**.
    """
    figure = plot_accessibility_impact_results(TOP_12_POSITIVE, 4, 3, 0.6, 0.05,
                                               "Top 12 stop removals that brings POSITIVE impacts")
    figure.show()


def plot_top_12_negative_impact_results():
    """
    Plot and show the top 12 negative impact results.

    ``range_km`` is set to **0.6** and ``interval_km`` is set to **0.05**.
    """
    figure = plot_accessibility_impact_results(TOP_12_NEGATIVE, 4, 3, 0.6, 0.05,
                                               "Top 12 stop removals that brings NEGATIVE impacts")
    figure.show()


# endregion


# region Stops map plotting


def generate_top_12_stops_map() -> FoliumMap:
    """Plot the locations of the top 12 positive/negative impactful stops on the map."""
    folium_map = generate_92_wkd_routes()

    # Getting the stop first so that if any of the stop does not exist, it fails faster
    stops = []
    for pos, neg in zip(TOP_12_POSITIVE, TOP_12_NEGATIVE):
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

# endregion
