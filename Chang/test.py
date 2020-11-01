import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import json
import time
import requests
from datetime import datetime, timedelta
from shapely.geometry import Point
from graph import Graph

DAY = "monday"
START_STOP = 765
START_TIME = "10:00:00"
ELAPSE_TIME = "00:10:00"
AVG_WALKING_SPEED = 3
MAX_WALKING_MIN = 10
MAX_WALKING_DISTANCE = MAX_WALKING_MIN / 60.0 * AVG_WALKING_SPEED

stops_df = pd.read_csv('data/chang/stops.txt', sep=",")
trips_df = pd.read_csv('data/chang/trips.txt', sep=",")
routeID_df = pd.read_csv('data/chang/routes.txt', sep=",")
stopTimes_df = pd.read_csv('data/chang/stop_times.txt', sep=",")
shape_df = pd.read_csv('data/chang/shapes.txt')
calendar_df = pd.read_csv('data/chang/calendar.txt')

def valid_service(day, start_date, end_date):
    return (day == 1) & (datetime.now() >= start_date) & (datetime.now() <= end_date)


def get_valid_stopTime(df, start_time, elapse_time):
    start_time = pd.to_timedelta(start_time)
    end_time = start_time + pd.to_timedelta(elapse_time)
    return df[(df['arrival_time'] > start_time) & (df['arrival_time'] < end_time)]

# get valid service_ids
calendar_df['start_date'] = pd.to_datetime(calendar_df['start_date'], format='%Y%m%d')
calendar_df['end_date'] = pd.to_datetime(calendar_df['end_date'], format='%Y%m%d')
calendar_filtered_df = calendar_df[valid_service(calendar_df[DAY], calendar_df["start_date"], calendar_df["end_date"])]
service_ids = calendar_filtered_df["service_id"].tolist()

# get valid trips
trips_filtered_df = trips_df[trips_df["service_id"].isin(service_ids)]

# get valid stop_times
stopTimes_filtered_df = trips_filtered_df.merge(stopTimes_df, on="trip_id")

stopTimes_merged_df = stopTimes_filtered_df.merge(stops_df, on="stop_id")[["service_id", "route_short_name", "trip_id", "stop_id", "stop_sequence", "arrival_time", "shape_dist_traveled", "stop_lat", "stop_lon", "cardinal_direction"]]

# get stop_times within the time frame
stopTimes_merged_df.loc[(stopTimes_merged_df.arrival_time.str.startswith('24')),'arrival_time'] = \
    stopTimes_merged_df.arrival_time.str.replace('24', '00')
stopTimes_merged_df.loc[(stopTimes_merged_df.arrival_time.str.startswith('25')),'arrival_time'] = \
    stopTimes_merged_df.arrival_time.str.replace('25', '01')
stopTimes_merged_df.loc[(stopTimes_merged_df.arrival_time.str.startswith('26')),'arrival_time'] = \
    stopTimes_merged_df.arrival_time.str.replace('26', '02')
stopTimes_merged_df.loc[(stopTimes_merged_df.arrival_time.str.startswith('27')),'arrival_time'] = \
    stopTimes_merged_df.arrival_time.str.replace('27', '03')
stopTimes_merged_df.loc[(stopTimes_merged_df.arrival_time.str.startswith('28')),'arrival_time'] = \
    stopTimes_merged_df.arrival_time.str.replace('28', '04')
stopTimes_merged_df.loc[(stopTimes_merged_df.arrival_time.str.startswith('29')),'arrival_time'] = \
    stopTimes_merged_df.arrival_time.str.replace('29', '05')
stopTimes_merged_df['arrival_time'] = pd.to_timedelta(stopTimes_merged_df['arrival_time'])

stopTimes_final_df = get_valid_stopTime(stopTimes_merged_df, START_TIME, ELAPSE_TIME).sort_values(by="arrival_time")

test_graph = Graph(stopTimes_final_df, START_STOP, MAX_WALKING_DISTANCE, AVG_WALKING_SPEED)
test_graph.dijkstra()