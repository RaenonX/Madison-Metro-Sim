import time

from msnmetrosim.views import (
    generate_top_12_removal_map_pop_density,
    plot_pop_density_top_12_negative_impact_cdf, plot_pop_density_top_12_positive_impact_cdf
)


def main():
    print("Generating map object...")

    folium_map = generate_top_12_removal_map_pop_density()

    print("Exporting HTML...")
    folium_map.save("map.html")


def main2():
    plot_pop_density_top_12_positive_impact_cdf()
    plot_pop_density_top_12_negative_impact_cdf()


if __name__ == '__main__':
    _start = time.time()
    main2()
    print(f"Time spent: {(time.time() - _start) * 1000:.3f} ms")
