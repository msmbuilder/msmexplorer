import numpy as np
from matplotlib.axes import SubplotBase
from msmbuilder.cluster import KMeans

from ..plots import plot_voronoi

rs = np.random.RandomState(42)
data = rs.rand(10000, 2)


def test_plot_voronoi():
    kmeans = KMeans(n_clusters=15)
    kmeans.fit([data])

    ax = plot_voronoi(kmeans, xlabel='x', ylabel='y')

    assert isinstance(ax, SubplotBase)
