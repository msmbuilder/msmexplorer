import numpy as np
import pandas as pd

from matplotlib import pyplot as pp
from matplotlib.path import Path
from matplotlib.colors import Normalize
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches

import seaborn.apionly as sns

from ..utils import msme_colors, wrap_angle, constrain_angle
from .. import palettes

__all__ = ['plot_chord', 'plot_stackdist', 'plot_trace', 'plot_trace2d', 'plot_angle']


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


@msme_colors
def plot_trace2d(data, obs=(0, 1), ts=1.0, cbar=True, ax=None, xlabel=None,
                 ylabel=None, labelsize=14,
                 cbar_kwargs=None, scatter_kwargs=None, plot_kwargs=None):
    """
    Plot a 2D trace of time-series data.

    Parameters
    ----------
    data : array-like (nsamples, 2) or list thereof
        The samples. This should be a single 2-D time-series array or a list of 2-D
        time-series arrays.
        If it is a single 2D np.array, the elements will be scatter plotted and
        color mapped to their values.
        If it is a list of 2D np.arrays, each will be plotted with a single color on
        the same axis.
    obs: tuple, optional (default: (0,1))
        Observables to plot.
    ts: float, optional (default: 1.0)
        Step in units of time between each data point in data
    cbar: bool, optional (default: True)
        Adds a colorbar that maps the evolution of points in data
    ax : matplotlib axis, optional
        main matplotlib figure axis for trace.
    xlabel : str, optional
        x-axis label
    ylabel : str, optional
        y-axis label
    labelsize : int, optional (default: 14)
        Font side for axes labels.
    cbar_kwargs: dict, optional
        Arguments to pass to matplotlib cbar
    scatter_kwargs: dict, optional
        Arguments to pass to matplotlib scatter
    plot_kwargs: dict, optional
        Arguments to pass to matplotlib plot
    Returns
    -------
    ax : matplotlib axis
        main matplotlib figure axis for 2D trace.
    """

    if ax is None:
        ax = pp.gca()
    if scatter_kwargs is None:
        scatter_kwargs = {}
    if plot_kwargs is None:
        plot_kwargs = {}

    if not isinstance(obs, tuple):
        raise ValueError('obs must be a tuple')

    if isinstance(data, list):
        # Plot each item in the list with a single color and join with lines
        for item in data:
            prune = item[:, obs]
            ax.plot(prune[:, 0], prune[:, 1], **plot_kwargs)
    else:
        # A single array of data is passed, so we scatter plot
        prune = data[:, obs]
        c = ax.scatter(prune[:, 0], prune[:, 1],
                       c=np.linspace(0, data.shape[0] * ts, data.shape[0]),
                       **scatter_kwargs)
        if cbar:
            # Map the time evolution between the data points to a colorbar
            if cbar_kwargs is None:
                cbar_kwargs = {}
            pp.colorbar(c, **cbar_kwargs)

    if xlabel:
        ax.set_xlabel(xlabel, size=labelsize)
    if ylabel:
        ax.set_ylabel(ylabel, size=labelsize)

    return ax


@msme_colors
def plot_angle(data, N=50, title=None, ax1=None, ax2=None, color=None, wrap=True):
    """
    Plot the distrubution of an angle in polar coordinates and a standard histogram / KDE plot.

    Parameters
    ----------
    data: array-like (nsamples,)
    N: int, optional (default: 50)
        Number of bins to use for histogramming the data
    title: str, optional (default: None)
        The title of the plot
    ax1: matplotlib axis, optional
        The left hand side polar plot
    ax2: matplotlib axis, optional
        The right hand side density plot
    color: str, optional (default: None)
        A color string to use
    wrap: bool, optional (default: True)
        True: Wrap the angle between -180 and 180
        False: Constrain the angle between 0 and 360

    Returns
    -------
    f: matplotlib.figure
        The figure with both axis
    ax1: matplotlib axis, optional
        The left hand side polar plot
    ax2: matplotlib axis, optional
        The right hand side density plot
    """

    if ax1 is None or ax2 is None:
        gs = gridspec.GridSpec(2, 6)
        ax1 = pp.subplot(gs[:1, :2], polar=True)
        ax2 = pp.subplot(gs[:1, 2:])

    if wrap:
        vf = np.vectorize(wrap_angle)
    else:
        vf = np.vectorize(constrain_angle)
    x = vf(data)

    sns.distplot(x, bins=N, ax=ax2, color=color, kde=True)
    radii, theta = np.histogram(x, bins=N, normed=True)
    ax1.set_yticklabels([])

    if wrap:
        ax1ticks = [0, 45, 90, 135, 180, -135, -90, -45]
        ax2ticks = list(range(-180, 180 + 45, 45))
        ax1.set_xticklabels(['{}°'.format(x) for x in ax1ticks])
        ax2.set_xlim(-180, 180)
        ax2.set_xticks(ax2ticks)
        ax2.set_xticklabels(['{}°'.format(x) for x in ax2ticks])

    else:
        ax2ticks = list(range(0, 360 + 45, 45))
        ax2.set_xlim(0, 360)
        ax2.set_xticks(ax2ticks)
        ax2.set_xticklabels(['{}°'.format(x) for x in ax2ticks])

    ax2.set_yticks([])
    ax2.set(xlabel='Angle', ylabel='Density')

    sns.despine(ax=ax2)
    width = (2 * np.pi) / N

    ax1.bar(np.deg2rad(theta[1:]), radii, width=width, color=color, alpha=.5)

    if title is not None:
        pp.suptitle(title)

    pp.tight_layout()

    f = pp.gcf()
    return f, (ax1, ax2)

