"""Stats object of the data."""
from dataclasses import dataclass, field
from statistics import fmean, median, quantiles
from typing import List, Optional, Tuple

__all__ = ("DataMetrics",)


@dataclass
class DataMetrics:
    """
    Get the metrics of a series of the data with some extra functionalities.

    .. note::
        https://docs.python.org/3/library/statistics.html
    """

    data: List[float]

    name: Optional[str] = None

    average: float = field(init=False)
    median: float = field(init=False)

    def __post_init__(self):
        self.average = fmean(self.data)  # Faster than `mean()` according to the doc
        self.median = median(self.data)

    def get_quantile(self, n: int) -> List[float]:  # pylint: disable=invalid-name
        """Call ``statistics.quantiles()`` on the data with count ``n``, and return it."""
        return quantiles(self.data, n=n)

    def get_quantile_cdf(self, n: int) -> Tuple[List[float], List[float]]:  # pylint: disable=invalid-name
        """
        Same as ``get_quantile()``, but the return will be ``(X_ARRAY, Y_ARRAY)`` for easier plotting.

        Y will be 0 <= x <= 1, and it will always starts from 0 and ends at 1.
        """
        x_array = [min(self.data)] + self.get_quantile(n) + [max(self.data)]
        y_array = [i / n for i in range(n)] + [1]

        return x_array, y_array

    def print_stats(self):
        """Print the stats of this metric object to ``sys.stdout``."""
        print(f"Data metrics - {self.name or '(No name)'}")
        print("================================")
        print(f"Average: {self.average} / Median: {self.median}")
        print(f"Decile: {self.get_quantile(10)}")
        print()
