import numpy as np
from matplotlib.axes import SubplotBase
from seaborn.apionly import FacetGrid

from ..plots import plot_chord, plot_stackdist, plot_trace
from . import PlotTestCase

rs = np.random.RandomState(42)
data = rs.rand(12, 12)
ts = rs.rand(100000, 1)


class TestChordPlot(PlotTestCase):
    """Test the function(s) that visualize a chord plot."""

    def test_plot_chord(self):

        ax = plot_chord(data, threshold=0.2, labels=list(range(12)))

        assert isinstance(ax, SubplotBase)


class TestStackedDistPlot(PlotTestCase):
    """Test the function(s) that visualize a chord plot."""

    def test_plot_chord(self):

        ax = plot_stackdist([ts])

        assert isinstance(ax, FacetGrid)


class TestTimeSeriesPlot(PlotTestCase):
    """Test the function(s) that visualize time-series."""

    def test_plot_trace(self):
        ax, side_ax = plot_trace(ts, xlabel='x', ylabel='y')

        assert isinstance(ax, SubplotBase)
        assert isinstance(side_ax, SubplotBase)
