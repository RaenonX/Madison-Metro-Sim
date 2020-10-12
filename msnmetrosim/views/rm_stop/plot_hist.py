"""Functions for plotting the histograms of stop removal results."""
from typing import List, Tuple

import matplotlib.pyplot as plt

from msnmetrosim.models.results import CrossStopRemovalResult
from msnmetrosim.utils import generate_points
from msnmetrosim.views.controllers import ctrl_stops_cross
from .static import TOP_12_POSITIVE_DUMMY, TOP_12_NEGATIVE_DUMMY


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


def plot_accessibility_impact_histograms(stops_name: List[Tuple[str, str]], plot_x: int, plot_y: int,
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


def plot_dummy_top_12_positive_impact_histogram():
    """
    Plot and show the top 12 positive impact histograms with dummy agents.

    ``range_km`` is set to **0.6** and ``interval_km`` is set to **0.05**.
    """
    figure = plot_accessibility_impact_histograms(TOP_12_POSITIVE_DUMMY, 4, 3, 0.6, 0.05,
                                                  "Top 12 stop removals that brings POSITIVE impacts")
    figure.show()


def plot_dummy_top_12_negative_impact_histogram():
    """
    Plot and show the top 12 negative impact histograms with dummy agents.

    ``range_km`` is set to **0.6** and ``interval_km`` is set to **0.05**.
    """
    figure = plot_accessibility_impact_histograms(TOP_12_NEGATIVE_DUMMY, 4, 3, 0.6, 0.05,
                                                  "Top 12 stop removals that brings NEGATIVE impacts")
    figure.show()
