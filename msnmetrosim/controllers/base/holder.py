"""Base classes for controller that holds data."""
from abc import ABC
from typing import Callable

__all__ = ("DataListHolder",)


class DataListHolder(ABC):
    """Controller base class that holds a list of data."""

    def __init__(self, data: list):
        self._data = data

    def duplicate(self, condition: Callable[[object], bool]):
        """Duplicate this controller with data matching the ``condition``."""
        return self.__class__([data for data in self._data if condition(data)])

    @property
    def all_data(self) -> list:
        """Get all the data held by this controller as :class:`list`."""
        return self._data
