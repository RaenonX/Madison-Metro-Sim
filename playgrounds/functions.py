import sys
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import os

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

def plot_route(ax=None, route_num=None, **kwargs): # TODO, add bus stop
    """
    return an axes object with the route on the plotted on the plot
    :param ax: if not specified, default is lake and madison city plot
    :param route_num: specified route number
    :return: ax with route plotted
    """
    if ax == None:
        ax = plot_background()
    colored_routes = gpd.read_file("../data_andy/Bus_Stops_and_Routes_Info/colored_routes-shp")
    if route_num != None:
        wanted = colored_routes[colored_routes["route_shor"] == route_num]
        wanted.plot(color=wanted["route_colo"], ax=ax, **kwargs)

    else:
        colored_routes.plot(color=colored_routes["route_colo"], ax=ax, **kwargs)

    return ax

def get_bus_stops_of_route(route_num=None):
    """
    If route_num not specified, return the number of bus stops of all routes,
    else return the number of bus stops of the specified route_num.
    Note that an opposite-direction of the same bus stop is counted as twice.

    :param route_num: specified route num.
    :return: a dictionary, route: num of bus stops
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


# example code:
# route_num = 80
# ax = functions.plot_route(functions.plot_background(), route_num)
# route_80 = functions.find_stop_of_route(route_num)
# route_80.set_geometry("geometry").plot(ax=ax, markersize=2, zorder=2)
def get_stop_locations_of_route(route_num):
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


def get_overlap_matrix():
    """
    return a DataFrame of each route and the number of overlaps of bus stops of all routes

    :return: a DataFrame of numbers of overlaps
    """
    if os.path.exists("../data_andy/route_overlap/matrix_nums.csv"):
        df = pd.read_csv("../data_andy/route_overlap/matrix_nums.csv").set_index("Unnamed: 0")
        df.index.names = [None]
        df.columns = [int(c) for c in df.columns]
        df.index = [int(i) for i in df.index]
        return df
    else:
        available_routes = get_bus_stops_of_route().keys()  # dict
        md = dict()

        # create a matrix that shows each bus stop's overlap percentage
        for route_num in available_routes:
            md[route_num] = defaultdict(int)
            route_df = get_stop_locations_of_route(route_num)  # df
            for i in range(len(route_df)):
                col_route = "".join(list(route_df.loc[i, "Route"])).split(", ")
                for r in col_route:
                    md[route_num][int(r)] += 1
            md[route_num] = dict(OrderedDict(sorted(md[route_num].items())))

        df = pd.DataFrame(md, columns=md.keys(), index=md.keys()).fillna(0)

        df.to_csv(path_or_buf="../data_andy/route_overlap/matrix_nums.csv")
        return df

def get_overlap_matrix_to_perc():
    """
    Return a DataFrame of the percentage of each route and the number of overlaps of bus stops of all routes.
    Reading from row to columns.

    :return: a DataFrame of percentages of overlaps.
    """
    if os.path.exists("../data_andy/route_overlap/matrix_perc.csv"):
        df = pd.read_csv("../data_andy/route_overlap/matrix_perc.csv").set_index("Unnamed: 0")
        df.index.names = [None]
        df.columns = [int(c) for c in df.columns]
        df.index = [int(i) for i in df.index]
        return df
    else:
        df = get_overlap_matrix()
        bus_stop_sum = get_bus_stops_of_route()

        df_perc = pd.DataFrame(columns=df.columns, index=df.columns)
        for col in df.columns:
            df_perc[col] = df[col] / bus_stop_sum[col]
        df_perc.T.to_csv(path_or_buf="../data_andy/route_overlap/matrix_perc.csv")
        return df_perc.T

def generate_color_map(threshold, savefig=False):
    """
    generate a colormap of the overlapping percentages of each route

    :param threshold: specified threshold
    :param savefig:
    :return:
    """
    plt.rcParams["font.size"] = 10
    plt.rcParams['xtick.bottom'] = plt.rcParams['xtick.labelbottom'] = False
    plt.rcParams['xtick.top'] = plt.rcParams['xtick.labeltop'] = True

    matrix_perc = get_overlap_matrix_to_perc()
    m = matrix_perc.to_numpy()
    fig = plt.figure(figsize=(14, 12))
    # img = plt.imshow(m, cmap = 'viridis', interpolation='nearest', vmax=threshold)
    img = plt.imshow(m, cmap=plt.cm.Blues, interpolation='nearest', vmax=threshold)

    plt.xticks(range(len(matrix_perc.index)), matrix_perc.index)
    plt.yticks(range(len(matrix_perc.columns)), matrix_perc.columns)
    plt.title('Overlap percentage of all stops for each route', y=1.05, fontsize=16)
    plt.colorbar(img)

    if savefig:
        plt.savefig("../report_andy/try.png", dpi=300, bbox_inches='tight')
        # plt.savefig("../report_andy/Overlap_Percentage_cmap_viridis.png", dpi=300, bbox_inches='tight')



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