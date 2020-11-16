import time
from datetime import datetime

from msnmetrosim.views import (
    # test_run,
    # Simulation graph benchmarking
    benchmark_map_construction,
    # Simulation benchmark plotting
    plot_trip_count_cdf, post_152f1000_pruned_no_detouring
)


def main():
    # Benchmark with pruning, max transfer 1~5

    travel_time = 1800

    results = []

    for max_transfer in range(5):
        results.extend(benchmark_map_construction(
            datetime(2020, 9, 2, 15),
            [travel_time],
            (43.069451, -89.401168),
            max_transfer=max_transfer
        ))

    print(f"{'=' * 50} RESULTS {'=' * 50}")
    for max_transfer, result in enumerate(results):
        print()
        print(f"{'=' * 20} Max transfer = {max_transfer}")
        print()
        print(result)


def main2():
    travel_time = 2700

    results = benchmark_map_construction(
        datetime(2020, 9, 2, 15),
        [travel_time],
        (43.069451, -89.401168),
    )
    print(f"{'=' * 50} RESULTS {'=' * 50}")
    print()
    print(results[0])
    print()


def main3():
    plot_trip_count_cdf(post_152f1000_pruned_no_detouring)


if __name__ == '__main__':
    _start = time.time()
    main3()
    print(f"Time spent: {(time.time() - _start) * 1000:.3f} ms")
