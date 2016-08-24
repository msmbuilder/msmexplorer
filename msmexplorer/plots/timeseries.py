import pandas as pd
import matplotlib.pyplot as pp
import seaborn.apionly as sns

from ..utils import extract_palette

__all__ = ['plot_trace']


def plot_trace(data, window=1, ax=None, side_ax=None, color='beryl', alpha=0.8,
               label=None, legend=True, xlabel=None, ylabel=None, labelsize=14,
               rolling_kwargs=None):
    """

    """

    sns.set_style('whitegrid')

    if ax is None:
        f, (ax, side_ax) = pp.subplots(1, 2, sharey=True, figsize=(20, 5),
                                       gridspec_kw={'width_ratios': [6, 1],
                                       'wspace': 0.01})

    if rolling_kwargs is None:
        rolling_kwargs = {}

    color = extract_palette(color)

    df = pd.DataFrame(data, columns=(label,)).rolling(window, **rolling_kwargs).mean()
    df.plot(ax=ax, color=color, alpha=alpha, legend=legend)

    ax.tick_params(top='off', right='off')

    if xlabel:
        ax.set_xlabel(xlabel, size=labelsize)
    if ylabel:
        ax.set_ylabel(ylabel, size=labelsize)

    df.hist(label, bins=30, normed=True, color=color, alpha=0.3,
            orientation='horizontal', ax=side_ax)
    sns.kdeplot(df[label], color=color, ax=side_ax, vertical=True)
    side_ax.tick_params(top='off', right='off')
    side_ax.xaxis.set_ticklabels([])

    return ax, side_ax
