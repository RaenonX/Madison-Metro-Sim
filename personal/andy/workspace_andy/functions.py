import sys
import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
import os

from collections import defaultdict, OrderedDict

stops = gpd.read_file("../../../data/bus_route_stop_info/stops-shp")
colored_routes = gpd.read_file("../../../data/bus_route_stop_info/routes_colored-shp")


def plot_background(ax=None, figsize=(12, 12)):
    """
    return an axes object with backgrounds of Madison city and the lakes around Madison
    :param figsize: adjust plot size
    :return: ax
    """
    water = gpd.read_file("../../../data/plot/background/water-shp")
    city = gpd.read_file("../../../data/plot/background/madison-shp")

    if ax == None:
        ax = water.plot(figsize=figsize, color="lightblue")
        city.plot(color="0.85", ax=ax)

    else:
        water.plot(ax=ax, figsize=figsize, color="lightblue")
        city.plot(color="0.85", ax=ax)

    # ax.set_axis_off() # TODO: uncomment this
    return ax

def plot_route(ax=None, route_num=None, **kwargs):
    """
    return an axes object with the route (already colored) on the plot

    :param ax: if not specified, default is lake and madison city plot
    :param route_num: specified route number
    :param kwargs: plot setting
    :return: ax with route plotted
    """
    if route_num == None:
        colored_routes.plot(ax=ax, color=colored_routes["route_colo"]  , **kwargs)
        return ax

    wanted = colored_routes[colored_routes["route_shor"] == route_num]
    wanted.plot(color=wanted["route_colo"], ax=ax, **kwargs)
    return ax

def plot_stops(ax, route_num, **kwargs):
    """
    This functions adds bus stops to the given axes object and returns ax.

    :param ax: axes object to plot.
    :param route_num: specified route number
    :param kwargs: plot setting
    :return: ax with bus stops plotted
    """
    if ax == None:
        plot_route(ax=ax, route_num=route_num)

    color = colored_routes[colored_routes["route_shor"] == route_num]["route_colo"].iloc[0] # color determined by colored_route
    route = get_stop_info_of_route(route_num)
    route.plot.scatter(ax=ax, x=["stop_lon"], y=["stop_lat"], color=color, **kwargs)

    return ax

# TODO: add a fake legend to display relative size of boarding
# reference:
# https://jakevdp.github.io/PythonDataScienceHandbook/04.06-customizing-legends.html
def plot_stops_sized(ax, route_num, day_type, **kwargs):
    """
    This functions adds bus stops to the given axes object sized by the number of boarding
    per each stop and returns ax.

    :param ax: axes object to plot.
    :param route_num: specified route number
    :param day_type: wkd, sat, sun
    :param kwargs: plot setting
    :return: ax with bus stops sized by boarding plotted
    """

    df = 0
    if day_type == "wkd":
        df = gpd.read_file("../../../data/ridership/by_stop_and_route/weekday-shp")
    elif day_type == "sat":
        df = gpd.read_file("../../../data/ridership/by_stop_and_route/saturday-shp")
    elif day_type == "sun":
        df = gpd.read_file("../../../data/ridership/by_stop_and_route/sunday-shp")
    else:
        return "day_type not found"

    df_route = pd.DataFrame(df)
    df_route = df_route[df_route["Route"] == route_num]
    color = colored_routes[colored_routes["route_shor"] == route_num]["route_colo"].iloc[0] # color determined by colored_route

    df_route.plot.scatter(ax=ax, x=["Lon"], y=["Lat"], s=df_route["DailyBoard"] * 2, color=color, **kwargs)
    # plt.legend(loc="upper left", frameon=False, fontsize=14, ncol=2)
    return ax


def get_num_stops_of_route(route_num=None):
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



