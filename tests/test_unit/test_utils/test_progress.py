from time import sleep

import pytest

from msnmetrosim.utils import Progress


def test_progress(is_github_actions):
    count = 10
    interval = 0.1

    progress = Progress(count)
    progress.start()
    for i in range(count):
        sleep(interval)
        progress.rec_completed_one()
        assert progress.completed == i + 1
        if not is_github_actions:
            assert progress.estimated_time_left == pytest.approx((count - i - 1) * interval, 0.1)
