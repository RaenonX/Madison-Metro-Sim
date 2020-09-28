"""Views of the data. Maps to render should be generated from this module."""
from .mapgen import (
    generate_clean_map, generate_92_wkd_routes, generate_92_wkd_routes_and_stops,
    generate_92_wkd_routes_and_grouped_stops
)
from .rm_stop import (
    plot_top_12_positive_impact_results, plot_top_12_negative_impact_results,
    generate_stop_removal_report, generate_top_12_stops_map
)
