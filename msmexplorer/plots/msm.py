import numpy as np
import networkx as nx
import seaborn.apionly as sns
from matplotlib import pyplot as pp


def plot_pop_resids(msm, **kwargs):
    msm_pop = msm.populations_
    raw_pop = msm.countsmat_.sum(1) / msm.countsmat_.sum()
    ax = sns.jointplot(np.log10(raw_pop), np.log10(msm_pop), kind='resid',
                       **kwargs)
    ax.ax_joint.set_xlabel('Raw Populations', size=20)
    ax.ax_joint.set_ylabel('Residuals', size=20)

    return ax


def plot_msm_network(msm, pos=None, node_color='c', node_size=300,
                     edge_color='k', ax=None, with_labels=True, **kwargs):
    graph = nx.Graph(msm.transmat_)

    if not ax:
        ax = pp.gca()

    return nx.draw_networkx(graph, pos=pos, node_color=node_color,
                            edge_color=edge_color, ax=ax, **kwargs)
