import time
from datetime import datetime

from msnmetrosim.utils import plot_multiple
from msnmetrosim.views import (
    # test_run,
    # Simulation graph benchmarking
    benchmark_map_construction,
    # Simulation benchmark plotting
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
    plot_multiple(
        list(range(10, 100, 10)),
        "Simulation time (mins)",
        [
            (
                "Graph Generation", "dashdot", [
                    1.564986, 1.821449, 2.485040, 3.429946, 4.576142, 5.923128, 7.881356, 9.760332, 11.980241
                ]
            ),
            (
                "Data Loading", "dashed", [
                    0.441076, 0.454345, 0.514306, 0.580983, 0.649454, 0.815186, 0.790881, 0.847786, 0.901834
                ]
            )
        ],
        "Time spent (secs)",
        "Process",
        title="Simulation Performance",
        legend_loc="upper left",
    )


if __name__ == '__main__':
    _start = time.time()
    main3()
    print(f"Time spent: {(time.time() - _start) * 1000:.3f} ms")
