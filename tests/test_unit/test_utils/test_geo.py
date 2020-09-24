from msnmetrosim.utils import distance, offset, time_function, generate_points


def test_offset_performance():
    result = time_function(offset, (43.073746, -89.406702), 0.1, 90, count=1000)
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


def test_points_in_range():
    result = time_function(generate_points, (43.084163, -89.324808), 2.0, 0.1)
    assert len(result.return_) == 1681
    for lat, lon in result.return_:
        assert isinstance(lat, float)
        assert isinstance(lon, float)

    result = time_function(generate_points, (43.084163, -89.324808), 0.3, 0.1)
    assert len(result.return_) == 49
    for lat, lon in result.return_:
        assert isinstance(lat, float)
        assert isinstance(lon, float)

    result = time_function(generate_points, (43.084163, -89.324808), 0.2, 0.1)
    assert len(result.return_) == 25
    for lat, lon in result.return_:
        assert isinstance(lat, float)
        assert isinstance(lon, float)

    result = time_function(generate_points, (43.084163, -89.324808), 0.01, 0.1)
    assert len(result.return_) == 1
    for lat, lon in result.return_:
        assert isinstance(lat, float)
        assert isinstance(lon, float)


def test_points_in_range_performance():
    result = time_function(generate_points, (43.084163, -89.324808), 2.0, 0.1)
    assert result.execution_ms < 5

    result = time_function(generate_points, (43.084163, -89.324808), 0.3, 0.1)
    assert result.execution_ms < 2.5

    result = time_function(generate_points, (43.084163, -89.324808), 0.2, 0.1)
    assert result.execution_ms < 1.5

    result = time_function(generate_points, (43.084163, -89.324808), 0.01, 0.1)
    assert result.execution_ms < 1.5
