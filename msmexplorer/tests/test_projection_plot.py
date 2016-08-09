import numpy as np
from matplotlib.figure import Figure

from ..plots import plot_histogram

rs = np.random.RandomState(42)
data = rs.rand(10000, 2)


def test_plot_histogram():
    fig = plot_histogram(data)

    assert isinstance(fig, Figure)
