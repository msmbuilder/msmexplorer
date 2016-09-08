import numpy as np

from matplotlib import pyplot as pp
from matplotlib.path import Path
from matplotlib.colors import Normalize
import matplotlib.patches as patches

__all__ = ['plot_chord']


def plot_chord(data, ax=None, cmap=None, labels=None, labelsize=12, norm=True,
               threshold=0.0):
    """
    Plot chord diagram from an adjacency matrix.

    Parameters
    ----------

    data : ndarray
        An adjacency matrix
    ax : matplotlib axis, optional (default: None)
        Axis to plot on, otherwise uses current axis.
    cmap : ColorMap, optional (default: None)
        Optional argument to set the desired colormap
    labels : list, optional (default: None)
        A list of str labels
    labelsize : int, optional (default: 12)
        Label font size
    norm : boolean, optional (default: True)
        Optional argument to normalize data into the [0.0, 1.0] range
    threshold : float, optional (default: 0.0)
        Threshold value for an edge  to be plotted

    Returns
    -------
    ax : Axis
        matplotlib figure axis

    """

    linewidth = 2
    data = np.array(data).copy()
    if norm:
        data /= data.max()
    data[data < threshold] = 0.0

    if len(data.shape) != 2:
        raise ValueError('data must be a 2d array.')
    if data.shape[0] != data.shape[1]:
        raise ValueError('data is not an adjacency matrix')

    if not ax:
        ax = pp.gca(projection='polar')
    if cmap is None:
        cmap = pp.cm.coolwarm

    scale = Normalize(vmin=0, vmax=data.shape[0])

    res = 2048

    theta = np.linspace(0, 2*np.pi, res * data.shape[0])
    r = np.linspace(0.6, 1, 4)

    # Create separators
    for i in range(data.shape[0]):
        theta_i = i*360*np.pi/(180 * data.shape[0])
        ax.plot([theta_i, theta_i], [r[1], 1], '-', color='#fcfcfc',
                lw=linewidth)

    # Create outer ring
    r0 = r[1:3]
    r0 = np.repeat(r0[:, np.newaxis], res, axis=1).T
    for i in range(data.shape[0]):
        theta0 = theta[i*res:i*res+res] + 360*np.pi/(data.shape[0] * 180)
        theta0 = np.repeat(theta0[:, np.newaxis], 2, axis=1)
        z = np.ones((res, 2)) * i
        ax.pcolormesh(theta0, r0, z, cmap=cmap, norm=scale)

    # Set labels
    ax.set_ylim([0, .8])
    ax.set_yticklabels([])
    offset = (3 * np.pi / data.shape[0])

    pos = (np.linspace(0, 2*np.pi, data.shape[0] + 1) + offset) % (2*np.pi)

    if labels:
        ax.set_xticks(pos)
        ax.set_xticklabels(labels, size=int(labelsize))
    else:
        ax.set_xticklabels([])

    ax.plot(np.linspace(-np.pi, np.pi, 2048), 2048*[.73], color='black',
            zorder=10, lw=1.5)

    # Plot connections
    codes = [Path.MOVETO,
             Path.CURVE4,
             Path.CURVE4,
             Path.CURVE4,
             ]

    for i in range(data.shape[0]):
        for j in range(data.shape[0]):
            if i != j and data[i, j] > 0.:
                offset_i = .1 * (j - (data.shape[0] - 1)/2) * offset / data.shape[0]
                offset_j = .1 * (i - (data.shape[0] - 1)/2) * offset / data.shape[0]
                verts = [
                    (pos[i] + offset_i, 0.9),  # P0
                    (pos[i] + offset_i, 0.5),  # P1
                    (pos[j] + offset_j, 0.5),  # P2
                    (pos[j] + offset_j, 0.9)  # P3
                    ]

                path = Path(verts, codes)
                patch = patches.PathPatch(path, facecolor='none',
                                          edgecolor=cmap(scale(i)),
                                          lw=10 * data[i, j], alpha=0.7,
                                          capstyle='round', zorder=-1)
                ax.add_patch(patch)
    return ax
