import numpy as np
from matplotlib.axes import SubplotBase
from seaborn.apionly import FacetGrid

from ..plots import plot_chord, plot_stackdist
from . import PlotTestCase

rs = np.random.RandomState(42)
data = rs.rand(12, 12)


class TestChordPlot(PlotTestCase):
    """Test the function(s) that visualize a chord plot."""

    def test_plot_chord(self):

        ax = plot_chord(data, threshold=0.2, labels=list(range(12)))

        assert isinstance(ax, SubplotBase)


class TestStackedDistPlot(PlotTestCase):
    """Test the function(s) that visualize a chord plot."""

    def test_plot_chord(self):

        ax = plot_stackdist(data)

        assert isinstance(ax, FacetGrid)
