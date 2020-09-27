"""Functions for plotting the data."""
from typing import List, Tuple

import matplotlib.pyplot as plt

from msnmetrosim.controllers import MMTStopDataController, MMTStopsAtCrossDataController
from msnmetrosim.models.results import CrossStopRemovalResult
from msnmetrosim.utils import generate_points

__all__ = ("plot_stop_accessibility_diff",)

_stops = MMTStopDataController.load_csv("mmt_gtfs/stops.csv")
_stops_cross = MMTStopsAtCrossDataController.from_stop_controller(_stops)


def plot_stop_accessibility_diff(subplot, result: CrossStopRemovalResult):
    """Plot the accessibility difference in ``result`` as a subplot onto ``subplot``."""
    # ----- Plot histogram
    # https://datavizpyr.com/overlapping-histograms-with-matplotlib-in-python/

    # Configure plot
    subplot.set_xlabel("Distance to stop (km)", size=14)
    subplot.set_ylabel("Agent count", size=14)
    subplot.set_title(f"Distance to stop change between before and after removing {result.stop_removed.cross_name}")

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


def plot_accessibility_impact_results(stops_cross: List[Tuple[str, str]], plot_x: int, plot_y: int,
                                      range_km: float, interval_km: float, title: str):
    """
    Plot the accessibility difference of before and after removing the stops onto a figure and return it.

    Each element of ``stops_cross`` contains the first and second street (order doesn't matter) name.

    ``plot_x`` x ``plot_y`` must equal to the count of ``stops_cross``.

    :param stops_cross: street pair of the stops to be removed
    :param plot_x: count of plots on x axis
    :param plot_y: count of plots on y axis
    :param range_km: range for the dummy agents to generate in km
    :param interval_km: dummy agents interval in km
    :param title: title of the main plot
    """
    # pylint: disable=too-many-arguments

    # Get the stops by its streets
    stops = []

    for primary, secondary in stops_cross:
        print(f"Getting the stop of {primary} & {secondary}")
        grouped_stop = _stops_cross.get_grouped_stop_by_street_names(primary, secondary)
        if not grouped_stop:
            raise ValueError(f"Grouped stop of {primary} & {secondary} not found")

        stops.append(grouped_stop)

    # Get metrics between before and after removing the stop
    results: List[CrossStopRemovalResult] = []

    for stop in stops:
        print(f"Getting the metrics of {stop.cross_name}")
        agents = generate_points(stop.coordinate, range_km, interval_km)

        result = _stops_cross.get_metrics_of_single_stop_removal(stop.primary, stop.secondary, agents)
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
    stops_cross = [
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

    figure = plot_accessibility_impact_results(stops_cross, 4, 3, 0.6, 0.05,
                                               "Top 12 stop removals that brings POSITIVE impacts")
    figure.show()


def plot_top_12_negative_impact_results():
    """
    Plot and show the top 12 negative impact results.

    ``range_km`` is set to **0.6** and ``interval_km`` is set to **0.05**.
    """
    stops_cross = [
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

    figure = plot_accessibility_impact_results(stops_cross, 4, 3, 0.6, 0.05,
                                               "Top 12 stop removals that brings NEGATIVE impacts")
    figure.show()


if __name__ == '__main__':
    plot_top_12_positive_impact_results()
    plot_top_12_negative_impact_results()
