"""Stats object of the data."""
from dataclasses import dataclass, field, InitVar
from statistics import fmean, median, quantiles
from typing import List, Optional

__all__ = ("DataMetrics",)


@dataclass
class DataMetrics:
    """
    Get the metrics of a series of the data with some extra functionalities.

    .. note::
        https://docs.python.org/3/library/statistics.html
    """

    data: List[float]
    quantile_n: InitVar[int] = 10

    name: Optional[str] = None

    cut_points: List[float] = field(init=False)
    """
    Cut points that separate the data equally in terms of count.

    This excludes the minimum and the maximum.
    """
    average: float = field(init=False)
    median: float = field(init=False)

    def __post_init__(self, quantile_n: int):
        self.cut_points = quantiles(self.data, n=quantile_n)
        self.average = fmean(self.data)  # Faster than `mean()` according to the doc
        self.median = median(self.data)

    def print_stats(self):
        """Print the stats of this metric object to ``stdout``."""
        print(f"Distance metrics - {self.name}")
        print("================================")
        print(f"Cut Points: {self.cut_points}")
        print(f"Average: {self.average} / Median: {self.median}")
        print()
