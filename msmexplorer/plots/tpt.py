import networkx as nx
from matplotlib import pyplot as pp

from msmbuilder import tpt

__all__ = ['plot_tpaths']


def plot_tpaths(msm, sources, sinks, for_committors=None, num_paths=1,
                pos=None, node_color='c', edge_color='k', ax=None, **kwargs):
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
    node_size : int, optional
        networkx node size
    node_size : str or [r, g, b], optional
        networkx edge color
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
    net_flux = tpt.net_fluxes(sources, sinks, msm,
                              for_committors=for_committors)
    paths, _ = tpt.paths(sources, sinks, net_flux, num_paths=num_paths)

    graph = nx.DiGraph()
    for path in paths:
        for u, v in zip(path[:-1], path[1:]):
            graph.add_edge(u, v, weight=net_flux[u, v])

    if not ax:
        ax = pp.gca()

    if not pos:
        pos = nx.spring_layout(graph)

    nx.draw_networkx(graph, pos=pos, node_color=node_color,
                     edge_color=edge_color, ax=ax, **kwargs)

    return ax
