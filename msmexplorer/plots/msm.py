import numpy as np
import networkx as nx
import seaborn as sns
from matplotlib import pyplot as pp

from ..utils import msme_colors
from ..palettes import msme_rgb

__all__ = ['plot_pop_resids', 'plot_msm_network', 'plot_timescales']


@msme_colors
def plot_pop_resids(msm, **kwargs):
    """
    Plot residuals between MSM populations and raw counts.

    Parameters
    ----------
    msm : msmbuilder.msm
        MSMBuilder MarkovStateModel
    **kwargs : dict, optional
        Extra arguments to pass to seaborn.jointplot

    Returns
    -------
    ax : matplotlib axis
        matplotlib figure axis

    """
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


@msme_colors
def plot_msm_network(msm, pos=None, node_size=None, node_color='pomegranate',
                     edge_color='carbon', alpha=.7, ax=None, with_labels=True,
                     **kwargs):
    """
    Plot MSM network diagram.

    Parameters
    ----------
    msm : msmbuilder.msm
        MSMBuilder MarkovStateModel
    pos : dict, optional
        Node positions in dict format (e.g. {node_id : [x, y]})
    node_color : str or [r, g, b], optional
        networkx node colors
    node_size : int or list, optional
        networkx node size
    node_color : str, optional
        networkx edge color
    ax : matplotlib axis, optional (default: None)
        Axis to plot on, otherwise uses current axis.
    with_labels : boolean, optional
        Whether or not to include node labels (default: True)
    alpha : float, optional  (default: 0.7)
        Opacity of nodes
    **kwargs : dict, optional
        Extra arguments to pass to networkx.draw_networkx

    Returns
    -------
    ax : matplotlib axis
        matplotlib figure axis

    """
    if hasattr(msm, 'all_populations_'):
        tmat = msm.all_transmats_.mean(0)
        pop = msm.all_populations_.mean(0)
    elif hasattr(msm, 'populations_'):
        tmat = msm.transmat_
        pop = msm.populations_

    graph = nx.Graph(tmat)

    if not ax:
        ax = pp.gca()

    if pos is None:
        pos = nx.spring_layout(graph)

    if node_size is None:
        node_size = 5000. * pop

    if isinstance(node_size, (list, np.ndarray)):
        node_size = [node_size[i] for i in graph.nodes()]

    if isinstance(node_color, (list, np.ndarray)):
        node_color = [node_color[i] for i in graph.nodes()]

    nx.draw_networkx(graph, pos=pos, node_color=node_color,
                     node_size=node_size, edge_color=edge_color, ax=ax,
                     with_labels=with_labels, alpha=alpha, **kwargs)

    return ax


@msme_colors
def plot_timescales(msm, n_timescales=None, error=None, sigma=2,
                    color_palette=None, xlabel=None, ylabel=None, ax=None):
    """
    Plot MSM timescales spectral diagram.

    Parameters
    ----------
    msm : msmbuilder.msm
        MSMBuilder MarkovStateModel
    n_timescales : int, optional
        Number of timescales to plot
    error : array-like (float), optional
        associated errors for each timescales
    sigma : float, optional
        significance level for default error bars
    color_palette: list or dict, optional
        Color palette to apply
    xlabel : str, optional
        x-axis label
    ylabel : str, optional
        y-axis label
    ax : matplotlib axis, optional (default: None)
        Axis to plot on, otherwise uses current axis.

    Returns
    -------
    ax : matplotlib axis
        matplotlib figure axis

    """
    if hasattr(msm, 'all_timescales_'):
        timescales = msm.all_timescales_.mean(0)
        if not error:
            error = (msm.all_timescales_.std(0) /
                     msm.all_timescales_.shape[0] ** 0.5)
    elif hasattr(msm, 'timescales_'):
        timescales = msm.timescales_
        if not error:
            error = np.nan_to_num(msm.uncertainty_timescales())

    if n_timescales:
        timescales = timescales[:n_timescales]
        error = error[:n_timescales]
    else:
        n_timescales = timescales.shape[0]

    ymin = 10 ** np.floor(np.log10(np.nanmin(timescales)))
    ymax = 10 ** np.ceil(np.log10(np.nanmax(timescales)))

    if not ax:
        _, ax = pp.subplots(1, 1, figsize=(2, 8))
    if not color_palette:
        color_palette = list(msme_rgb.values())

    for i, item in enumerate(zip(timescales, error)):
        t, s = item
        color = color_palette[i % len(color_palette)]
        ax.errorbar([0, 1], [t, t], c=color)
        if s:
            for j in range(1, sigma + 1):
                ax.fill_between([0, 1], y1=[t - j * s, t - j * s],
                                y2=[t + j * s, t + j * s],
                                color=color, alpha=0.2 / j)

    ax.xaxis.set_ticks([])
    if xlabel:
        ax.xaxis.set_label_text(xlabel, size=18)
        ax.xaxis.labelpad = 18
    if ylabel:
        ax.yaxis.set_label_text(ylabel, size=18)
    ax.set_yscale('log')
    ax.set_ylim([ymin, ymax])

    autoAxis = ax.axis()
    rec = pp.Rectangle((autoAxis[0], 100),
                       (autoAxis[1] - autoAxis[0]),
                       ymax, fill=False, lw=2)
    rec = ax.add_patch(rec)

    for tick in ax.yaxis.get_major_ticks():
        tick.label.set_fontsize(16)

    return ax
