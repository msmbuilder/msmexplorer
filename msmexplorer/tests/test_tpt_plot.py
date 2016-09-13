from nose.plugins.skip import SkipTest
import numpy as np
from msmbuilder.msm import MarkovStateModel, BayesianMarkovStateModel
from matplotlib.axes import SubplotBase

from ..plots import plot_tpaths

rs = np.random.RandomState(42)
data = rs.randint(low=0, high=10, size=100000)

msm = MarkovStateModel()
msm.fit(data)
bmsm = BayesianMarkovStateModel()
bmsm.fit(data)


def test_plot_tpaths_msm():
    ax = plot_tpaths(msm, 0, 9)

    assert isinstance(ax, SubplotBase)


@SkipTest
def test_plot_tpaths_bmsm():
    ax = plot_tpaths(bmsm, 0, 9)

    assert isinstance(ax, SubplotBase)
