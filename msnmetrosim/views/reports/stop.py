"""Get various reports related to stop data."""
from msnmetrosim.views.controllers import ctrl_stops, ctrl_ridership_stop


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
