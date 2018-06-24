import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cbook
from matplotlib import cm
from matplotlib.colors import LightSource
import matplotlib.colors as mcolors
from mpl_toolkits.mplot3d import Axes3D
import csv
from scipy import interpolate
import statistics

DataIn = csv.reader(open('coordinate.csv', 'r'))
x, y, z = [], [], []
for row in DataIn:
    x.append(eval(row[1]))
    y.append(eval(row[2]))
    z.append(eval(row[3]))
print(min(x), max(x))
print(min(y), max(y))
print(min(z), max(z))
x = np.array(x)
y = np.array(y)
z = np.array(z)
#####################################################
n = 100
X = np.linspace(120.5, 122, n)
Y = np.linspace(30.5, 32, n)
X, Y = np.meshgrid(X, Y)
Z = np.zeros([n, n])
step = 1.5/n

tmp = np.zeros([n, n, 2])
for k in range(len(x)):
    i = 0
    while x[k] > 120.5 + step*(i+1):
        i += 1
    j = 0
    while y[k] > 30.5 + step*(j+1):
        j += 1
    tmp[j][i][0] += z[k]
    tmp[j][i][1] += 1
print('done')
for i in range(n):
    for j in range(n):
        if tmp[i][j][1]:
            Z[i][j] = tmp[i][j][0]/tmp[i][j][1]

edge = 8
for i in range(n):
    for j in range(n):
        if 1:
        # if not Z[i][j]:
            start1 = i-edge if i>=edge else 0
            end1 = i+edge if i<100-edge else 99
            start2 = j-edge if j>=edge else 0
            end2 = j+edge if j<100-edge else 99
            node = []
            for a in range(start1, end1+1):
                for b in range(start2, end2+1):
                    if Z[a][b]:
                        node.append(Z[a][b])
            if node:
                Z[i][j] = statistics.mean(node)

plt.contourf(X, Y, Z, 8, alpha=0.75, cmap=plt.cm.hot)
C = plt.contour(X, Y, Z, 8, colors='black', linewidth=.05)
plt.xticks(())
plt.yticks(())
plt.show()
#####################################################
# gammas = [0.8, 0.5, 0.3]
# fig, axes = plt.subplots(nrows=2, ncols=2)
# axes[0, 0].set_title('Linear normalization')
# axes[0, 0].hist2d(x, y, bins=100)
# for ax, gamma in zip(axes.flat[1:], gammas):
#     ax.set_title('Power law $(\gamma=%1.1f)$' % gamma)
#     ax.hist2d(x, y,
#               bins=100, norm=mcolors.PowerNorm(gamma))
# fig.tight_layout()
# plt.show()
#####################################################
# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.plot_trisurf(x, y, z, )
# plt.show()
#####################################################
# ax = plt.subplot(111, projection='3d')
# ax.scatter(x, y, z, cmap='rainbow', alpha=0.4)
#
# ax.set_zlabel('Z')
# ax.set_ylabel('Y')
# ax.set_xlabel('X')
# plt.show()
#####################################################
