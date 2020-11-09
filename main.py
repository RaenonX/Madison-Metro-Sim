import time

from msnmetrosim.views import (
    test_run,
    # Simulation graph benchmarking
    # benchmark_gen_map,
    # Simulation benchmark plotting
    # gen_map_only_df8d234f
)


def main():
    test_run()


def main2():
    pass


if __name__ == '__main__':
    _start = time.time()
    main()
    print(f"Time spent: {(time.time() - _start) * 1000:.3f} ms")
