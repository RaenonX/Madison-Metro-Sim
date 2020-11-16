"""Functions for easier calculations."""
from typing import List, Iterable

__all__ = ("cumulate_vector", "normalize_vector", "normalize_cumulate_vector")


def cumulate_vector(vector: Iterable[float]) -> List[float]:
    """Cumulate ``vector``."""
    ret: List[float] = []
    for entry in vector:
        ret.append((ret[-1] if len(ret) > 0 else 0) + entry)

    return ret


def normalize_vector(vector: Iterable[float]) -> List[float]:
    """Normalize ``vector``, letting the sum of the vector to be 1."""
    total = sum(vector)

    return [item / total for item in vector]


def normalize_cumulate_vector(vector: Iterable[float]) -> List[float]:
    """Normalize and cumulate ``vector``."""
    normalized = normalize_vector(vector)

    return cumulate_vector(normalized)
