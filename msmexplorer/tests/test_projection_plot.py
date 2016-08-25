import numpy as np
from matplotlib.figure import Figure
from matplotlib.axes import SubplotBase

from ..plots import plot_histogram, plot_free_energy

rs = np.random.RandomState(42)
data = rs.rand(100000, 2)


def test_plot_histogram():
    fig = plot_histogram(data)

    assert isinstance(fig, Figure)


def test_plot_free_energy_1d():
    ax = plot_free_energy(data, n_samples=10000)

    assert isinstance(ax, SubplotBase)


def test_plot_free_energy_2d():
    ax = plot_free_energy(data, obs=(0, 1), n_samples=10000)

    assert isinstance(ax, SubplotBase)
