import numpy as np
from msmbuilder.msm import MarkovStateModel, BayesianMarkovStateModel
from matplotlib.axes import Subplot
from seaborn.apionly import JointGrid

from ..plots import plot_pop_resids, plot_msm_network, plot_timescales

data = np.random.randint(low=0, high=10, size=100000)
msm = MarkovStateModel()
msm.fit(data)
bmsm = BayesianMarkovStateModel()
bmsm.fit(data)


def test_plot_pop_resids():
    ax = plot_pop_resids(msm)

    assert isinstance(ax, JointGrid)


def test_plot_msm_network():
    ax = plot_msm_network(msm)

    assert isinstance(ax, Subplot)


def test_plot_timescales_msm():
    ax = plot_timescales(msm)

    assert isinstance(ax, Subplot)


def test_plot_timescales_bmsm():
    ax = plot_timescales(bmsm)

    assert isinstance(ax, Subplot)
