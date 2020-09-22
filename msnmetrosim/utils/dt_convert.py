"""Conversion functions related to datetime."""
from datetime import time

__all__ = ("time_from_seconds",)


def time_from_seconds(seconds: int) -> time:
    """Convert ``seconds`` to :class:`time`."""
    # ``seconds`` passed in may be > 86400 (a day), which causes ``hours`` to be invalid.
    # One example is that ``trips.txt:trip_sort`` contains value > 86400.
    seconds %= 86400

    # Not directly modifying ``seconds`` for easier debugging (check the original input)
    hours, secs = divmod(seconds, 3600)
    mins, secs = divmod(secs, 60)
    return time(hours, mins, secs)
