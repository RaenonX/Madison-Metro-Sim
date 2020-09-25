"""Stats object of the data."""
from dataclasses import dataclass, field, InitVar
from statistics import fmean, median, quantiles
from typing import List

__all__ = ("DataMetrics",)


@dataclass
class DataMetrics:
    """Get the metrics of a series of a data."""

    data: InitVar[List[float]]
    quantile_n: InitVar[int]

    cut_points: List[float] = field(init=False)
    """
    Cut points that separate the data equally in terms of count.

    This excludes the minimum and the maximum.
    """
    average: float = field(init=False)
    median: float = field(init=False)

    def __post_init__(self, data: List[float], quantile_n: int):
        self.cut_points = quantiles(data, n=quantile_n)
        self.average = fmean(data)  # Faster than `mean()` according to the doc
        self.median = median(data)
