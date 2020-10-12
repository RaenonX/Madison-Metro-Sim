import time

from msnmetrosim.views import (
    generate_map_with_points, print_report_rank_change
)
from msnmetrosim.views.controllers import ctrl_population


def main():
    print("Generating map object...")

    folium_map = generate_map_with_points([data.coordinate for data in ctrl_population.all_data])

    print("Exporting HTML...")
    folium_map.save("map.html")


def main2():
    print_report_rank_change("assets/reports/attachments/1012/impact-idx-pop.csv",
                             "assets/reports/attachments/0928/impact-idx-dummy.csv", 12)
    # print_report_rank_change("assets/reports/attachments/0928/impact-idx-dummy.csv",
    #                          "assets/reports/attachments/1012/impact-idx-pop.csv", 12)


if __name__ == '__main__':
    _start = time.time()
    main2()
    print(f"Time spent: {(time.time() - _start) * 1000:.3f} ms")
