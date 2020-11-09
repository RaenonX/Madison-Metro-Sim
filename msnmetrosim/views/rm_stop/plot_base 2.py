"""Some shared base method for creating the plots."""
from typing import Tuple, List, Callable

import matplotlib.pyplot as plt

from msnmetrosim.models import MMTStopsAtCross
from msnmetrosim.models.results import CrossStopRemovalResult
from msnmetrosim.views.controllers import ctrl_stops_cross

__all__ = ("get_stops_at_cross", "generate_accessibility_plot_canvas")


def get_stops_at_cross(stops_name: List[Tuple[str, str]]) -> List[MMTStopsAtCross]:
    """Get a list of stops by its ``stops_name``."""
    # Get the stops by its streets
    stops_at_cross = []

    for primary, secondary in stops_name:
        print(f"Getting the stop of {primary} & {secondary}")
        grouped_stop = ctrl_stops_cross.get_grouped_stop_by_street_names(primary, secondary)
        if not grouped_stop:
            raise ValueError(f"Grouped stop of {primary} & {secondary} not found")

        stops_at_cross.append(grouped_stop)

    return stops_at_cross


def generate_accessibility_plot_canvas(plot_x: int, plot_y: int,
                                       subplot_func: Callable[[plt.Subplot, CrossStopRemovalResult], None],
                                       results: List[CrossStopRemovalResult], /,
                                       fig_size: int = 6):
    """
    Generate a ``plot_x`` x ``plot_y`` figure with the plots from ``subplot_func`` and return it.

    ``plot_x`` x ``plot_y`` must equal to the data count in ``results``.

    The metrics of the before and the after in each entry of ``results`` will be plotted to a single subplot.

    The function for plotting the result is ``subplot_func``.

    .. note::
        https://matplotlib.org/3.1.0/gallery/subplots_axes_and_figures/subplots_demo.html
    """
    # pylint: disable=invalid-name

    figure, axs = plt.subplots(plot_x, plot_y, figsize=(plot_x * fig_size, plot_y * fig_size))

    for x in range(plot_x):
        for y in range(plot_y):
            subplot_func(axs[x, y], results[x * plot_y + y])

    # pylint: enable=invalid-name, duplicate-code

    return figure
