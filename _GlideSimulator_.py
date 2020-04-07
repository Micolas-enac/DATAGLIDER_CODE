import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle
from matplotlib.collections import PatchCollection


# # parameters
# p = np.exp(-1.5)  # the probability of not finding a thermal
# nsample = 300
#
# N = []
# for i in range(0,10000):
#     X = np.random.binomial(1,1-p,size=nsample)
#     n = 1 + np.where(X == 0)[0][0]
#     if n < nsample:
#         N.append(n)
#     else:
#         raise ValueError("n>sampleSize, start again !")
#
# plt.hist(N,bins=np.arange(0.5,10.5,1),align='mid',density=True)
# k = np.arange(1,10,1)
# plt.plot(k , p*(1-p)**(k-1))
#
# print(np.mean(N))
# print(1/p)
# print(np.var(N))
# print(1/p**2-1/p)

# Latin HyperCube sampling of 2D space
# ------------------------------------
N = 100 # number of spot
l = 10 # square side length (km)


def gen_spots():
    """Generate a random field of points in a 2D unit square area.
    The random sampling uses Latin Hypercube Sampling.
    :return:
    """
    xcat = np.linspace(0, l, N + 1)
    xcat = list(zip(xcat[0:-1], xcat[1:]))
    ycat = np.linspace(0, l, N + 1)
    ycat = list(zip(ycat[0:-1], ycat[1:]))

    ncat = N
    x = []
    y = []
    for i in range(0,N):
        ix = np.random.randint(0,ncat) # choose a random cell
        iy = np.random.randint(0,ncat)
        try:
            xran = xcat[ix]
            yran = ycat[iy]
        except IndexError as err:
            print(err)
            print(len(xcat))
            print(ix)
            print(iy)

        x.append(float(np.random.random(1))*(xran[1]-xran[0])+xran[0])
        y.append(float(np.random.random(1))*(yran[1]-yran[0])+yran[0])

        del xcat[ix]
        del ycat[iy]
        ncat -= 1

    return list(zip(x,y))

# Glider simulation
y0 = 5
R = 0.1
R2 = R ** 2
xmax = 2
print("lambda = %0.1f" % (1 / (N/l**2 * 2 * R)))
print("E(X) = %0.1f" % np.exp(xmax * N/l**2 * 2 * R))
def simu(spots):
    """ Run a flight simulation in a given thermal fields in x direction.
    :param spots: the (x,y) position of the thermals
    :return: the list of x in a thermal.
    """
    x0 = 0
    xt = 0
    points = [0]
    while (xt-x0)<xmax:
        for s in spots:
            dist2 = (xt-s[0])**2+(y0-s[1])**2
            if dist2 < R2:
                x0 = xt
                points.append(x0)
            elif xt>l:
                raise ValueError("Out of simulation area")
            else:
                pass
        xt += 1e-1
    points.append(points[-1]+xmax)
    return points

x = []
for k in range(0,100):
    spots = gen_spots()
    points = simu(spots)
    x.append(points[-1])
    print("k=%d, Ex=%0.2f" %(k,np.mean(x)))

fig,ax = plt.subplots()
x,y = zip(*spots)
ax.scatter(x,y)
ax.plot(points,[y0]*len(points),':+k')
ax.set_aspect('equal')
patches = []
for s in spots:
    p = Circle(s,radius=R,fc='k',ec='k')
    patches.append(p)

pc = PatchCollection(patches,alpha=0.5)
ax.add_collection(pc)

plt.show()
