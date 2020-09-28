"""Controllers that is ready for use to generate the data views.."""
from msnmetrosim.controllers import (
    # MMT GTFS data controllers
    MMTRouteDataController, MMTShapeDataController, MMTStopDataController, MMTStopsAtCrossDataController,
    MMTTripDataController,
    # Ridership data controllers
    RidershipByStopController
)

__all__ = ("ctrl_ridership_stop", "ctrl_routes", "ctrl_shapes", "ctrl_stops", "ctrl_stops_cross", "ctrl_trips")

# Load the controllers for use

ctrl_ridership_stop = RidershipByStopController.load_csv("ridership/by_stop.csv")
ctrl_routes = MMTRouteDataController.load_csv("mmt_gtfs/routes.csv")
ctrl_shapes = MMTShapeDataController.load_csv("mmt_gtfs/shapes.csv")
ctrl_stops = MMTStopDataController.load_csv("mmt_gtfs/stops.csv")
ctrl_stops_cross = MMTStopsAtCrossDataController.from_stop_controller(ctrl_stops)
ctrl_trips = MMTTripDataController.load_csv("mmt_gtfs/trips.csv")
