import os

import pytest


@pytest.fixture
def performance_tolerance():
    """
    Get the performance tolerance multiplier from environment variables.

    The performance tolerance multiplier can be defined as ``TEST_PERFORMANCE_TOLERANCE`` in environment variables.

    If the variable is not defined, it will be defaulted to 1.

    Usage:

    >>> def test_somethings(performance_tolerance):
    >>>     # Some code
    >>>     code_performance = 5   # Takes 5 ms in normal to complete
    >>>     assert code_performance < 10 * performance_tolerance
    """
    tolerance = os.environ.get("TEST_PERFORMANCE_TOLERANCE")

    if tolerance:
        tolerance = float(tolerance)
        print(f"Testing performance tolerance multiplier set to: {tolerance}x")
    else:
        tolerance = 1
        print("Testing performance tolerance not set. Using the default value: 1.0x")

    return tolerance
