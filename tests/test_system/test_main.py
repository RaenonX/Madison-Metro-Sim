import os

from msnmetrosim.views import (
    generate_clean_map, generate_92_wkd_routes_and_stops, generate_92_wkd_routes_and_grouped_stops
)


def test_gen_clean_map():
    """Test if a clean map can be generated."""
    generate_clean_map().save("temp.html")

    # cleanup
    os.unlink("temp.html")


def test_gen_92_wkd_map():
    """Test if a map with routes in 92_WKD service plan and stops can be generated."""
    generate_92_wkd_routes_and_stops().save("temp.html")

    # cleanup
    os.unlink("temp.html")


def test_gen_92_wkd_map_grouped():
    """Test if a map with routes in 92_WKD service plan and stops grouped by cross can be generated."""
    generate_92_wkd_routes_and_grouped_stops().save("temp.html")

    # cleanup
    os.unlink("temp.html")
