import numpy as np
import networkx as nx
import seaborn.apionly as sns
from matplotlib import pyplot as pp

__all__ = ['plot_pop_resids', 'plot_msm_network']


def plot_pop_resids(msm, **kwargs):
    if hasattr(msm, 'all_populations_'):
        msm_pop = msm.populations_.mean(0)
    elif hasattr(msm, 'populations_'):
        msm_pop = msm.populations_

    raw_pop = msm.countsmat_.sum(1) / msm.countsmat_.sum()
    ax = sns.jointplot(np.log10(raw_pop), np.log10(msm_pop), kind='resid',
                       **kwargs)
    ax.ax_joint.set_xlabel('Raw Populations', size=20)
    ax.ax_joint.set_ylabel('Residuals', size=20)

    return ax


def plot_msm_network(msm, pos=None, node_color='c', node_size=300,
                     edge_color='k', ax=None, with_labels=True, **kwargs):
    if hasattr(msm, 'all_populations_'):
        tmat = msm.all_transmats_.mean(0)
    elif hasattr(msm, 'populations_'):
        tmat = msm.transmat_

    graph = nx.Graph(tmat)

    if not ax:
        ax = pp.gca()

    nx.draw_networkx(graph, pos=pos, node_color=node_color,
                     edge_color=edge_color, ax=ax, **kwargs)

    return ax
