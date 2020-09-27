"""Functions to generate various text reports."""
from datetime import datetime

from msnmetrosim.controllers import MMTStopDataController, MMTStopsAtCrossDataController

__all__ = ("generate_stop_removal_report",)

_stops = MMTStopDataController.load_csv("mmt_gtfs/stops.csv")
_stops_cross = MMTStopsAtCrossDataController.from_stop_controller(_stops)


def generate_stop_removal_report(range_km: float, interval_km: float,
                                 report_path: str = "../reports/0921-report.txt"):
    """
    Generate a stop removal report with impact index included.

    This uses ``msnmetrosim.utils.generate_points()`` to generate dummy agents
    for simulating the accessibility difference,

    The report will be output to ``report_path``.
    """
    # Get a list of results of removing each stops
    results = _stops_cross.get_all_stop_remove_results(range_km, interval_km)

    # Generate the report to `reports/0921-report.txt`
    with open(report_path, "w") as f:
        f.write(f"Report on {datetime.now()} (CDT)\n")
        f.write("\n")
        f.write(f"Range: {range_km} km / Interval: {interval_km} km\n")

        # Get each removal results and sort them by impact index
        # Check the documentation of `impact_index` to get more information
        for rank, result in enumerate(sorted(results, key=lambda r: r.impact_index, reverse=True), start=1):
            f.write(f"#{rank} - Remove {result.stop_removed.cross_name}\n")
            f.write(f"Impact index: {result.impact_index:.4f}\n")
