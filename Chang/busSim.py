import pandas as pd
import geopandas as gpd
from datetime import datetime
from graph import Graph
import os


class BusSim:

    def __init__(self, data_path, day, start_time, elapse_time, avg_walking_speed, max_walking_min):
        self.day = day
        self.start_time = start_time
        self.elapse_time = elapse_time
        self.avg_walking_speed = avg_walking_speed
        self.max_walking_min = max_walking_min
        self.max_walking_distance = max_walking_min * 60.0 * avg_walking_speed
        self.stopTimes_final_df = self._gen_final_df(data_path)
        self.graph = Graph(self.stopTimes_final_df, start_time,
                           elapse_time, self.max_walking_distance, avg_walking_speed)

    def get_gdf(self, start_stop):
        gdf = self.graph.get_gdf(start_stop)

        gdf['geometry_centriod'] = gdf.geometry

        # https://epsg.io/3174
        gdf = gdf.to_crs(epsg=3174)
        gdf['geometry'] = gdf.geometry.buffer(gdf['radius'])
        gdf = gdf.to_crs(epsg=4326)
        return gdf

    def get_area(self, gdf):
        # the area returned is in meters^2
        lakes = gpd.read_file("../data/plot/background/water-shp")
        lakes = lakes.to_crs(epsg=3174)
        gdf = gdf.to_crs(epsg=3174)
        return gdf.unary_union.difference(lakes.unary_union).area

    def _gen_final_df(self, data_path):
        mmt_gtfs_path = os.path.join(data_path, "mmt_gtfs")
        stops_df = pd.read_csv(os.path.join(
            mmt_gtfs_path, "stops.csv"), sep=",")
        trips_df = pd.read_csv(os.path.join(
            mmt_gtfs_path, "trips.csv"), sep=",")
        stopTimes_df = pd.read_csv(os.path.join(
            mmt_gtfs_path, "stop_times.csv"), sep=",")
        calendar_df = pd.read_csv(os.path.join(
            mmt_gtfs_path, "calendar.csv"), sep=",")

        # get valid service_ids
        calendar_df['start_date'] = pd.to_datetime(
            calendar_df['start_date'], format='%Y%m%d')
        calendar_df['end_date'] = pd.to_datetime(
            calendar_df['end_date'], format='%Y%m%d')
        calendar_filtered_df = calendar_df[self._is_service_valid(
            calendar_df[self.day], calendar_df["start_date"], calendar_df["end_date"])]
        service_ids = calendar_filtered_df["service_id"].tolist()

        # get valid trips
        trips_filtered_df = trips_df[trips_df["service_id"].isin(service_ids)]

        # get valid stop_times
        stopTimes_filtered_df = trips_filtered_df.merge(
            stopTimes_df, on="trip_id")
        stopTimes_merged_df = stopTimes_filtered_df.merge(stops_df, on="stop_id")[
            ["service_id", "route_short_name", "trip_id", "stop_id", "stop_sequence", "arrival_time", "shape_dist_traveled", "stop_lat", "stop_lon", "cardinal_direction"]]

        # get stop_times within the time frame
        stopTimes_merged_df.loc[(stopTimes_merged_df.arrival_time.str.startswith('24')), 'arrival_time'] = \
            stopTimes_merged_df.arrival_time.str.replace('24', '00')
        stopTimes_merged_df.loc[(stopTimes_merged_df.arrival_time.str.startswith('25')), 'arrival_time'] = \
            stopTimes_merged_df.arrival_time.str.replace('25', '01')
        stopTimes_merged_df.loc[(stopTimes_merged_df.arrival_time.str.startswith('26')), 'arrival_time'] = \
            stopTimes_merged_df.arrival_time.str.replace('26', '02')
        stopTimes_merged_df.loc[(stopTimes_merged_df.arrival_time.str.startswith('27')), 'arrival_time'] = \
            stopTimes_merged_df.arrival_time.str.replace('27', '03')
        stopTimes_merged_df.loc[(stopTimes_merged_df.arrival_time.str.startswith('28')), 'arrival_time'] = \
            stopTimes_merged_df.arrival_time.str.replace('28', '04')
        stopTimes_merged_df.loc[(stopTimes_merged_df.arrival_time.str.startswith('29')), 'arrival_time'] = \
            stopTimes_merged_df.arrival_time.str.replace('29', '05')
        stopTimes_merged_df['arrival_time'] = pd.to_timedelta(
            stopTimes_merged_df['arrival_time'])

        stopTimes_final_df = self._get_valid_stopTime(
            stopTimes_merged_df, self.start_time, self.elapse_time).sort_values(by="arrival_time")

        return stopTimes_final_df

    def _is_service_valid(self, day, start_date, end_date):
        return (day == 1) & (datetime.now() >= start_date) & (datetime.now() <= end_date)

    def _get_valid_stopTime(self, df, start_time, elapse_time):
        start_time = pd.to_timedelta(start_time)
        end_time = start_time + pd.to_timedelta(elapse_time)
        return df[(df['arrival_time'] > start_time) & (df['arrival_time'] < end_time)]
