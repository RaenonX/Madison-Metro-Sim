import time

from msnmetrosim.views import generate_92_wkd_routes_and_grouped_stops


def main():
    print("Generating map object...")
    folium_map = generate_92_wkd_routes_and_grouped_stops()

    print("Exporting HTML...")
    folium_map.save("map.html")


if __name__ == '__main__':
    _start = time.time()
    main()
    print(f"Time spent: {(time.time() - _start) * 1000:.3f} ms")
