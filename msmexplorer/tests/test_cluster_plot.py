import numpy as np
from matplotlib.axes import Subplot
from msmbuilder.cluster import KMeans

from ..plots import plot_voronoi

data = np.random.rand(10000, 2)


def test_plot_voronoi():
    kmeans = KMeans(n_clusters=15)
    kmeans.fit([data])

    ax = plot_voronoi(kmeans)

    assert isinstance(ax, Subplot)
