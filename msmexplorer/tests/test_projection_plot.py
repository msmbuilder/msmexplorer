import numpy as np
from matplotlib.figure import Figure
from matplotlib.axes import SubplotBase

from ..plots import plot_histogram, plot_free_energy
from . import PlotTestCase

n = 100000
rs = np.random.RandomState(42)
data = rs.rand(n, 2)

class TestProjectionPlot(PlotTestCase):
    """Test the function(s) that visualize projections."""

    def test_plot_histogram(self):
        fig = plot_histogram(data)

        assert isinstance(fig, Figure)

    def test_plot_free_energy_1d(self):
        ax = plot_free_energy(data, n_samples=10000, pi=np.array(n*[.5]),
                              xlabel='x', ylabel='y')

        assert isinstance(ax, SubplotBase)

    def test_plot_free_energy_2d(self):
        ax = plot_free_energy(data, obs=(0, 1), n_samples=10000,
                              pi=np.array(n*[.5]), xlabel='x', ylabel='y',
                              clabel=True)

        assert isinstance(ax, SubplotBase)
