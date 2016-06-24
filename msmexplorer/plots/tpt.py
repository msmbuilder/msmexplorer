import networkx as nx
from matplotlib import pyplot as pp
from msmbuilder import tpt


def plot_tpaths(msm, sources, sinks, for_committors=None, num_paths=1,
                pos=None, node_color='c', edge_color='k', ax=None, **kwargs):

    net_flux = tpt.net_fluxes(sources, sinks, msm,
                              for_committors=for_committors)
    paths, _ = tpt.paths(sources, sinks, net_flux, num_paths=num_paths)

    graph = nx.DiGraph()
    for path in paths:
        for u, v in zip(path[:-1], path[1:]):
            graph.add_edge(u, v, weight=net_flux[u, v])

    if not ax:
        ax = pp.gca()

    nx.draw_networkx(graph, pos=pos, node_color=node_color,
                     edge_color=edge_color, ax=ax, **kwargs)

    return ax
