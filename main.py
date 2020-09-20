import csv

import folium


def main():
    m = folium.Map(location=[43.080171, -89.380797])

    # Read csv

    with open("data/mmt_gtfs/stops.csv", "r") as stops:
        csv_reader = csv.reader(stops, delimiter=",")
        next(csv_reader, None)  # Dump header

        for row in csv_reader:
            lat = float(row[4])
            lon = float(row[5])

            name = f"#{row[0]} - {row[2]}"

            folium.Circle((lat, lon), 0.5, popup=name).add_to(m)

    m.save("map.html")


if __name__ == '__main__':
    main()
