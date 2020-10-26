"""Functions for plotting the CDFs of stop removal results."""
from typing import List, Tuple

from matplotlib.pyplot import Subplot

from msnmetrosim.models.results import CrossStopRemovalResult
from msnmetrosim.views.controllers import ctrl_stops_cross, ctrl_population
from .plot_base import get_stops_at_cross, generate_accessibility_plot_canvas
from .static import TOP_12_POSITIVE_POP_DENSITY, TOP_12_NEGATIVE_POP_DENSITY

__all__ = ("plot_pop_density_top_12_positive_impact_cdf", "plot_pop_density_top_12_negative_impact_cdf")


def plot_stop_accessibility_cdf(subplot: Subplot, result: CrossStopRemovalResult):
    """Plot the accessibility difference in ``result`` as a subplot onto ``subplot``."""
    # pylint: disable=invalid-name

    # Configure plot
    subplot.set_xlabel("Distance to stop (km)", size=20)
    subplot.set_ylabel("Percentile", size=20)
    subplot.set_title(result.stop_removed.cross_name, size=24)

    # Plot CDF
    x, y = result.metrics_before.get_quantile_cdf(20)
    subplot.plot(x, y, label="Before")

    x, y = result.metrics_after.get_quantile_cdf(20)
    subplot.plot(x, y, label="After")

    # Post-configure the plot
    subplot.legend(loc="upper right")


def plot_accessibility_impact_cdf(stops_name: List[Tuple[str, str]], plot_x: int, plot_y: int,
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
    # pylint: disable=too-many-arguments, too-many-locals

    # Get metrics between before and after removing the stop
    results: List[CrossStopRemovalResult] = []

    for stop in get_stops_at_cross(stops_name):
        print(f"Getting the metrics of {stop.cross_name}")
        agents, weights = ctrl_population.get_population_points(stop.lat, stop.lon, range_km, interval_km)

        result = ctrl_stops_cross.get_metrics_of_single_stop_removal(stop.primary, stop.secondary, agents, weights)
        results.append(result)

    # Plot the data
    figure = generate_accessibility_plot_canvas(plot_x, plot_y, plot_stop_accessibility_cdf, results)
    figure.suptitle(title, y=0.99, fontsize=24)  # Enlarging the text and slightly reposition the title

    return figure


def plot_pop_density_top_12_positive_impact_cdf():
    """
    Plot and show the top 12 positive impact CDFs with population density points.

    ``range_km`` is set to **0.6** and ``interval_km`` is set to **0.05**.
    """
    figure = plot_accessibility_impact_cdf(TOP_12_POSITIVE_POP_DENSITY, 4, 3, 0.6, 0.05,
                                           "Top 12 stop removals that brings POSITIVE impacts")
    figure.show()


def plot_pop_density_top_12_negative_impact_cdf():
    """
    Plot and show the top 12 negative impact CDFs with population density points.

    ``range_km`` is set to **0.6** and ``interval_km`` is set to **0.05**.
    """
    figure = plot_accessibility_impact_cdf(TOP_12_NEGATIVE_POP_DENSITY, 4, 3, 0.6, 0.05,
                                           "Top 12 stop removals that brings NEGATIVE impacts")
    figure.show()
