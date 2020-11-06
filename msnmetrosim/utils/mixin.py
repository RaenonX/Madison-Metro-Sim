"""Misceallneous mixins."""
from abc import ABC

__all__ = ("TimeableMixin",)


class TimeableMixin(ABC):
    """Mixin for anything that can calculate time spent on that."""

    @property
    def time_spent(self) -> float:
        """Time spent in seconds."""
        raise NotImplementedError()