def get_stop_info_of_route(route_num):
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
    if os.path.exists("../../../data/temp/matrix_nums.csv"):
        df = pd.read_csv("../../../data/temp/matrix_nums.csv").set_index("Unnamed: 0")
        df.index.names = [None]
        df.columns = [int(c) for c in df.columns]
        df.index = [int(i) for i in df.index]
        return df
    else:
        available_routes = get_num_stops_of_route().keys()  # dict
        md = dict()

        # create a matrix that shows each bus stop's overlap percentage
        for route_num in available_routes:
            md[route_num] = defaultdict(int)
            route_df = get_stop_info_of_route(route_num)  # df
            for i in range(len(route_df)):
                col_route = "".join(list(route_df.loc[i, "Route"])).split(", ")
                for r in col_route:
                    md[route_num][int(r)] += 1
            md[route_num] = dict(OrderedDict(sorted(md[route_num].items())))

        df = pd.DataFrame(md, columns=md.keys(), index=md.keys()).fillna(0)

        df.to_csv(path_or_buf="../../../data/temp/matrix_nums.csv")
        return df

def get_overlap_matrix_to_perc():
    """
    Return a DataFrame of the percentage of each route and the number of overlaps of bus stops of all routes.
    Reading from row to columns.

    :return: a DataFrame of percentages of overlaps.
    """
    if os.path.exists("../../../data/temp/matrix_perc.csv"):
        df = pd.read_csv("../../../data/temp/matrix_perc.csv").set_index("Unnamed: 0")
        df.index.names = [None]
        df.columns = [int(c) for c in df.columns]
        df.index = [int(i) for i in df.index]
        return df
    else:
        df = get_overlap_matrix()
        bus_stop_sum = get_num_stops_of_route()

        df_perc = pd.DataFrame(columns=df.columns, index=df.columns)
        for col in df.columns:
            df_perc[col] = df[col] / bus_stop_sum[col]
        df_perc.T.to_csv(path_or_buf="../../../data/temp/matrix_perc.csv")
        return df_perc.T


# need to be improved
def generate_color_map(threshold, savefig=False, filename=None):
    """
    generate a colormap of the overlapping percentages of each route

    :param threshold: specified threshold
    :param savefig:
    :return:
    """
    plt.rcParams["font.size"] = 10
    # plt.rcParams['xtick.bottom'] = plt.rcParams['xtick.labelbottom'] = False
    plt.rcParams['xtick.top'] = plt.rcParams['xtick.labeltop'] = True

    matrix_perc = get_overlap_matrix_to_perc()
    m = matrix_perc.to_numpy()
    fig = plt.figure(figsize=(14, 12))
    # img = plt.imshow(m, cmap = 'viridis', interpolation='nearest', vmax=threshold)
    img = plt.imshow(m, cmap=plt.cm.Blues, interpolation='nearest', vmax=threshold)

    plt.xticks(range(len(matrix_perc.index)), matrix_perc.index)
    plt.ylabel("Current Available Routes in Madison", fontsize=16)
    plt.yticks(range(len(matrix_perc.columns)), matrix_perc.columns)
    plt.title('Overlap Percentage of All Stops For Each Route', y=1.05, fontsize=16)
    plt.colorbar(img, label="Overlapping Percentage of Each Route")

    if savefig:
        plt.savefig("../brainstorm_report" + filename, dpi=300, bbox_inches='tight')
        # plt.savefig("../brainstorm_report", dpi=300, bbox_inches='tight')

    # Improvement
    # savefig = True
    # filename = "Number_of_Overlaps_cmap_YlGn.png"
    # threshold = 40
    #
    # plt.rcParams["font.size"] = 10
    # # plt.rcParams['xtick.bottom'] = plt.rcParams['xtick.labelbottom'] = False
    # plt.rcParams['xtick.top'] = plt.rcParams['xtick.labeltop'] = True
    #
    # matrix_num = functions.get_overlap_matrix()
    # m = matrix_num.to_numpy()
    # fig = plt.figure(figsize=(14, 12))
    # # img = plt.imshow(m, cmap = 'viridis', interpolation='nearest', vmax=threshold)
    # img = plt.imshow(m, cmap=plt.cm.YlGn, interpolation='nearest', vmax=threshold)
    #
    # plt.xticks(range(len(matrix_num.index)), matrix_num.index)
    # plt.ylabel("Current Available Routes in Madison", fontsize=16)
    # plt.yticks(range(len(matrix_num.columns)), matrix_num.columns)
    # plt.title('Number of Overlaps for Each Route', y=1.05, fontsize=16)
    # plt.colorbar(img, label="Number of Overlaps")
    #
    # if savefig:
    #     plt.savefig("../report_andy/Oct_05th/" + filename, dpi=300, bbox_inches='tight')



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