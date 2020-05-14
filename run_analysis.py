import field_model as fm
import matplotlib.pyplot as plt
import numpy as np


#Calculating the simulation
def compute_simulation(density_list, dim_x, dim_y, radius, height, ldr, speed, altitude, increment, strategy=False):
    res_tab = []
    energy_tab = []
    time_tab = []
    for density in density_list:
        scene = fm.Scene(dim_x, dim_y, radius, height, density, ldr, speed, altitude, increment)
        scene.glider.strategy = strategy
        #print(scene)
        scene.run()
        #print(scene)
        res_tab.append(scene.glider.pos_historic)
        energy_tab.append(scene.energyData)#liste de tuples (Ep, Ec, Em)
        time_tab.append(scene.time_data)
        #if density == 0.2 : print(scene)
        #print (scene.glider.pos_historic)
        #print(scene.glider)
    return res_tab, scene, energy_tab, time_tab

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

def plot_mechanical_energy(res_tab, energyData, scene, time):
    fig, axis = plt.subplots(2, 1, sharex='col')

    #plotting the first trajectory
    t = np.array(time[0])
    x = np.array([res_tab[0][j][0].x for j in range(len(res_tab[0]))])
    y = np.array([res_tab[0][j][0].y for j in range(len(res_tab[0]))])
    #d = np.sqrt(np.array(x) ** 2 + np.array(y) ** 2)
    z = np.array([res_tab[0][j][1] for j in range(len(res_tab[0]))])
    index_vache = 0
    while z[index_vache] > 0 and index_vache < len(z) - 1:
        index_vache += 1

    Ep = np.array([energyData[0][j][0] for j in range(len(x))])/1000
    Ec = np.array([energyData[0][j][1] for j in range(len(x))])/1000
    Em = np.array([energyData[0][j][2] for j in range(len(x))])/1000
    #print(len(t), len(d))
    ax = axis[0]
    print(t)
    print(z)
    ax.plot(t[1:], z[1:], label = "Altitude")
    t_vache = t[index_vache - 1]
    ax.plot([t_vache, t_vache], [-1000, scene.field.height], 'r')
    ax.set_ylabel("Altitude(m)")
    ax.legend()

    #plotting the corresponding energy
    ax2 = axis[1]
    ax2.plot()
    ax2.plot(t[1:], Ep[1:], label = "Énergie potentielle")
    ax2.plot(t[1:], Ec[1:], label = "Énergie cinétique")
    ax2.plot(t[1:], Em[1:], label = "Énergie mécanique")
    ax2.plot([t_vache, t_vache], [-5000, 5000], 'r')
    ax2.set_xlabel("t (s)")
    ax2.set_ylabel("Énergie (kJ)")
    ax2.legend()

    plt.show()
    return None


def statistical_energy_analysis (density,dim_x, dim_y, radius, height, ldr, speed, altitude, increment, strategy=False):
    """Computes 1000 scenes, for a total of 1000 runs, and calculates the average energy gained before hitting the ground and various other stuff"""
    density_list = [density for i in range(200)]
    res_tab, scene, energy_tab, time_tab = compute_simulation(density_list, dim_x, dim_y, radius, height, ldr, speed, altitude, increment, strategy)
    energy_added_list =[]
    t_vol_list = []
    d_vol_list = []
    for i in range(len(res_tab)) :
        #print(res_tab[i])
        x = [res_tab[i][j][0].x for j in range(len(res_tab[i]))]
        y = [res_tab[i][j][0].y for j in range(len(res_tab[i]))]
        d = np.sqrt(np.array(x)**2+np.array(y)**2)
        z = [res_tab[i][j][1]for j in range(len(res_tab[i]))]
        t = time_tab[i]
        index_vache = 0
        while z[index_vache]>0 and index_vache<len(z)-1:
            index_vache += 1
        additional_distance = d[index_vache]
        delta_z = 1000*additional_distance/ldr #convert to meters
        delta_e = scene.glider.mass*9.81*delta_z
        energy_added_list.append(delta_e)
        t_vol_list.append(t[index_vache])
        d_vol_list.append(d[index_vache])

    energy_mean = np.mean(np.array(energy_added_list))
    flight_time_mean = np.mean(np.array(t_vol_list))
    flight_distance_mean = np.mean(np.array(d_vol_list))
    if strategy : print("Strategy used")
    else : print("Naive flight")
    print('-----------------------------------------')
    print("Distance without thermals ", z[1]*ldr/1000, "km")
    print("Energy gained : ", energy_mean, " Joules")
    print("flight duration : ", flight_time_mean, " seconds")
    print("Distance : ", flight_distance_mean, " kilometers")
    print('-----------------------------------------')
    return energy_mean, flight_time_mean, flight_distance_mean


if __name__ == "__main__":
    # paramètres

    dim_x = 75  # km
    dim_y = 75  # km
    radius = 0.25  # km
    height = 2000  # vertical limit of the thermals field
    density_list = [0.1 for i in range(4)]#[0.1 * i for i in range(1, 5)]  # unit : km**(-2)
    ldr = 38
    speed = 105  # km/h
    altitude = 1200  # m, initial altitude
    increment = 10
    density = 0.07 #needed parameter for statistical_energy_analysis

    #tab_res, scene, energyData, timeData = compute_simulation(density_list, dim_x, dim_y, radius, height, ldr, speed, altitude, increment, True)
    #plot_flight_profile(tab_res, scene)
    #plot_mechanical_energy(tab_res, energyData, scene, timeData)
    print(statistical_energy_analysis(density,dim_x, dim_y, radius, height, ldr, speed, altitude, increment, False))