"""Base dataclass for object that contains coordinates."""
from abc import ABC
from dataclasses import dataclass

__all__ = ("HasCrossModelBase",)


@dataclass
class HasCrossModelBase(ABC):
    """Interface for the data entry which is located on a cross (at least have properties of this)."""

    primary: str
    secondary: str

    @property
    def unique_cross_id(self) -> int:
        """Unique ID for identifying the street cross."""
        # timeit.timeit("hash(('A', 'B')) + hash(('B', 'A'))", number=5000000)
        # Out[10]: 0.6956078999999704
        # timeit.timeit("hash(tuple(sorted(('A', 'B'))))", number=5000000)
        # Out[11]: 1.2402921000000333
        #
        # Primary and secondary streets need to be switchable without changing the outcome
        return self.calculate_hash(self.primary, self.secondary)

    @property
    def cross_name(self):
        """
        Get the name of the cross.

        The return will be (<PRIMARY> & <SECONDARY>).
        """
        return f"{self.primary} & {self.secondary}"

    @staticmethod
    def calculate_hash(street_1: str, street_2: str):
        """Calculate an unique hash ID of a street cross."""
        return hash((street_1, street_2)) + hash((street_2, street_1))
