import networkx as nx
from matplotlib import pyplot as pp


def plot_msm_network(msm, pos=None, node_color='c', node_size=300,
                     edge_color='k', ax=None, with_labels=True, **kwargs):
    graph = nx.Graph(msm.transmat_)

    if not ax:
        ax = pp.gca()

    return nx.draw_networkx(graph, pos=pos, node_color=node_color,
                            edge_color=edge_color, ax=ax, **kwargs)
