import numpy as np
from scipy.constants import Avogadro, Boltzmann, calorie_th
from matplotlib import pyplot as pp

from corner import corner as plot_histogram
import seaborn.apionly as sns
from seaborn.distributions import (_scipy_univariate_kde, _scipy_bivariate_kde)

from msmexplorer.palettes import all_rgb

__all__ = ['plot_histogram', 'plot_free_energy']

THERMO_CONSTANT = 10**-3 * Boltzmann * Avogadro / calorie_th


def _thermo_transform(Z, temperature):
    return - THERMO_CONSTANT * temperature * np.log(Z)


def plot_free_energy(data, ax=None, obs=0, n_samples=None, pi=None,
                     gridsize=30, cut=3, clip=None, cmap='bone', color='beryl',
                     bw='scott', temperature=300., vmin=None, vmax=None,
                     n_levels=10, filled=True, alpha=0.5, clabel=False,
                     clabel_kwargs=None, xlabel=None, ylabel=None):

    sns.set_style('whitegrid')

    if ax is None:
        ax = pp.gca()

    if pi is not None and sum(pi) > 1:
        pi /= sum(pi)

    if isinstance(obs, int):
        obs = (obs,)

    prune = data[:, obs]
    if n_samples:
        idx = np.random.choice(range(data.shape[0]), size=n_samples, p=pi)
        prune = prune[idx, :]

    if prune.shape[1] == 1:

        if clip is None:
            clip = (-np.inf, np.inf)

        X, Z = _scipy_univariate_kde(prune[:, 0], bw, gridsize, cut, clip)

        Z = _thermo_transform(Z, temperature)

        ax.plot(X, Z, color=all_rgb[color])

        ax.fill_between(X, Z, Z.max(), facecolor=all_rgb[color], alpha=alpha)

    elif prune.shape[1] == 2:

        if clip is None:
            clip = [(-np.inf, np.inf), (-np.inf, np.inf)]
        elif np.ndim(clip) == 1:
            clip = [clip, clip]

        X, Y, Z = _scipy_bivariate_kde(prune[:, 0], prune[:, 1], bw, gridsize,
                                       cut, clip)

        Z = _thermo_transform(Z, temperature)

        if not vmin:
            vmin = np.percentile(Z, 0)
        if not vmax:
            vmax = np.percentile(Z, 50)

        if filled:
            ax.contourf(X, Y, Z - Z.min(), cmap=pp.get_cmap(cmap),
                        levels=np.linspace(vmin, vmax, n_levels), alpha=alpha,
                        zorder=1, vmin=vmin, vmax=vmax)
        cs = ax.contour(X, Y, Z - Z.min(), cmap=pp.get_cmap('bone_r'),
                        levels=np.linspace(vmin, vmax, n_levels), alpha=1,
                        zorder=2, vmin=vmin, vmax=vmax)

        if clabel:
            if not clabel_kwargs:
                clabel_kwargs = {}

            ax.clabel(cs, **clabel_kwargs)

        ax.grid(zorder=0)

    else:
        raise ValueError('obs cannot be greater than size 2')

    return ax
