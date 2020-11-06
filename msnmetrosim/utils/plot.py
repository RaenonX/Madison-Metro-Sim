"""Helper functions for plotting the data."""
from typing import Iterable, Tuple, Optional, Union

import matplotlib.pyplot as plt

__all__ = ("plot_twin_y", "plot_single", "plot_multiple")


def plot_single(x_data: Iterable[float], x_name: str, y_data: Iterable[float], y_name: str,
                title: Optional[str] = None):
    """Generate a plot with a single X and Y."""
    fig, axe = plt.subplots()

    axe.set_xlabel(x_name)
    axe.set_ylabel(y_name)
    axe.plot(x_data, y_data)
    axe.tick_params(axis="y")

    if title:
        axe.set_title(title)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()


def plot_multiple(x_data: Iterable[float], x_name: str,
                  y_data_collection: Iterable[Tuple[str, str, Iterable[float]]], y_name: str,
                  legend_title: str, legend_loc: Union[Tuple[float, float], str] = "lower right",
                  title: Optional[str] = None):
    """
    Generate a plot with a single X and multiple Y.

    For ``y_data_collection``, the 1st sub-element is the name of the data series;
    2nd sub-element is the line style and the 3rd element is the data series.

    Check https://matplotlib.org/3.3.2/api/_as_gen/matplotlib.lines.Line2D.html#matplotlib.lines.Line2D.set_linestyle
    for the line style string.
    """
    fig, axe = plt.subplots()

    axe.set_xlabel(x_name)
    axe.set_ylabel(y_name)
    for name, line_style, y_data in y_data_collection:
        axe.plot(x_data, y_data, label=name, linestyle=line_style)
    axe.tick_params(axis="y")

    fig.legend(title=legend_title, loc=legend_loc)
    if title:
        axe.set_title(title)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()


def plot_twin_y(x_data: Iterable[float], x_name: str,
                y1_data: Iterable[float], y1_name: str,
                y2_data: Iterable[float], y2_name: str,
                title: Optional[str] = None):
    """
    Generate a plot with 2 different series sharing the same X but different Y.

    ``y1`` will be plotted in red; ``y2`` will be plotted in blue.

    .. note::
        Copied and modified from https://matplotlib.org/gallery/api/two_scales.html
    """
    fig, ax1 = plt.subplots()

    color = "tab:red"
    ax1.set_xlabel(x_name)
    ax1.set_ylabel(y1_name, color=color)
    ax1.plot(x_data, y1_data, color=color)
    ax1.tick_params(axis="y", labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = "tab:blue"
    ax2.set_ylabel(y2_name, color=color)  # we already handled the x-label with ax1
    ax2.plot(x_data, y2_data, color=color, linestyle="dashed")
    ax2.tick_params(axis="y", labelcolor=color)

    if title:
        ax1.set_title(title)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()
