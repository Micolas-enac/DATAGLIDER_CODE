import numpy.random as rd
import matplotlib.pyplot as plt
import numpy as np


def deg_to_rad(deg):
    """
    :param deg: angle in degrees
    :return: angle in radians
    """
    return deg * np.pi/180


def intersect_solver(point_c, point_0, point_1, radius):
    """
    :param point_c: center of a circle
    :param point_0: first point to define the line path of the glider. Is used the last historic point found
    :param point_1: second point used to define the line path of the glider. Is used the detected position in the lift.
    :param radius:  radius of the lift field. given in km.
    :return: the lowest point of intersection between the circle and the line.
    """
    a = (point_1.y - point_0.y) / (point_1.x - point_0.x)
    b = point_0.y - a * point_0.x
    coeff_a = 1 + a ** 2
    coeff_b = 2 * a * (b-point_c.y) - 2 * point_c.x
    coeff_c = point_c.x ** 2 + (b - point_c.y) ** 2 - radius ** 2
    delta = coeff_b ** 2 - 4 * coeff_a * coeff_c
    if delta > 0:
        x = min((- coeff_b - delta ** 0.5) / (2 * coeff_a), (- coeff_b + delta ** 0.5) / (2 * coeff_a))
    else:
        x = point_0.x
    y = a * x + b
    return Point(x, y)


