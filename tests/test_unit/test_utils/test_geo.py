from msnmetrosim.utils import distance, offset, time_function


def test_offset_performance():
    result = time_function(offset, (43.073746, -89.406702), 0.1, count=1000)
    assert result.execution_ms < 3  # Expected 1 or 2 ms

    returned_coord = result.return_[0]
    assert len(returned_coord) == 2
    assert isinstance(returned_coord[0], float)
    assert isinstance(returned_coord[1], float)


def test_distance_performance():
    result = time_function(distance, (43.084163, -89.324808), (43.073746, -89.406702), count=1000)
    assert result.execution_ms < 3  # Expected 1 or 2 ms

    returned_dist = result.return_[0]
    assert isinstance(returned_dist, float)
