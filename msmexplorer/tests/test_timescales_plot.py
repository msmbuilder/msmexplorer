import numpy as np
from msmbuilder.msm import MarkovStateModel, BayesianMarkovStateModel
from matplotlib.axes import Subplot

from ..plots import plot_timescales

data = np.random.randint(low=0, high=10, size=100000)
msm = MarkovStateModel()
msm.fit(data)
bmsm = BayesianMarkovStateModel()
bmsm.fit(data)


def test_plot_timescales_msm():
    ax = plot_timescales(msm)

    assert isinstance(ax, Subplot)


def test_plot_timescales_bmsm():
    ax = plot_timescales(bmsm)

    assert isinstance(ax, Subplot)
