from __future__ import print_function
import igc_lib
import matplotlib.pyplot as plt
import geopandas
import numpy as np
import data_analysis


def make_list_of_tracks(repertoire, list_of_names_txt):
    list_filename = "IGC_FILES/" + repertoire + "/" + list_of_names_txt
    file = open(list_filename, 'r')
    data = file.readlines()
    list_of_track_names = list()
    for line in data:
        list_of_track_names.append(line[:-1])
    list_of_track_names[-1] += 'c'

    return list_of_track_names


def get_list_of_flight(repertoire, list_of_names_txt):
    list_of_flight = list()
    track_list = make_list_of_tracks(repertoire, list_of_names_txt)
    for name in track_list:
        flight = igc_lib.Flight.create_from_file("IGC_FILES/" + repertoire + '/' + name)
        if flight.valid:
            list_of_flight.append(flight)
    return list_of_flight


def get_thermal_list(list_flights):
    thermal_list = list()
    for flight in list_flights:
        thermal_list += flight.thermals
    return thermal_list


def plot_thermal_position(thermal_list_, ax, title="Graphics"):
    latitude, longitude = list(), list()
    for thermal in thermal_list_:
        latitude.append((thermal.enter_fix.lat + thermal.exit_fix.lat) / 2)
        longitude.append((thermal.enter_fix.lon + thermal.exit_fix.lon) / 2)

    ax.scatter(longitude, latitude)
    ax.set_xlabel("longitude (deg)")
    ax.set_ylabel("latitude (deg)")
    ax.grid(True)
    plt.title(title)


def plot_thermal_position_2(thermal_list_, ax, title="Graphics"):
    latitude, longitude, v_speed, altitude = list(), list(), list(), list()
    for thermal in thermal_list_:
        latitude.append((thermal.enter_fix.lat + thermal.exit_fix.lat) / 2)
        longitude.append((thermal.enter_fix.lon + thermal.exit_fix.lon) / 2)
        v_speed.append(thermal.vertical_velocity())
        altitude.append(thermal.exit_fix.gnss_alt - thermal.enter_fix.gnss_alt)

    scatter = ax.scatter(longitude, latitude, c=v_speed, s=altitude, alpha=0.4, cmap=plt.get_cmap("jet"))

    handles, labels = scatter.legend_elements(prop="sizes", alpha=0.6)
    legend1 = ax.legend(handles, labels, loc="upper left", title="Altitude Gain")
    handles, labels = scatter.legend_elements(prop="colors", alpha=0.6)
    legend2 = ax.legend(handles, labels, loc="lower left", title="Vertical Speed")

    ax.add_artist(legend1)
    ax.add_artist(legend2)
    ax.set_xlabel("longitude (deg)")
    ax.set_ylabel("latitude (deg)")
    ax.grid(True)
    plt.title(title)


def plot_over_map(thermal_list, ax, title="Graphics"):

    sorted_x_th = sorted(thermal_list, key=lambda thermal: (thermal.enter_fix.lon + thermal.exit_fix.lon) / 2)
    long_min, long_max = (sorted_x_th[0].enter_fix.lon + sorted_x_th[0].exit_fix.lon) / 2, \
                         (sorted_x_th[-1].enter_fix.lon + sorted_x_th[-1].exit_fix.lon) / 2
    sorted_y_th = sorted(thermal_list, key=lambda thermal: (thermal.enter_fix.lat + thermal.exit_fix.lat) / 2)
    lat_min, lat_max = (sorted_y_th[0].enter_fix.lat + sorted_y_th[0].exit_fix.lat) / 2, \
                       (sorted_y_th[-1].enter_fix.lat + sorted_y_th[-1].exit_fix.lat) / 2

    world = geopandas.read_file(geopandas.datasets.get_path('naturalearth_lowres'))
    world.plot(ax=ax)
    plot_thermal_position(thermal_list, ax, title=title)

    plt.xlim(long_min - 10, long_max + 10)
    plt.ylim(lat_min - 10, lat_max + 10)


def sort_by_date(flight_list):

    def date_to_str(date_):
        return str(date_.year) + "-" + str(date_.month) + "-" + str(date_.day)

    flight_per_date = dict()
    for flight in flight_list:
        date = date_to_str(flight.date)
        if flight_per_date.get(date):
            flight_per_date[date] += [flight]
        else:
            flight_per_date[date] = [flight]
    return flight_per_date


def main():
    repertoires = ["IGC_SO_18"]
    for rep in repertoires:
        repertoire, list_of_names_txt = rep, "list_files_igc_1.txt"
        list_of_flights = get_list_of_flight(repertoire, list_of_names_txt)
        dict_flight = sort_by_date(list_of_flights)
        for key, cont in dict_flight:
            print(key, len(cont))
        # thermal_list = get_thermal_list(list_of_flights)
        # print(thermal_list)
        # neighbors = data_analysis.find_k_neighbors(thermal_list, 5)
        # neighbors_list = list()
        # for neighbor in neighbors:
        #    neighbors_list += neighbor
        # distances = [neigh[1] for neigh in neighbors_list]
        # fig, ax = plt.subplots()
        # plot_over_map(thermal_list, title=rep, ax=ax)
        # plot_thermal_position_2(thermal_list, title="Graphics", ax=ax)
        # plt.show()


if __name__ == "__main__":
    main()
