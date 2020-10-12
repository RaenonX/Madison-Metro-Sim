"""Functions for plotting the histograms of stop removal results."""
from typing import List, Tuple

from matplotlib.pyplot import Subplot

from msnmetrosim.models.results import CrossStopRemovalResult
from msnmetrosim.utils import generate_points
from msnmetrosim.views.controllers import ctrl_stops_cross
from .plot_base import get_stops_at_cross, generate_accessibility_plot_canvas
from .static import TOP_12_POSITIVE_DUMMY, TOP_12_NEGATIVE_DUMMY


def plot_stop_accessibility_hist(subplot: Subplot, result: CrossStopRemovalResult):
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

    # Get metrics between before and after removing the stop
    results: List[CrossStopRemovalResult] = []

    for stop in get_stops_at_cross(stops_name):
        print(f"Getting the metrics of {stop.cross_name}")
        agents = generate_points(stop.coordinate, range_km, interval_km)

        result = ctrl_stops_cross.get_metrics_of_single_stop_removal(stop.primary, stop.secondary, agents)
        results.append(result)

    # Plot the data
    figure = generate_accessibility_plot_canvas(plot_x, plot_y, plot_stop_accessibility_hist, results)
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
