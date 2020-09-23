"""Get reports related to stop data."""
from msnmetrosim.controllers import MMTStopDataController, RidershipByStopController

_stops = MMTStopDataController.load_csv("mmt_gtfs/stops.csv")
_ridership_stop = RidershipByStopController.load_csv("ridership/by_stop.csv")


def get_stops_without_ridership():
    """Print the stops that do not have ridership data."""
    no_data = []

    for stop in _stops.get_all_stops():
        ridership = _ridership_stop.get_stop_data_by_id(stop.stop_id)
        if ridership is None:
            no_data.append(stop)

    stops_without_ridership = [f"#{stop.stop_id:04} - {stop.stop_name}"
                               for stop in sorted(no_data, key=lambda data: data.stop_id)]

    print(f"{len(stops_without_ridership)} stops do not have ridership data:")
    for stop_without_ridership in stops_without_ridership:
        print(stop_without_ridership)


if __name__ == '__main__':
    get_stops_without_ridership()
