import pytest

from msnmetrosim.utils import get_plane


def test_plane():
    get_plane(((0.65612, 0.53440, 0.24175),
               (0.62279, 0.51946, 0.25744),
               (0.61216, 0.53959, 0.26394)))


def test_plane_get_z():
    plane = get_plane(((0.65612, 0.53440, 0.24175),
                       (0.62279, 0.51946, 0.25744),
                       (0.61216, 0.53959, 0.26394)))

    assert plane.get_z(0.65612, 0.53440) == pytest.approx(0.24175)
    assert plane.get_z(0.62279, 0.51946) == pytest.approx(0.25744)
    assert plane.get_z(0.61216, 0.53959) == pytest.approx(0.26394)
    assert plane.get_z(0.64055, 0.52455) == pytest.approx(0.248907)


def test_plane_get_z_min():
    plane = get_plane(((0.65612, 0.53440, 0.24175),
                       (0.62279, 0.51946, 0.25744),
                       (0.61216, 0.53959, 0.26394)))

    assert plane.get_z(3000, 0.52455, -1) == pytest.approx(-1)
    assert plane.get_z(3000, 0.52455, 0) == pytest.approx(0)
    assert plane.get_z(3000, 0.52455) == pytest.approx(-1492.480107)
