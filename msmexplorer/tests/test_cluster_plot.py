import numpy as np
from matplotlib.axes import SubplotBase
from msmbuilder.cluster import KMeans

from ..plots import plot_voronoi
from . import PlotTestCase

rs = np.random.RandomState(42)
data = rs.rand(10000, 2)


class TestClusterPlot(PlotTestCase):
    """Test the function(s) that visualize clustering."""

    def test_plot_voronoi(self):
        kmeans = KMeans(n_clusters=15)
        kmeans.fit([data])

        ax = plot_voronoi(kmeans, xlabel='x', ylabel='y')

        assert isinstance(ax, SubplotBase)
