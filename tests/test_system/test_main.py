import os

from msnmetrosim.views import generate_clean_map, generate_92_wkd_routes_and_stops


def test_gen_clean_map():
    generate_clean_map().save("temp.html")

    # cleanup
    os.unlink("temp.html")


def test_gen_92_wkd_map():
    generate_92_wkd_routes_and_stops().save("temp.html")

    # cleanup
    os.unlink("temp.html")
