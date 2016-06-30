import numpy as np
from matplotlib.figure import Figure

from ..plots import plot_histogram

data = np.random.rand(10000, 2)


def test_plot_histogram():
    fig = plot_histogram(data)

    assert isinstance(fig, Figure)