class Point:
    """
    This standard class is made to define points of coordinates x and y in 2D graphics.
    """

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return "({},{})".format(self.x, self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def distance(self, other):
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5

    def update(self, other):
        self.x = other.x
        self.y = other.y


class Field:
    """
    This class creates the field of lifts.
    """

    def __init__(self, dim_x, dim_y, radius, height=1000):
        """
        :param dim_x: x_width of the field
        :param dim_y: y_width of the field
        :param radius: radius of the lifts in the field
        :param height: height of the lifts in the field
        """
        self.dim_x = dim_x
        self.dim_y = dim_y
        self.lift = list()  # will contain the centers of the lifts
        self.radius = radius
        self.height = height

    def __repr__(self):
        fig, ax = plt.subplots()
        ax.set_aspect(1)  # aspect ratio of the drawing
        for point in self.lift:
            ax.add_artist(plt.Circle((point.x, point.y), self.radius, alpha=0.35))  # draw the circle of the lift
            ax.scatter(point.x, point.y, marker='2', color='black')  # draw the center point
        return ""  # just to avoid error from python

    def generate(self, density):
        """
        create a random distribution of lifts in the field with a certain density of lifts
        :param density: int which defines the number of lifts per km ** (-2)
        :return: nothing but fills up the self.lift
        """
        n = int(self.dim_x * self.dim_y * density)
        x_add, y_add = rd.uniform(0, self.dim_x, n), rd.uniform(0, self.dim_y, n)
        for i in range(len(x_add)):
            self.lift.append(Point(x_add[i], y_add[i]))


class Glider:
    """
    creates a simple object of gliding performance
    """

    def __init__(self, ldr, speed, altitude):
        self.ldr = ldr  # lift to drag ratio
        self.speed = speed  # speed of glide
        self.altitude = altitude  # altitude parameter (is function of time)
        self.position = Point(0, 0)  # initial position
        self.pos_historic = [(self.position, self.altitude)]  # historic of positions and alt. through the simulation

    def __repr__(self):
        x, y, alti = list(), list(), list()
        for (pos, alt) in self.pos_historic:
            x.append(pos.x)
            y.append(pos.y)
            alti.append(alt)
        plt.plot(x, y, dashes=[3, 2], color='grey')  # plots the path of the glider
        plt.scatter(x, y, marker='x', color='red')  # scatters the path colored with altitude
        return ""  # avoid error

    def in_lift(self, field):
        """
        check function to know if the glider has entered a lift or not yet.
        :param field:
        :return: the lift which was entered or None if no lift has been crossed yet
        """
        in_lift_in = list()
        for n in range(len(field.lift)):
            if self.position.distance(field.lift[n]) < field.radius:
                in_lift_in.append(field.lift[n])
        return in_lift_in[0] if len(in_lift_in) > 0 else Point(-1, -1)

    def in_scene(self, field):
        x_cond = self.position.x < field.dim_x
        y_cond = self.position.y < field.dim_y
        return x_cond or y_cond

    def update_position(self, time_increment, phi):
        """
        Update of the gliding position
        :param time_increment: time spent since last position
        :param phi: angle between the x-axis and the path that follows the glider (in degrees, betwwen 0 an 90)
        :return: a new position and ltitude depending on the case
        """
        x = self.position.x + 0.001 * (self.speed / 3.6) * time_increment * np.cos(deg_to_rad(phi))
        y = self.position.y + 0.001 * (self.speed / 3.6) * time_increment * np.sin(deg_to_rad(phi))
        self.position.update(Point(x, y))
        self.pos_historic.append((self.position, self.altitude))


class Scene:
    """
    create a Scene object to make the simulation work
    """
    def __init__(self, dim_x, dim_y, radius, height, density, ldr, speed, altitude, increment=10):
        self.field = Field(dim_x, dim_y, radius, height)  # creates an empty field
        self.field.generate(density)  # fills it with lifts
        self.glider = Glider(ldr, speed, altitude)  # places a glider
        self.time = 0  # initialize time to 0 (in seconds)
        self.increment = increment  # increment of time between to steps

    def __repr__(self):
        print(self.field)  # plot the field
        print(self.glider)  # plot the glider path at time of print
        plt.xlim(-2, self.field.dim_x + 2)
        plt.ylim(-2, self.field.dim_y + 2)
        plt.show()
        return ""  # avoid errors

    def update(self):
        """
        creates an iteration of the scene : updates time and position of the glider
        :return: scene object (self) updated
        """
        self.time += self.increment
        self.glider.update_position(self.increment, 45)

    def run(self):
        """
        main function : runs the simulation
        :return: time flown and mean free path
        """
        cross_lift_list = list()

        while self.glider.in_scene(self.field):  # while the glider is in the air
            # if the glider is not in a lift
            cross_lift_list.append(self.glider.in_lift(self.field))
            if self.glider.in_lift(self.field) == Point(-1, -1):
                self.update()  # update the scene
            else:
                new_x = self.glider.position.x + 2 * self.field.radius
                new_y = self.glider.position.y + 2 * self.field.radius
                self.glider.position.update(Point(new_x, new_y))

        crossed_lifts = [Point(0, 0)] + [point for point in cross_lift_list if point != Point(-1, -1)]
        m_f_p_l = list()
        for i in range(1, len(crossed_lifts)):
            m_f_p_l.append(crossed_lifts[i].distance(crossed_lifts[i-1]))
        return m_f_p_l


def main():
    n = 5
    RADIUS = 0.500
    dict_item = dict()
    density_list = [0.05 * i for i in range(1, 20)]
    for i in range(n):
        print(['XXX'*int(i+1)], i+1, '/', n)

        mean_fp_list = list()
        for density in density_list:
            scene = Scene(75, 75, radius=RADIUS, height=1600, density=density, ldr=30,
                          speed=98, altitude=1250, increment=20)
            m_f_p_l = scene.run()
            temp_add = 1 / np.mean(m_f_p_l) if m_f_p_l !=[] else 0
            if dict_item.get(density):
                dict_item[density] += temp_add
            else:
                dict_item[density] = temp_add
            mean_fp_list.append(temp_add)
        plt.plot(density_list, mean_fp_list, marker='+', linewidth=0.67)
        plt.scatter(density_list, mean_fp_list, marker='+', linewidth=0.9, color='black')
    values_to_fit = [value / n for value in dict_item.values()]
    fitting = np.polyfit(density_list, values_to_fit, 1)
    fitted = [fitting[0] * density + fitting[1] for density in density_list]
    plt.plot(density_list, fitted, linewidth='0.8', color='red')
    plt.grid(True)
    plt.xlabel('Inverted Lift Density $(km^{2})$')
    plt.ylabel('Mean Free Path $(km)$')
    bbox_props = dict(fc="w", ec="0.5", alpha=1)
    plt.text(0.28, 0.4, 'Lift radius : $500$ $m$ \nScene dimensions : $75x75$ $km$ \n $\lambda=' +
             '{:.3f}'.format(fitting[0])+'$', ha="center", va="center", size=9, bbox=bbox_props)
    plt.show()


if __name__ == '__main__':
    main()
