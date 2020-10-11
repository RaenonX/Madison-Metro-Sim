"""Get various reports related to stop data."""
import matplotlib.pyplot as plt

from msnmetrosim.utils import generate_points
from msnmetrosim.views.controllers import ctrl_stops, ctrl_stops_cross, ctrl_ridership_stop

__all__ = ("get_stops_without_ridership", "get_distance_to_stop")


def get_stops_without_ridership():
    """Print the stops that do not have ridership data."""
    no_data = []

    for stop in ctrl_stops.all_data:
        ridership = ctrl_ridership_stop.get_stop_data_by_id(stop.stop_id)
        if ridership is None:
            no_data.append(stop)

    stops_without_ridership = [f"#{stop.stop_id:04} - {stop.stop_name}"
                               for stop in sorted(no_data, key=lambda data: data.stop_id)]

    print(f"{len(stops_without_ridership)} stops do not have ridership data:")
    for stop_without_ridership in stops_without_ridership:
        print(stop_without_ridership)


def get_distance_to_stop():
    """Get the travel time to ``target_stop``."""
    # Controllers to traverse
    target_stop = ctrl_stops_cross.get_grouped_stop_by_street_names("Inwood", "Open Wood")
    stop_cross_no_target = ctrl_stops_cross.duplicate(lambda data: data.unique_cross_id != target_stop.unique_cross_id)

    # Create simulated agents
    sim_agents = generate_points(target_stop.coordinate, 0.5, 0.02)

    # Get the distance metrics
    metrics_original = ctrl_stops_cross.get_distance_metrics_to_closest(sim_agents, "Original")
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
    plt.savefig("../assets/reports/0921-5.png")  # Save the figure
    plt.show()

    # Add function for searching the least impactful removal
    # - Replace the current content of 0921-04 and 0921-05, and plot it using (plot_stop_removal_difference_metrics)
