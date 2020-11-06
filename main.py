import time
from datetime import datetime

from msnmetrosim.views import (
    # Graph simulation
    benchmark_map
)


def main():
    pass


def main2():
    travel_times = [600, 1200, 1800, 2700, 3600, 5400, 7200]

    start_coord = (43.069451, -89.401168)

    benchmark = benchmark_map(datetime(2020, 9, 2, 15), travel_times, start_coord,
                              map_action=lambda sim_map: print(sim_map))
    print(benchmark)


if __name__ == '__main__':
    _start = time.time()
    main()
    print(f"Time spent: {(time.time() - _start) * 1000:.3f} ms")
