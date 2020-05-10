import field_model as fm
import matplotlib.pyplot as plt
import numpy as np


#Calculating the simulation
def compute_simulation(density_list, dim_x, dim_y, radius, height, ldr, speed, altitude, increment):
    res_tab = []
    for density in density_list:
        scene = fm.Scene(dim_x, dim_y, radius, height, density, ldr, speed, altitude, increment)
        #print(scene)
        scene.run()
        res_tab.append(scene.glider.pos_historic)
        #if density == 0.2 : print(scene)
        #print (scene.glider.pos_historic)
        #print(scene.glider)
    return res_tab, scene

#Analysis of results

def plot_flight_profile(res_tab, scene):

    print(res_tab)
    print(len(res_tab))
    fig, axis = plt.subplots(len(res_tab), 1, sharex = 'col')

    print(axis)
    for i in range(len(res_tab)) :
        #print(res_tab[i])
        x = [res_tab[i][j][0].x for j in range(len(res_tab[i]))]
        y = [res_tab[i][j][0].y for j in range(len(res_tab[i]))]
        d = np.sqrt(np.array(x)**2+np.array(y)**2)
        z = [res_tab[i][j][1]for j in range(len(res_tab[i]))]
        index_vache = 0
        while z[index_vache]>0 and index_vache<len(z)-1:
            index_vache += 1
        #print(x, len(x))
        ax = axis[i]
        ax.plot(d[1:], z[1:])
        d_vache = d[index_vache-1]
        ax.plot([d_vache,d_vache], [-1000, scene.field.height], 'r')
        ax.plot()
    plt.show()

    return None

def plot_mechanical_energy(tab_res):
    return None

if __name__ == "__main__":
    # paramètres

    dim_x = 75  # km
    dim_y = 75  # km
    radius = 0.5  # km
    height = 2000  # vertical limit of the thermals field
    density_list = [0.2 * i for i in range(1, 5)]  # unit : km**(-2)
    ldr = 38
    speed = 105  # km/h
    altitude = 1200  # m, initial altitude
    increment = 10

    tab_res, scene = compute_simulation(density_list, dim_x, dim_y, radius, height, ldr, speed, altitude, increment)
    plot_flight_profile(tab_res, scene)
