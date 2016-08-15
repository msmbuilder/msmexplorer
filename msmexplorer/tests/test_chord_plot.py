import numpy as np
from matplotlib.axes import SubplotBase

from ..plots import plot_chord

data = np.random.rand(12, 12)


def test_plot_chord():

    ax = plot_chord(data, threshold=0.2)

    assert isinstance(ax, SubplotBase)
