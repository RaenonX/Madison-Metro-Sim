import time
from datetime import datetime

from msnmetrosim.views import (
    test_run,
    # Simulation graph benchmarking
    benchmark_gen_map,
    # Simulation benchmark plotting
    gen_map_only_df8d234f
)


def main():
    # plot_travel_time_x_proc_time_n_count(gen_map_only_df8d234f)
    # plot_point_x_proc_time(gen_map_only_df8d234f)
    # plot_point_x_t_each_point(gen_map_only_df8d234f)
    # plot_point_count_x_proc_time_detailed(gen_map_only_df8d234f)
    # plot_point_count_x_gen_static(gen_map_only_df8d234f)
    print("Max. Travel Time (s) | Process Time (s) | Point Count | Point / s")
    print(":---: | :---: | :---: | :---:")
    for result in gen_map_only_df8d234f:
        print(result.travel_time, result.t_total, result.point_count, result.t_each_point, sep=" | ")


def main2():
    test_run()

    travel_times = range(600, 7800, 600)

    start_coord = (43.069451, -89.401168)

    benchmark = benchmark_gen_map(datetime(2020, 9, 2, 15), travel_times, start_coord,
                                  map_action=lambda sim_map: print(sim_map))
    for b in benchmark:
        print(b)


if __name__ == '__main__':
    _start = time.time()
    main()
    print(f"Time spent: {(time.time() - _start) * 1000:.3f} ms")
