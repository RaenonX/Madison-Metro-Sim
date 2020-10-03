import sys
import geopandas as gpd
import pandas as pd
from collections import defaultdict, OrderedDict

stops = gpd.read_file("../data_andy/Bus_Stops_and_Routes_Info/Metro_Transit_Bus_Stops-shp")

def plot_background(figsize=(12, 12)):
    """
    return an axes object with backgrounds of Madison city and the lakes around Madison
    :param figsize: adjust plot size
    :return: ax
    """
    water = gpd.read_file("../data_andy/Plot_Background/water-shp")
    city = gpd.read_file("../data_andy/Plot_Background/madison-shp")

    ax = water.plot(figsize=figsize, color="lightblue")
    city.plot(color="0.85", ax=ax)

    # ax.set_axis_off() # TODO: uncomment this
    return ax

def plot_route(ax=None, route_num=None): # TODO, add bus stop
    """
    return an axes object with the route on the plotted on the plot
    :param ax: if not specified, default is lake and madison city plot
    :param route_num: specified route number
    :return: ax
    """
    if ax == None:
        ax = plot_background()
    colored_routes = gpd.read_file("../data_andy/Bus_Stops_and_Routes_Info/colored_routes-shp")
    if route_num != None:
        wanted = colored_routes[colored_routes["route_shor"] == route_num]
        wanted.plot(color=wanted["route_colo"], ax=ax)

    else:
        colored_routes.plot(color=colored_routes["route_colo"], ax=ax)

    return ax

def get_number_of_bus_stops(route_num=None):
    """
    If route_num not specified, return the number of bus stops of all routes,
    else return the number of bus stops of the specified route_num.
    Note that an opposite-direction of the same bus stop is counted as twice.

    :param route_num: specified route num.
    :return: the number of bus stops of all routes or the specified route_num.
    """
    available_routes = defaultdict(int)

    for route in list(stops["Route"]):
        for r in route.split(","):
            if r != 'None':
                available_routes[int(r)] += 1

    if route_num == None:
        available_routes = dict(OrderedDict(sorted(available_routes.items())))
        return available_routes
    else:
        return available_routes[route_num]

def find_stop_of_route(route_num):
    """
    return a dataframe that has all stops of the specified route_num

    :param route_num: specified route_num
    :return: a dataframe of the stop information
    """
    stop_with_route = pd.DataFrame(columns=stops.columns)

    for i in range(len(stops)):
        if stops.loc[i, "Route"] == "None":
            continue
        if route_num in list(map(int, stops.loc[i, "Route"].split(","))):
            stop_with_route = stop_with_route.append(stops.iloc[i], ignore_index=True)

    return stop_with_route









def main(argv):
    pass
    # if len(argv) < 2:
    #     print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
    #     sys.exit(1)
    # # loops over all .json files in the argument
    # for f in argv[1:]:
    #     if isJson(f): # check file extenstion
    #         parseJson(f)
    #         print("Success parsing " + f)

if __name__ == '__main__':
    main(sys.argv)