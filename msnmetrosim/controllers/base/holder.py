"""Base classes for controller that holds data."""
from abc import ABC

__all__ = ("DataListHolder",)


class DataListHolder(ABC):
    """Controller base class that holds a list of data."""

    # pylint: disable=too-few-public-methods

    def __init__(self, data: list):
        self._data = data

    @property
    def all_data(self) -> list:
        """Get all the data held by this controller as :class:`list`."""
        return self._data
