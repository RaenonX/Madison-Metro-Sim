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


def test_closest_stop_performance():
    """Test if the performance of getting the closest stops is OK."""
    # In Cottage Grove, very distant from the bus stops (unusual case)
    result = time_function(mmt_stop_controller.find_closest_stop, 43.086601, -89.208467)
    assert result.execution_ms < 3.5

    # On Reddan Soccer Park, comparatively distant from the bus stops
    result = time_function(mmt_stop_controller.find_closest_stop, 43.006027, -89.524661)
    assert result.execution_ms < 2.5

    # In UW Campus, has a stop very close to this point
    result = time_function(mmt_stop_controller.find_closest_stop, 43.084163, -89.324808)
    assert result.execution_ms < 1.5

    # In NW of Lake Monona, on Walgreens, has a stop very close to this point
    result = time_function(mmt_stop_controller.find_closest_stop, 43.073746, -89.406702)
    assert result.execution_ms < 1.5
