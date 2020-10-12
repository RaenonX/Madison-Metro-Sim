"""Functions to visualize the stop removal related data."""
from .plot_cdf import plot_pop_density_top_12_positive_impact_cdf
from .plot_hist import (
    plot_dummy_top_12_positive_impact_histogram, plot_dummy_top_12_negative_impact_histogram
)
from .plot_map import generate_top_12_stops_map_dummy, generate_top_12_stops_map_pop_density
from .report import generate_stop_removal_report, get_report_rank_change, print_report_rank_change
