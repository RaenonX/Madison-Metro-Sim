"""Get reports related to stop data."""
import matplotlib.pyplot as plt

from msnmetrosim.controllers import MMTStopDataController, MMTStopsAtCrossDataController, RidershipByStopController
from msnmetrosim.utils import generate_points

_stops = MMTStopDataController.load_csv("mmt_gtfs/stops.csv")
_stops_cross = MMTStopsAtCrossDataController.from_stop_controller(_stops)
_ridership_stop = RidershipByStopController.load_csv("ridership/by_stop.csv")


def get_stops_without_ridership():
    """Print the stops that do not have ridership data."""
    no_data = []

    for stop in _stops.all_data:
        ridership = _ridership_stop.get_stop_data_by_id(stop.stop_id)
        if ridership is None:
            no_data.append(stop)

    stops_without_ridership = [f"#{stop.stop_id:04} - {stop.stop_name}"
                               for stop in sorted(no_data, key=lambda data: data.stop_id)]

    print(f"{len(stops_without_ridership)} stops do not have ridership data:")
    for stop_without_ridership in stops_without_ridership:
        print(stop_without_ridership)


def get_travel_time_to_stop():
    """Get the travel time to ``target_stop``."""
    # Controllers to traverse
    target_stop = _stops_cross.get_grouped_stop_by_street_names("Inwood", "Open Wood")
    stop_cross_no_target = _stops_cross.duplicate(lambda data: data.unique_cross_id != target_stop.unique_cross_id)

    # Create simulated agents
    sim_agents = generate_points(target_stop.coordinate, 0.5, 0.02)

    # Get the distance metrics
    metrics_original = _stops_cross.get_distance_metrics_to_closest(sim_agents, "Original")
    metrics_after = stop_cross_no_target.get_distance_metrics_to_closest(sim_agents, "Original")

    # ----- Plot histogram
    # https://datavizpyr.com/overlapping-histograms-with-matplotlib-in-python/

    # Configure plot
    plt.figure(figsize=(10, 10))
    plt.xlabel("Distance to stop (km)", size=14)
    plt.ylabel("Agent count", size=14)
    plt.title(f"Distance to stop change between before and after removing {target_stop.cross_name}")

    # Plot histogram
    plt.hist(metrics_original.data, bins=20, alpha=0.5, label="Original")
    plt.hist(metrics_after.data, bins=20, alpha=0.5, label="After")

    # Output plot image
    plt.legend(loc="upper right")
    # plt.savefig("../assets/reports/0921-5.png")  # Save the figure
    plt.show()


if __name__ == '__main__':
    get_travel_time_to_stop()
