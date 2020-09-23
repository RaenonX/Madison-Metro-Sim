"""Some static variables. For example: configurations, madison center coordinate, etc."""

# Map configurations
import os

MAP_CENTER_COORD = (43.080171, -89.380797)
"""The center coordinates of the map upon open."""

MAP_TILE = "CartoDB dark_matter"
"""Map tile style."""

MAP_ZOOM_START = 14
"""Map zoom scale upon open."""

# Data configurations

DATA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "data")
"""Directory of all data."""
