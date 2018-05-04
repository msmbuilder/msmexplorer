import numpy as np
from matplotlib.axes import SubplotBase
from seaborn.apionly import FacetGrid

from ..plots import plot_chord, plot_stackdist, plot_trace, plot_trace2d, plot_angle
from . import PlotTestCase

rs = np.random.RandomState(42)
data = rs.rand(12, 12)
ts = rs.rand(100000, 1)
ts2 = rs.rand(100000, 2)


class TestChordPlot(PlotTestCase):
    """Test the function(s) that visualize a chord plot."""

    def test_plot_chord(self):

        ax = plot_chord(data, threshold=0.2, labels=list(range(12)))

        assert isinstance(ax, SubplotBase)


class TestStackedDistPlot(PlotTestCase):
    """Test the function(s) that visualize a chord plot."""

    def test_plot_chord(self):

        ax = plot_stackdist([ts, ts])

        assert isinstance(ax, FacetGrid)


class TestTimeSeriesPlot(PlotTestCase):
    """Test the function(s) that visualize time-series."""

    def test_plot_trace(self):
        ax, side_ax = plot_trace(ts, xlabel='x', ylabel='y')

        assert isinstance(ax, SubplotBase)
        assert isinstance(side_ax, SubplotBase)

    def test_plot_trace2d(self):
        ax1 = plot_trace2d(ts2)
        ax2 = plot_trace2d([ts2, ts2])

        assert isinstance(ax1, SubplotBase)
        assert isinstance(ax2, SubplotBase)

class TestAnglePlot(PlotTestCase):
    """Test the function(s) that visualize angle distributions"""

    def test_plot_angle(self):
        f, (left_ax, right_ax) = plot_angle(ts)
        assert isinstance(left_ax, SubplotBase)
        assert isinstance(right_ax, SubplotBase)