import numpy as np
import pandas as pd

from matplotlib import pyplot as pp
from matplotlib.path import Path
from matplotlib.colors import Normalize
import matplotlib.patches as patches

import seaborn.apionly as sns

from ..utils import msme_colors
from .. import palettes

__all__ = ['plot_chord', 'plot_stackdist', 'plot_trace']


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

    theta = np.linspace(0, 2 * np.pi, res * data.shape[0])
    r = np.linspace(0.6, 1, 4)

    # Create separators
    for i in range(data.shape[0]):
        theta_i = i * 360 * np.pi / (180 * data.shape[0])
        ax.plot([theta_i, theta_i], [r[1], 1], '-', color='#fcfcfc',
                lw=linewidth)

    # Create outer ring
    r0 = r[1:3]
    r0 = np.repeat(r0[:, np.newaxis], res, axis=1).T
    for i in range(data.shape[0]):
        theta0 = theta[i * res:i * res + res] + \
            360 * np.pi / (data.shape[0] * 180)
        theta0 = np.repeat(theta0[:, np.newaxis], 2, axis=1)
        z = np.ones((res, 2)) * i
        ax.pcolormesh(theta0, r0, z, cmap=cmap, norm=scale)

    # Set labels
    ax.set_ylim([0, .8])
    ax.set_yticklabels([])
    offset = (3 * np.pi / data.shape[0])

    pos = (np.linspace(0, 2 * np.pi, data.shape[0] + 1) + offset) % (2 * np.pi)

    if labels:
        ax.set_xticks(pos)
        ax.set_xticklabels(labels, size=int(labelsize))
    else:
        ax.set_xticklabels([])

    ax.plot(np.linspace(-np.pi, np.pi, 2048), 2048 * [.73], color='black',
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
                offset_i = .1 * (j - (data.shape[0] - 1) / 2)
                offset_i *= offset / data.shape[0]
                offset_j = .1 * (i - (data.shape[0] - 1) / 2)
                offset_j *= offset / data.shape[0]
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


def plot_stackdist(data, size=.5, aspect=12, x_labels=None,
                   y_labels=None, palette=None, g=None):
    """
    Plot stacked distributions (a.k.a Joy plot) of data.

    Parameters
    ----------

    data : list of ndarrays
        A list of 2D numpy arrays with dimensions (n_observations, n_features)
    size : scalar, optional (default: .5)
        Height (in inches) of each facet. See also: ``aspect``.
    aspect : scalar, optional (default: 12)
        Aspect ratio of each facet, so that ``aspect * size`` gives the width
        of each facet in inches.
    x_labels : list, optional (default: None)
        A list of str labels for feature-axis
    y_labels : list, optional (default: None)
        A list of str labels for y-axis
    palette : list of colors, optional (default: None)
        List of colors for plots. If ``None``, the default MSMExplorer colors
        are used.
    g : Seaborn.FacetGrid, optional (default: None)
        Pre-initialized FacetGrid to use for plotting.

    Returns
    -------
    g : Seaborn.FacetGrid
        Seaborn FacetGrid of the stacked distributions.

    """

    n_feat = data[0].shape[1]
    x = np.concatenate([d.ravel() for d in data], axis=0)
    f = np.concatenate([(np.ones_like(d) * np.arange(d.shape[1])).ravel()
                        for d in data], axis=0)
    g = np.concatenate([i * np.ones_like(d.ravel()).astype(int)
                        for i, d in enumerate(data)], axis=0)
    df = pd.DataFrame(dict(x=x, f=f, g=g))

    if not palette:
        palette = list(palettes.msme_rgb.values())[::-1]

    # Initialize the FacetGrid object
    g = sns.FacetGrid(df, row="g", col="f", hue="f",
                      aspect=aspect, size=size, palette=palette)

    # Draw the densities in a few steps
    global row_count, col_count
    col_count = 0
    row_count = 0

    def kdeplot(x, color='w', **kwargs):
        global row_count, col_count

        if color != 'w':
            color = sns.light_palette(
                color, n_colors=len(data) + 1)[row_count + 1]
        sns.kdeplot(x, color=color, **kwargs)

        col_count = (col_count + 1) % n_feat

        if col_count == 0:
            row_count = (row_count + 1) % len(data)

    g.map(kdeplot, "x", clip_on=False, shade=True, alpha=1., bw=.2)
    g.map(kdeplot, "x", clip_on=False, color='w', lw=2, bw=.2)

    # Add y labels
    g.set_titles("")
    g.set_xlabels("")
    for i, ax in enumerate(g.axes):
        if y_labels is not None:
            ax[0].text(0, .2, y_labels[i], fontweight="bold", color='k',
                       ha="left", va="center", transform=ax[0].transAxes)
        for j, a in enumerate(ax):
            a.set_facecolor((0, 0, 0, 0))
            if i == 0 and x_labels is not None:
                a.set_title(x_labels[j])

    # Set the subplots to overlap
    g.fig.subplots_adjust(hspace=-.25, wspace=0.1)

    # Remove axes details that don't play will with overlap
    g.set(yticks=[])
    g.set(xticks=[])
    g.despine(bottom=False, left=True)
    return g


@msme_colors
def plot_trace(data, label=None, window=1, ax=None, side_ax=None,
               color='beryl', alpha=0.8, legend=None, xlabel=None, ylabel=None,
               labelsize=14, rolling_kwargs=None):
    """
    Plot trace of time-series data.

    Parameters
    ----------
    data : array-like (nsamples, )
        The samples. This should be a 1-D time-series array.
    label : str, optional
        Label for time-series.
    window : int, optional (default: 1)
        Size of the moving window. This is the number of observations used for
        calculating the average.
    ax : matplotlib axis, optional
        main matplotlib figure axis for trace.
    side_ax : matplotlib axis, optional
        side matplotlib figure axis for histogram. If you provide
        ax but not side_ax, we won't plot the histogram. If provide
        neither ax nor side_ax, we will set up the axes for you.
        If you supply side_ax but not ax, an error will be raised.
    color : str, optional (default: 'beryl')
        Style color of the trace.
    alpha : float, optional  (default: 0.5)
        Opacity of shaded area.
    legend : bool, optional
        Whether to display legend in plot. Defaults to
        True if legend is provided, otherwise defaults to False.
    xlabel : str, optional
        x-axis label
    ylabel : str, optional
        y-axis label
    labelsize : int, optional (default: 14)
        Font side for axes labels.
    rolling_kwargs : dict, optional
        Keyword arguments for ``pandas.DataFrame.rolling``.

    Returns
    -------
    ax : matplotlib axis
        main matplotlib figure axis for trace.
    side_ax : matplotlib axis
        side matplotlib figure axis for histogram.

    """

    if ax is None:
        if side_ax is not None:
            raise ValueError("If you're supplying ax, you must also "
                             "supply side_ax.")
        f, (ax, side_ax) = pp.subplots(1, 2, sharey=True, figsize=(20, 5),
                                       gridspec_kw={'width_ratios': [6, 1],
                                                    'wspace': 0.01})

    if rolling_kwargs is None:
        rolling_kwargs = {}

    if legend is None:
        legend = (label is not None)

    df = (pd.DataFrame(data, columns=(label,))
          .rolling(window, **rolling_kwargs)
          .mean())
    df.plot(ax=ax, color=color, alpha=alpha, legend=legend)

    ax.tick_params(top='off', right='off')

    if xlabel:
        ax.set_xlabel(xlabel, size=labelsize)
    if ylabel:
        ax.set_ylabel(ylabel, size=labelsize)

    if side_ax is not None:
        df.hist(bins=30, normed=True, color=color, alpha=0.3,
                orientation='horizontal', ax=side_ax)
        sns.kdeplot(df[label], color=color, ax=side_ax, vertical=True)
        side_ax.tick_params(top='off', right='off')
        side_ax.xaxis.set_ticklabels([])
        side_ax.legend([])
        side_ax.set_title('')

    return ax, side_ax
