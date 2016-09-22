import numpy as np
import networkx as nx
from matplotlib import pyplot as pp

from msmbuilder import tpt

from ..utils import msme_colors

__all__ = ['plot_tpaths']


@msme_colors
def plot_tpaths(msm, sources, sinks, for_committors=None, num_paths=1,
                pos=None, node_size=300, node_color='pomegranate',
                edge_color='carbon', alpha=.7, with_labels=True, ax=None,
                **kwargs):
    """
    Plot TPT network diagram.

    Parameters
    ----------
    msm : msmbuilder.msm
        MSMBuilder MarkovStateModel
    sources : int or list, optional
        TPT source states
    sinks : int or list, optional
        TPT sink states
    sinks : ndarray, optional
        Pre-computed forward committors
    pos : dict, optional
        Node positions in dict format (e.g. {node_id : [x, y]})
    node_color : str or [r, g, b], optional
        networkx node colors
    node_size : int or list, optional
        networkx node size
    node_color : str, optional
        networkx edge color
    alpha : float, optional  (default: 0.7)
        Opacity of nodes
    ax : matplotlib axis, optional (default: None)
        Axis to plot on, otherwise uses current axis.
    with_labels : boolean, optional
        Whether or not to include node labels (default: True)
    **kwargs : dict, optional
        Extra arguments to pass to networkx.draw_networkx

    Returns
    -------
    ax : Axis
        matplotlib figure axis

    """
    if hasattr(msm, 'all_populations_'):
        pop = msm.all_populations_.mean(0)
    elif hasattr(msm, 'populations_'):
        pop = msm.populations_

    net_flux = tpt.net_fluxes(sources, sinks, msm,
                              for_committors=for_committors)
    paths, _ = tpt.paths(sources, sinks, net_flux, num_paths=num_paths)

    graph = nx.DiGraph()
    for path in paths:
        for u, v in zip(path[:-1], path[1:]):
            graph.add_edge(u, v, weight=net_flux[u, v])

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

    nx.draw_networkx(graph, pos=pos, node_color=node_color, alpha=alpha,
                     node_size=node_size, edge_color=edge_color, ax=ax,
                     with_labels=with_labels, **kwargs)

    return ax
