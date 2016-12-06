import numpy as np
from matplotlib.axes import SubplotBase

from ..plots import plot_trace

rs = np.random.RandomState(42)
data = rs.rand(100000)


def test_plot_trace():
    ax, side_ax = plot_trace(data, xlabel='x', ylabel='y')

    assert isinstance(ax, SubplotBase)
    assert isinstance(side_ax, SubplotBase)
