import topopy
from topopy.tests.test_functions import *
import matplotlib.pyplot as plt
import samplers
from matplotlib import patches, collections
import numpy as np

test_function = gerber_different_heights
samples = 50
seed = 0

def validation_grid(resolution=20, min_x = 0, max_x = 1):
    x, y = np.mgrid[min_x:max_x:(resolution * 1j), min_x:max_x:(resolution * 1j)]
    X = np.vstack([x.ravel(), y.ravel()]).T
    return x, y, X

def surface_plot(f, ax, resolution=50, samples=None, edges=None, title=None, cmap=plt.cm.cividis):
    min_x = 0
    max_x = 1
    x, y, X = validation_grid(resolution)
    Z = f(X)
    z = Z.reshape(x.shape)
    ax.contourf(x,y,z, cmap=cmap)
    if samples is not None:
        ax.scatter(samples[:, 0], samples[:, 1], s=80, linewidth=2, edgecolors="#FFFFFF", facecolors='none', zorder=2)
    if edges is not None:
        lines = []
        for edge in edges:
            lines.append([(samples[edge[0], 0], samples[edge[0], 1]),
                          (samples[edge[1], 0], samples[edge[1], 1])])
        lc = mc.LineCollection(lines, colors="#FFFFFF",
                               linewidths=1, linestyles='--', zorder=1)
        ax.add_collection(lc)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.set_title(title, fontsize=18)

def f(X):
    X = np.atleast_2d(X)
    Z = np.empty(X.shape[0])
    for i, xi in enumerate(X):
        Z[i] = test_function(xi)
    return Z

X = samplers.CVTSampler.generate_samples(samples, 2, seed)
Y = test_function(X)
Y = (Y - np.min(Y)) / (np.max(Y) - np.min(Y))
msc = topopy.MorseComplex()
msc.build(X, Y)
partitions = msc.get_partitions(0.05)
print(partitions)