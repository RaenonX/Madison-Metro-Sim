"""Controllers that is ready for use to generate the data views.."""
from msnmetrosim.controllers import (
    # MMT GTFS data controllers
    MMTRouteDataController, MMTShapeDataController, MMTStopDataController, MMTStopsAtCrossDataController,
    MMTTripDataController, MMTStopScheduleController, MMTCalendarController,
    # Ridership data controllers
    RidershipByStopController,
    # Population data controllers
    PopulationDataController
)

__all__ = ("ctrl_calendar", "ctrl_routes", "ctrl_shapes", "ctrl_stops", "ctrl_stops_cross", "ctrl_stop_schedule",
           "ctrl_trips", "ctrl_ridership_stop",
           "ctrl_population")

# Load the controllers for use

# ---- Others

ctrl_population = PopulationDataController.load_csv("population.csv")
ctrl_ridership_stop = RidershipByStopController.load_csv("ridership/by_stop.csv")

# ---- MMT GTFS

ctrl_calendar = MMTCalendarController.load_csv("mmt_gtfs/calendar.csv")
ctrl_routes = MMTRouteDataController.load_csv("mmt_gtfs/routes.csv")
ctrl_shapes = MMTShapeDataController.load_csv("mmt_gtfs/shapes.csv")
ctrl_stops = MMTStopDataController.load_csv("mmt_gtfs/stops.csv")
ctrl_stops_cross = MMTStopsAtCrossDataController.from_stop_controller(ctrl_stops)
ctrl_stop_schedule = MMTStopScheduleController.load_csv("mmt_gtfs/stop_times.csv")
ctrl_trips = MMTTripDataController.load_csv("mmt_gtfs/trips.csv")
