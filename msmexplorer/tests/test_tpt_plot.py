import numpy as np
from msmbuilder.msm import MarkovStateModel, BayesianMarkovStateModel
from matplotlib.axes import Subplot

from ..plots import plot_tpaths

data = np.random.randint(low=0, high=10, size=100000)
msm = MarkovStateModel()
msm.fit(data)
bmsm = BayesianMarkovStateModel()
bmsm.fit(data)


def test_plot_tpaths_msm():
    ax = plot_tpaths(msm, 0, 9)

    assert isinstance(ax, Subplot)


def test_plot_tpaths_bmsm():
    ax = plot_tpaths(bmsm, 0, 9)

    assert isinstance(ax, Subplot)
