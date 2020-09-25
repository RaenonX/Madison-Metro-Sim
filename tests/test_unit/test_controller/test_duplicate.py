from msnmetrosim.controllers import (
    MMTStopDataController, MMTStopsAtCrossDataController, MMTRouteDataController,
    MMTShapeDataController, MMTTripDataController, RidershipByStopController
)

_routes = MMTRouteDataController.load_csv("mmt_gtfs/routes.csv")
_shapes = MMTShapeDataController.load_csv("mmt_gtfs/shapes.csv")
_stops = MMTStopDataController.load_csv("mmt_gtfs/stops.csv")
_stops_cross = MMTStopsAtCrossDataController.from_stop_controller(_stops)
_trips = MMTTripDataController.load_csv("mmt_gtfs/trips.csv")
_ridership_stop = RidershipByStopController.load_csv("ridership/by_stop.csv")


def test_duplicate_route():
    sample_data = _routes.all_data[0]
    total_len = len(_routes.all_data)

    duplicated = _routes.duplicate(lambda data: data != sample_data)

    assert len(duplicated.all_data) < total_len


def test_duplicate_shape():
    sample_data = _shapes.all_data[0]
    total_len = len(_shapes.all_data)

    duplicated = _shapes.duplicate(lambda data: data != sample_data)

    assert len(duplicated.all_data) < total_len


def test_duplicate_stop():
    sample_data = _stops.all_data[0]
    total_len = len(_stops.all_data)

    duplicated = _routes.duplicate(lambda data: data != sample_data)

    assert len(duplicated.all_data) < total_len


def test_duplicate_stop_on_cross():
    sample_data = _stops_cross.all_data[0]
    total_len = len(_stops_cross.all_data)

    duplicated = _routes.duplicate(lambda data: data != sample_data)

    assert len(duplicated.all_data) < total_len


def test_duplicate_trip():
    sample_data = _trips.all_data[0]
    total_len = len(_trips.all_data)

    duplicated = _routes.duplicate(lambda data: data != sample_data)

    assert len(duplicated.all_data) < total_len


def test_duplicate_ridership_stop():
    sample_data = _ridership_stop.all_data[0]
    total_len = len(_ridership_stop.all_data)

    duplicated = _routes.duplicate(lambda data: data != sample_data)

    assert len(duplicated.all_data) < total_len
