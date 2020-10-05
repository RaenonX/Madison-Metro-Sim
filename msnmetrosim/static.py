"""Some static variables. For example: configurations, madison center coordinate, etc."""
import os

# Map configurations

MAP_MADISON_CENTER_COORD = (43.080171, -89.380797)
"""The center coordinates of the map upon opening."""

MAP_TILE = "CartoDB Positron"
"""Map tile style."""

MAP_ZOOM_START = 12
"""Map zoom scale upon opening."""

CONTROL_SCALE = True
"""To display a control scale on the map or not."""

# Data configurations

DATA_DIR = os.path.join(os.path.dirname(os.path.realpath(__file__)), "..", "data")
"""Directory of all data."""
