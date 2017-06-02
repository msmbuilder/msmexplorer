import numpy as np
from matplotlib.axes import SubplotBase

from ..plots import plot_trace
from . import PlotTestCase

rs = np.random.RandomState(42)
data = rs.rand(100000)

class TestTimeSeriesPlot(PlotTestCase):
    """Test the function(s) that visualize time-series."""

    def test_plot_trace(self):
        ax, side_ax = plot_trace(data, xlabel='x', ylabel='y')

        assert isinstance(ax, SubplotBase)
        assert isinstance(side_ax, SubplotBase)
