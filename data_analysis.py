import matplotlib.pyplot as plt
# import numpy as np
# import sklearn


def dispersions_use(thermal_list):
    vertical_speed = [thermal.vertical_velocity() for thermal in thermal_list]
    altitude_gain = [thermal.alt_change() for thermal in thermal_list]
    time_spent = [thermal.time_change() for thermal in thermal_list]
    fig, ax = plt.subplots(2, 1)
    ax[0].scatter(altitude_gain, vertical_speed, marker="x")
    ax[0].set_xlabel("Altitude Gain")
    ax[0].set_ylabel("Vertical Speed")
    ax[0].grid(True)
    ax[1].scatter(time_spent, vertical_speed, marker="x")
    ax[1].set_xlabel("Time spent in thermal")
    ax[1].set_ylabel("Vertical Speed")
    ax[1].grid(True)


def find_k_neighbors_of_one(list_thermal, index, k):
    thermal_init = list_thermal[index]

    list_for_zip = zip(list_thermal, [thermal_init.distance(therm) for therm in list_thermal])
    neighbors = sorted(list_for_zip, key=lambda a: a[1])[1:k+1]
    return neighbors


def find_k_neighbors(list_thermal, k):
    distances = list()
    for i in range(len(list_thermal)):
        distances.append(find_k_neighbors_of_one(list_thermal, i, k))
    return distances


