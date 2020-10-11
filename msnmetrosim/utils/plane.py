"""Module for calculation related to a plane."""
from dataclasses import dataclass
from typing import Tuple, Optional

import numpy as np

__all__ = ("get_plane", "Plane")


# pylint: disable=invalid-name


@dataclass
class Plane:
    """A graphical plane."""

    normal: np.array
    d: np.array

    def get_z(self, x: float, y: float, min_val: Optional[float] = None) -> float:
        """
        Get the value of ``z`` given ``x`` and ``y``.

        If ``min_val`` is given, returned value will always be greater than or equal to ``min_val``.
        """
        z = (-self.normal[0] * x - self.normal[1] * y + self.d) / self.normal[2]

        if min_val is not None:  # explicitly checking because `min_val = 0` will not go here
            z = max(z, min_val)

        return z


def get_plane(points: Tuple[Tuple[float, float, float], Tuple[float, float, float], Tuple[float, float, float]]) \
        -> Plane:
    """
    Get a plane using exactly 3 ``points``.

    .. note::
        Copied and slightly modified from https://stackoverflow.com/q/53698635/11571888.
    """
    # pylint: disable=too-many-locals
    if len(points) != 3:
        raise ValueError(f"Count of points passed in is not 3 ({len(points)})")

    p0, p1, p2 = points

    x0, y0, z0 = p0
    x1, y1, z1 = p1
    x2, y2, z2 = p2

    ux, uy, uz = [x1 - x0, y1 - y0, z1 - z0]
    vx, vy, vz = [x2 - x0, y2 - y0, z2 - z0]

    u_cross_v = [uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx]

    point = np.array(p0)
    normal = np.array(u_cross_v)

    d = point.dot(normal)

    return Plane(normal, d)
