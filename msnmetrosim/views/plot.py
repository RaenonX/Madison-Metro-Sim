"""Functions for plotting the data."""
from typing import Optional

import matplotlib.pyplot as plt

from msnmetrosim.models import MMTStopsAtCross
from msnmetrosim.utils import DataMetrics

__all__ = ("plot_stop_removal_difference_metrics",)


def plot_stop_removal_difference_metrics(stop_removed: MMTStopsAtCross, before: DataMetrics, after: DataMetrics,
                                         fig_save_path: Optional[str] = None):
    """
    Plot the difference between before and after the stop removal.

    This function takes two metrics which represents the travel time to stops for each agents
    from their place to the removed stop before and after the removal.
    """
    # ----- Plot histogram
    # https://datavizpyr.com/overlapping-histograms-with-matplotlib-in-python/

    # Configure plot
    plt.figure(figsize=(10, 10))
    plt.xlabel("Distance to stop (km)", size=14)
    plt.ylabel("Agent count", size=14)
    plt.title(f"Distance to stop change between before and after removing {stop_removed.cross_name}")

    # Plot histogram
    plt.hist(before.data, bins=20, alpha=0.5, label="Before")
    plt.hist(after.data, bins=20, alpha=0.5, label="After")

    # Output plot image
    plt.legend(loc="upper right")
    if fig_save_path:
        # Save the figure of path provided
        plt.savefig(fig_save_path)
    plt.show()
