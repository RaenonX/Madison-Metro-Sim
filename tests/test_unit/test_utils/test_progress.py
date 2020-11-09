from time import sleep

from msnmetrosim.utils import Progress


def test_progress():
    count = 10
    interval = 0.1

    progress = Progress(count)
    progress.start()
    for i in range(count):
        sleep(interval)
        progress.rec_completed_one()
        assert progress.completed == i + 1
