"""
idée : créer plusieurs classes pour modéliser :
l'atm (P, rho, T) CHECK
les champs d'ascendances (list de thermals igc lib)
un point mobile (position, altitude, energie)

--> faire traverser le champs de thermiques en ligne droite aléatoire
    le point mobile pour trouver son libre parcours moyen

--> faire la même opération pour trouver le gain d'énergie mécanique
    sur un parcours en fonction de la distance

--> regarder le nombre de pompes observées par rapport à la distance

--> faire chacune des simulations pour plusieurs types de météos et
    tracer les courbes (lpm=f(T)=g(P), Energy=f(T), g(P), consommation% = f(T), g(P)
"""

import numpy.random as npr
import matplotlib.pyplot as plt
# import igc_lib as igc
# import data_analysis as data


def feet_to_meter(feet):
    return feet / 3.048


class Weather:

    def __init__(self, pressure=1013, temp_gnd=15, dew_point=10, humidity=30):
        self.pressure = pressure
        self.temp_gnd = temp_gnd + 273.15
        self.dew_point = dew_point + 273.15
        self.humidity = humidity
        self.rho = self.pressure * 100 / (287 * (self.temp_gnd + 273.15))

    def get_ceiling(self):
        ceiling_feet = 400 * (self.temp_gnd - self.dew_point)
        return feet_to_meter(ceiling_feet)

    def virtual_temp(self):
        return self.temp_gnd * (1013.25 / self.pressure) ** (2/7)

    def heat_flux(self):
        return 365 / (self.rho * 1006)

    def convective_speed(self):
        """
        :return: standard vertical speed of the air in the lifts of the weather area.
        This is not the real speed of climb in a lift but the theoretical one.
        For the practical one, see the thermal class
        """
        q = self.heat_flux()
        z_m = self.get_ceiling()
        theta = self.virtual_temp()
        return (q * 9.81 * z_m / theta) ** (1/3)


class Thermal:

    def __init__(self, longitude, latitude, weather):
        self.lon = longitude
        self.lat = latitude
        self.weather = weather

    def convective_standard_speed(self, altitude):
        """
        :param altitude:
        :return: a random speed for the lift, which will allow the non uniformity
        of the thermal array (each lift is not the same speed). This speed is given
        at a specific altitude, which is meant to be the 2/3 Zm altitude.
        """
        v_0 = self.weather.convective_speed()
        z_zm = altitude / self.weather.get_ceiling()
        sigma = (v_0 * v_0 * 1.8 * (z_zm ** (2/3)) * (1 - 0.8 * z_zm) ** 2) ** 0.5
        return list(npr.randn(1) * sigma + v_0)[0]

    def real_convective_speed(self, altitude, v_00=None):
        """
        :param altitude:
        :return: the real speed for the lift that will be effective for a plane crossing
        at this altitude. Is also meant to be calculated at the altitude 2/3 ZM.
        """
        z_zm = altitude / self.weather.get_ceiling()
        if v_00 is not None:
            v_0 = v_00
        else :
            v_0 = self.convective_standard_speed(altitude)+1.3
        return v_0 * (z_zm ** (1/3)) * (1 - 1.1 * z_zm)


mto = Weather(1028, 35, 16, 30)
z_m = mto.get_ceiling()
print(z_m)
print(mto.convective_speed())
print()
lift = Thermal(1, 2, mto)
# print(lift.convective_standard_speed(0.66 * z_m))
# print(lift.real_convective_speed(0.66 * z_m))

X = [lift.convective_standard_speed(z_m * 0.6) for _ in range(100000)]
Y = [lift.real_convective_speed(z_m * 0.6) for _ in range(100000)]
plt.hist(X, bins=65, normed=True, color="blue", alpha=0.5, label="lift speed")
plt.hist(Y, bins=65, normed=True, color="green", alpha=0.5, label="climb speed")
plt.grid()
plt.ylabel("proportion (probability)")
plt.xlabel("Vertical Speed (m/s)")
plt.title("Climb and Lift Vertical Speeds over\n20000 tries with the statistics model"
          "\n Weather (Temp:35°C ; DewPoint:16°C ; QNH:1028 hPa)"
          "\n Lift Ceiling : 2493 m, Study Altitude: 1620 m")
plt.legend()
plt.show()


"""altitude_ = [i/50 for i in range(0, 51)]
v_01 = mto.convective_speed()
v_speed = [lift.convective_standard_speed(alt * z_m) for alt in altitude_]
altiprint = [alt * z_m for alt in altitude_]
plt.plot(v_speed, altiprint)
plt.grid()
plt.xlabel("Vertical Speed in the lift (m/s)")
plt.ylabel("Altitude (m)")
plt.title("Lift profile function of altitude")
plt.show()"""

"""LAB = [i/100 for i in range(0, 26)]
LBC = [i/100 for i in range(25, 76)]
LCD = [i/100 for i in range(75, 101)]

L = LAB+LBC+LCD


def ty(LAB,LBC,LCD):
    AB = [0.5 * (1-x)**2 - 1/2 for x in LAB]
    BC = [0.5 * (1 - x) ** 2 - 1/2 for x in LBC]
    CD = [0.5 * (1-x)**2 for x in LCD]
    return AB+BC+CD


def Mz(LAB,LBC,LCD):
    AB = [(1/6) * (1-x)**3 - (1/12) * (0.75-x) - (5/12) * (0.25-x) for x in LAB]
    BC = [(1/6) * (1-x)**3 - (1/12) * (0.75-x) for x in LBC]
    CD = [(1/6) * (1-x)**3 for x in LCD]
    return AB+BC+CD


def Mx(LAB,LBC,LCD):
    AB = [- (1 - x) ** 2 * 0.1 /2 for x in LAB]
    BC = [- (1 - x) ** 2 * 0.1 /2 for x in LBC]
    CD = [- (1 - x) ** 2 * 0.1 /2 for x in LCD]
    return AB+BC+CD


N = [0 for _ in L]
TY = ty(LAB, LBC, LCD)
MZ = Mz(LAB, LBC, LCD)
MX = Mx(LAB, LBC, LCD)

fig, ax = plt.subplots(2,1)
ax[0].plot(L, N, label='N')
ax[0].plot(L, TY, label='Ty')
ax[0].legend()
ax[0].set_xlabel("pourcentage de L")
ax[0].set_ylabel('Efforts')
ax[0].grid()
ax[1].plot(L, MZ, label='Mz')
ax[1].plot(L, MX, label='Mx')
ax[1].grid()
ax[1].set_ylabel('Moments')
ax[1].legend()
plt.show()"""


