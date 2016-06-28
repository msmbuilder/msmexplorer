import numpy as np
from matplotlib import pyplot as pp

from ..palettes import msme_rgb

__all__ = ['plot_timescales']


def plot_timescales(msm, n_timescales=None, error=None, sigma=2, colors=None,
                    xlabel=None, ylabel=None, ax=None):

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
        ax = pp.gca()
    if not colors:
        colors = list(msme_rgb.values())

    for i, item in enumerate(zip(timescales, error)):
        t, s = item
        color = colors[i % len(colors)]
        ax.errorbar([0, 1], [t, t], c=color)
        if s:
            for j in range(1, sigma + 1):
                ax.fill_between([0, 1], y1=[t - j * s, t - j * s],
                                y2=[t + j * s, t + j * s],
                                color=color, alpha=0.2 / j)

    ax.xaxis.set_ticks([])
    if xlabel:
        ax.xaxis.set_label_text(xlabel, size=18, labelpad=18)
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
