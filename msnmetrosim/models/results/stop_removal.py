"""Result of a single stop removal."""
from dataclasses import dataclass

from msnmetrosim.models import MMTStopsAtCross
from msnmetrosim.utils import DataMetrics

__all__ = ("CrossStopRemovalResult",)


@dataclass
class CrossStopRemovalResult:
    """Result of removing a single stop."""

    stop_removed: MMTStopsAtCross

    metrics_before: DataMetrics
    metrics_after: DataMetrics

    @property
    def impact_index(self) -> float:
        """
        Index of the impact.

        This sums the differences between the cut points of each metrics, then multiply the weight of it.
        """
        total_val = 0

        for weight, cut_point in enumerate(zip(self.metrics_before.cut_points, self.metrics_after.cut_points),
                                           start=1):
            before, after = cut_point

            total_val += (before - after) * weight

        return total_val
