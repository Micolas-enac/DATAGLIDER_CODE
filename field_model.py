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
            ax.scatter(point.x, point.y, marker='2', color='black') # draw the center point
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
        plt.scatter(x, y, marker='x', c=alti, cmap=plt.get_cmap('jet'))  # scatters the path colored with altitude
        return ""  # avoid error

    def in_lift(self, field):
        """
        check function to know if the glider has entered a lift or not yet.
        :param field:
        :return: the lift which was entered or None if no lift has been crossed yet
        """
        for l in field.lift:
            print(l)
            if self.position.distance(l) < field.radius:
                return l
            else:
                pass
        return None

    def in_scene(self, field):
        x_cond = self.position.x > field.dim_y
        y_cond = self.position.y > field.dim_y
        return not(x_cond or y_cond)

    def update_position(self, time_increment, phi, field):
        """
        Update of the gliding position
        :param time_increment: time spent since last position
        :param phi: angle between the x-axis and the path that follows the glider (in degrees, betwwen 0 an 90)
        :param field: field of evolution of the glider
        :return: a new position and ltitude depending on the case
        """
        x = self.position.x + 0.001 * (self.speed / 3.6) * time_increment * np.cos(deg_to_rad(phi))
        y = self.position.y + 0.001 * (self.speed / 3.6) * time_increment * np.sin(deg_to_rad(phi))
        self.position = Point(x, y)
        if self.in_lift(field) is not None:  # if a lift is crossed,
            # update the position in order to find the intersection with the lift
            position_temp = intersect_solver(self.in_lift(field), self.pos_historic[-1][0], self.position, field.radius)
            self.position = position_temp
        else:  # else, continue to follow a direct path descending
            # alti = self.altitude - (self.speed/3.6) * time_increment / self.ldr
            # self.altitude = alti  # if alti > 0 else 0
            return
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
        plt.show()
        return ""  # avoid errors

    def update(self):
        """
        creates an iteration of the scene : updates time and position of the glider
        :return: scene object (self) updated
        """
        self.time += self.increment
        self.glider.update_position(self.increment, 30, self.field)

    def run(self):
        """
        main function : runs the simulation
        :return: time flown and mean free path
        """
        while True:  # while the glider is in the air
            # if the glider is not in a lift and still in the field

            if self.glider.in_lift(self.field) is None:
                if self.glider.in_scene(self.field):
                    # if not self.glider.not_in_scene(self.field):
                    self.update()  # update the scene
                else:
                    break
                # else:
                # else, the glider has flown all over the field
                #    break
            # if the glider crosses a lift
            else:
                break
        # give final interest parameters if the glider has flown until ground
        temp = self.glider.altitude if self.glider.altitude > 0 else 0
        self.glider.altitude = temp
        print("TIME FLOWN=", self.time, 'sec')
        print("LPR =", self.glider.position.distance(Point(0, 0)), 'km')
        return self.glider.position.distance(Point(0, 0))


def main():
    n = 1
    free_mean_path = list()
    for _ in range(n):
        scene = Scene(10, 10, radius=0.3, height=1600, density=0.5, ldr=30, speed=98, altitude=1250, increment=20)
        print(scene)
        print(scene.glider.in_scene(scene.field))
        free_mean_path.append(scene.run())
        print(scene)
    print(free_mean_path)


if __name__ == '__main__':
    main()
