import pandas as pd
import matplotlib.pyplot as pp
import seaborn as sns

from ..utils import msme_colors

__all__ = ['plot_trace']


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

    sns.set_style('whitegrid')

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
