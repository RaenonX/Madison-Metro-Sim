"""Helper functions for plotting the data."""
from typing import Dict, Iterable, Optional, Sequence, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes

from .calc import normalize_vector

__all__ = ("plot_twin_y", "plot_single", "plot_multiple", "plot_discrete_distribution_normalized")


def plot_base(fn):
    """Wrapper for a plotting function to auto-fill the axe."""

    def plot_base_inner(*args, **kwargs):
        auto_gen = False

        if 'axe' not in kwargs or kwargs['axe'] is None:
            auto_gen = True
            fig, axe = plt.subplots()
            fig.tight_layout(pad=2)  # otherwise the right y-label is slightly clipped

            kwargs['axe'] = axe

        fn(*args, **kwargs)

        if auto_gen:
            plt.show()

    return plot_base_inner


@plot_base
def plot_single(x_data: Iterable[float], x_name: str, y_data: Iterable[float], y_name: str, /,
                title: Optional[str] = None, log_x: bool = False, log_y: bool = False, axe: Optional[Axes] = None):
    """Generate a plot with a single X and Y."""
    axe.set_xlabel(x_name)
    if log_x:
        axe.set_xscale('log')
    axe.set_ylabel(y_name)
    if log_y:
        axe.set_yscale('log')
    axe.plot(x_data, y_data)
    axe.tick_params(axis="y")

    if title:
        axe.set_title(title)


@plot_base
def plot_multiple(x_data: Iterable[float], x_name: str,
                  y_data_collection: Iterable[Tuple[str, str, Iterable[float]]], y_name: str,
                  legend_title: str, legend_loc: Union[Tuple[float, float], str] = "lower right",
                  title: Optional[str] = None, axe: Optional[Axes] = None):
    """
    Generate a plot with a single X and multiple Y.

    For ``y_data_collection``, the 1st sub-element is the name of the data series;
    2nd sub-element is the line style and the 3rd element is the data series.

    Check https://matplotlib.org/3.3.2/api/_as_gen/matplotlib.lines.Line2D.html#matplotlib.lines.Line2D.set_linestyle
    for the line style string.
    """
    axe.set_xlabel(x_name)
    axe.set_ylabel(y_name)
    for name, line_style, y_data in y_data_collection:
        axe.plot(x_data, y_data, label=name, linestyle=line_style)
    axe.tick_params(axis="y")

    axe.legend(title=legend_title, loc=legend_loc)
    if title:
        axe.set_title(title)


@plot_base
def plot_twin_y(x_data: Iterable[float], x_name: str,
                y1_data: Iterable[float], y1_name: str,
                y2_data: Iterable[float], y2_name: str, /,
                title: Optional[str] = None, axe: Optional[Axes] = None):
    """
    Generate a plot with 2 different series sharing the same X but different Y.

    ``y1`` will be plotted in red; ``y2`` will be plotted in blue.

    .. note::
        Copied and modified from https://matplotlib.org/gallery/api/two_scales.html
    """
    color = "tab:red"
    axe.set_xlabel(x_name)
    axe.set_ylabel(y1_name, color=color)
    axe.plot(x_data, y1_data, color=color)
    axe.tick_params(axis="y", labelcolor=color)

    ax2 = axe.twinx()  # instantiate a second axes that shares the same x-axis

    color = "tab:blue"
    ax2.set_ylabel(y2_name, color=color)  # we already handled the x-label with ax1
    ax2.plot(x_data, y2_data, color=color, linestyle="dashed")
    ax2.tick_params(axis="y", labelcolor=color)

    if title:
        axe.set_title(title)


@plot_base
def plot_discrete_distribution_normalized(categories: Sequence[str], results: Dict[str, Sequence[float]], /,
                                          title: Optional[str] = None, axe: Optional[Axes] = None):
    """
    Generate a normalized discrete distribution chart.

    .. note::
        Copied and modified from
        https://matplotlib.org/3.3.3/gallery/lines_bars_and_markers/horizontal_barchart_distribution.html
    """
    # pylint: disable=too-many-locals

    # Pre-process the data
    labels = [f"{label}\n({sum(results[label])})" for label in results.keys()]
    data_normalized = np.array([normalize_vector(vector) for vector in results.values()])  # Normalize data
    data_counts = list(results.values())  # To be used for indicating the data count
    data_cum = data_normalized.cumsum(axis=1)  # To be used for centering the texts

    # Get the color map to be used
    category_colors = plt.get_cmap("plasma")(np.linspace(0.15, 0.85, data_normalized.shape[1]))

    # Set the figure width to be 2 times the height
    axe.figure.set_size_inches(axe.figure.get_size_inches()[1] * 2, axe.figure.get_size_inches()[1])

    axe.invert_yaxis()
    axe.xaxis.set_visible(False)
    axe.set_xlim(0, 1)

    for cat_idx, (colname, color) in enumerate(zip(categories, category_colors)):
        bar_widths = data_normalized[:, cat_idx]
        bar_starts = data_cum[:, cat_idx] - bar_widths
        axe.barh(labels, bar_widths, left=bar_starts, height=0.5, label=colname, color=color)

        # Text plotting
        r, g, _, _ = color  # pylint: disable=invalid-name
        text_color = 'black' if max(r, g) > 0.5 else 'white'  # max(r, g) gets the B of HSB
        xcenters = bar_starts + bar_widths / 2

        # Plot texts
        for bar_idx, (xcenter, data_val) in enumerate(zip(xcenters, bar_widths)):
            if data_val > 0:  # Only plot the text if the data value is > 0
                axe.text(xcenter, bar_idx, f"{data_counts[bar_idx][cat_idx]}\n{data_val:.2%}",
                         ha='center', va='center', color=text_color)

    # Plot the legend at the left side
    axe.legend(ncol=len(categories), bbox_to_anchor=(0, 1),
               loc='lower left', fontsize='small')

    # Set title
    if title:
        axe.set_title(title)
