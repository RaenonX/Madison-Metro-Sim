from msnmetrosim.controllers import MMTStopDataController
from msnmetrosim.utils import time_function

mmt_stop_controller = MMTStopDataController.load_csv("mmt_gtfs/stops.csv")


def test_closest_stop():
    """Test if the closest stops can be acquired."""
    closest_stop = mmt_stop_controller.find_closest_stop(43.086601, -89.208467)
    assert abs(4.229083964374434 - closest_stop.distance) < 0.003
    assert closest_stop.stop.stop_id == 7811

    closest_stop = mmt_stop_controller.find_closest_stop(43.006027, -89.524661)
    assert abs(1.5473440806767247 - closest_stop.distance) < 0.003
    assert closest_stop.stop.stop_id == 8379

    closest_stop = mmt_stop_controller.find_closest_stop(43.084163, -89.324808)
    assert abs(0.019202918428765734 - closest_stop.distance) < 0.003
    assert closest_stop.stop.stop_id == 7215

    closest_stop = mmt_stop_controller.find_closest_stop(43.073746, -89.406702)
    assert abs(0.028556489501980448 - closest_stop.distance) < 0.003
    assert closest_stop.stop.stop_id == 706


def test_closest_stop_performance(performance_tolerance):
    """Test if the performance of getting the closest stops is OK."""
    # In Cottage Grove, very distant from the bus stops (unusual case)
    result = time_function(mmt_stop_controller.find_closest_stop, 43.086601, -89.208467, count=1000)
    # Expected to be 1300~1500 ms / 2000 ms on Github Actions
    assert result.execution_ms < 2000 * performance_tolerance

    # On Reddan Soccer Park, comparatively distant from the bus stops
    result = time_function(mmt_stop_controller.find_closest_stop, 43.006027, -89.524661, count=1000)
    # Expected to be 1000 ms / 1500~1700 ms on Github Actions
    assert result.execution_ms < 1500 * performance_tolerance

    # In UW Campus, has a stop very close to this point
    result = time_function(mmt_stop_controller.find_closest_stop, 43.084163, -89.324808, count=1000)
    # Expected to be 80~110 ms
    assert result.execution_ms < 250 * performance_tolerance

    # In NW of Lake Monona, on Walgreens, has a stop very close to this point
    result = time_function(mmt_stop_controller.find_closest_stop, 43.073746, -89.406702, count=1000)
    # Expected to be 90~130 ms
    assert result.execution_ms < 220 * performance_tolerance
