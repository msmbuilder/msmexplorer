import numpy as np
from scipy.constants import Avogadro, Boltzmann, calorie_th
from matplotlib import pyplot as pp

from corner import corner
from seaborn.distributions import (_scipy_univariate_kde, _scipy_bivariate_kde)

from ..utils import msme_colors

__all__ = ['plot_histogram', 'plot_free_energy', 'plot_decomp_grid']

THERMO_CONSTANT = 10**-3 * Boltzmann * Avogadro / calorie_th


def _thermo_transform(Z, temperature):
    return - THERMO_CONSTANT * temperature * np.log(Z)


plot_histogram = msme_colors(corner)


@msme_colors
def plot_free_energy(data, ax=None, obs=0, temperature=300., n_samples=None,
                     pi=None, bw='scott', gridsize=30, cut=3, clip=None,
                     color='beryl', shade=True, alpha=0.5, cmap='bone',
                     vmin=None, vmax=None, n_levels=10, clabel=False,
                     clabel_kwargs=None, cbar=False, cbar_kwargs=None,
                     xlabel=None, ylabel=None,
                     labelsize=14, random_state=None, return_data=False):
    """
    Plot free energy of observable(s) in kilocalories per mole.

    Parameters
    ----------
    data : ndarray (nsamples, ndim)
        The samples. This should be a 1- or 2-dimensional array. For a 1-D
        array this results in 1-D kernel density plot. For a 2-D array, this
        generates a 2-D contour plot.
    ax : matplotlib axis, optional
        matplotlib figure axis
    obs : int or tuple, optional (default: 0)
        Observables to plot.
    temperature : float, optional (default: 300.0)
        Simulation temperature in degrees Kelvin.
    n_samples : int, optional
        Number of points to subsample from original data.
    pi : array-like, optional
        Equilibrium ensemble weights for each observation.
    bw : {‘scott’ | ‘silverman’ | scalar | pair of scalars }, optional
        Name of reference method to determine kernel size, scalar factor, or
        scalar for each dimension of the bivariate plot.
    gridsize : int, optional
        Number of discrete points in the evaluation grid per dimensional.
    cut : scalar, optional (default: 3)
        Draw the estimate to cut * bw from the extreme data points.
    clip : pair of scalars, or pair of pair of scalars, optional
        Lower and upper bounds for datapoints used to fit KDE. Can provide a
        pair of (low, high) bounds for bivariate plots.
    color : str, optional (default: 'beryl')
        Color of the univariate KDE curve.
    shade : bool, optional
        If True, shade in the area over the KDE curve (or draw with filled
        contours when data is bivariate).
    alpha : float, optional  (default: 0.5)
        Opacity of shaded area.
    cmap : str or matplotlib colormap, optional (default: 'bone')
        Colormap to use in the filled contour plot.
    vmin : float, optional
        The minimum value used in contour plot. If None the minimum value
        of the KDE is used.
    vmax : float, optional
        The maximum value used in contour plot. If None the median value
        of the KDE is used.
    n_levels : int, optional (default: 10)
        Number of contour levels to include.
    clabel : bool, optional (default: False)
        Adds labels to contours in counter plot.
    clabel_kwargs : dict, optional
        Arguments to pass to matplotlib clabel.
    cbar: bool, optional (default: False)
        Adds a colorbar that maps the free energy colors
    cbar_kwargs: dict, optional
        Arguments to pass to matplotlib cbar
    xlabel : str, optional
        x-axis label
    ylabel : str, optional
        y-axis label
    labelsize : int, optional (default: 14)
        x- and y-label font size
    random_state : integer or numpy.RandomState, optional
        The generator used to initialize the centers. If an integer is
        given, it fixes the seed. Defaults to the global numpy random
        number generator
    return_data : Boolean,optional
        Whether or not to return the plotting data

    Returns
    -------
    ax : matplotlib axis
        matplotlib figure axis
    return_data : list of lists, optional
        data that can be used to remake the figures. The last list is always the free energy.
        To remake 1 dim plot:plot(return_data[0],return_data[1]).
        To remake 2 dim plots: contour(return_data[0],return_data[1],return_data[2])
    """

    if ax is None:
        ax = pp.gca()

    if pi is not None and sum(pi) > 1:
        pi /= sum(pi)

    if isinstance(obs, int):
        obs = (obs,)

    if isinstance(random_state, (int, type(None))):
        random_state = np.random.RandomState(random_state)

    prune = data[:, obs]
    if n_samples:
        idx = random_state.choice(range(data.shape[0]), size=n_samples, p=pi)
        prune = prune[idx, :]

    if return_data:
        to_return = []

    if prune.shape[1] == 1:

        if clip is None:
            clip = (-np.inf, np.inf)

        X, Z = _scipy_univariate_kde(prune[:, 0], bw, gridsize, cut, clip)

        Z = _thermo_transform(Z, temperature)

        ax.plot(X, Z - Z.min(), color=color)

        if shade:
            ax.fill_between(X, Z - Z.min(), Z.max() - Z.min(),
                            facecolor=color, alpha=alpha)
        if return_data:
            to_return.append(X)
            to_return.append(Z)

    elif prune.shape[1] == 2:

        if clip is None:
            clip = [(-np.inf, np.inf), (-np.inf, np.inf)]
        elif np.ndim(clip) == 1:
            clip = [clip, clip]

        X, Y, Z = _scipy_bivariate_kde(prune[:, 0], prune[:, 1], bw, gridsize,
                                       cut, clip)

        Z = _thermo_transform(Z, temperature)

        if not vmin:
            vmin = -1E-12
        if not vmax:
            vmax = np.percentile(Z, 50)

        if shade:
            cf = ax.contourf(X, Y, Z - Z.min(), cmap=pp.get_cmap(cmap),
                             levels=np.linspace(vmin, vmax, n_levels),
                             alpha=alpha, zorder=1, vmin=vmin, vmax=vmax)
        cs = ax.contour(X, Y, Z - Z.min(), cmap=pp.get_cmap('bone_r'),
                        levels=np.linspace(vmin, vmax, n_levels), alpha=1,
                        zorder=1, vmin=vmin, vmax=vmax)

        if clabel:
            if not clabel_kwargs:
                clabel_kwargs = {}

            ax.clabel(cs, **clabel_kwargs)

        if cbar:
            if not cbar_kwargs:
                cbar_kwargs = {}
            if shade:
                mappable = cf
            else:
                mappable = cs
            pp.colorbar(mappable, **cbar_kwargs)

        ax.grid(zorder=0)

        if return_data:
            to_return.append(X)
            to_return.append(Y)
            to_return.append(Z)
    else:
        raise ValueError('obs cannot be greater than size 2')

    if xlabel:
        ax.set_xlabel(xlabel, size=labelsize)

    if ylabel:
        ax.set_ylabel(ylabel, size=labelsize)

    if return_data:
        return ax, to_return
    else:
        return ax


def plot_decomp_grid(decomposition, obs=0, n_levels=10, res=50, alpha=1.,
                     cmap='magma', ylim=None, xlim=None, ax=None):
    """
    Plot a filled 2-D contour plot of a dimensionality reduction.

    Parameters
    ----------
    decomposition : msmbuilder.decomposition object
        Decomposition object to visualize.
    obs : int or tuple, optional (default: 0)
        Decomposition dimension to plot.
    n_levels : int, optional (default: 10)
        Number of contour levels to include.
    obs : int or tuple, optional (default: 0)
        Observables to plot.
    alpha : float, optional  (default: 1.)
        Opacity of shaded area.
    cmap : str or matplotlib colormap, optional (default: 'magma')
        Colormap to use in the filled contour plot.
    xlim : tuple, optional
        Horizontal axis limits for plotting. Not needed if `ax` is supplied.
    ylim : tuple, optional
        Vertical axis limits for plotting. Not needed if `ax` is supplied.
    ax : matplotlib axis, optional
        matplotlib figure axis

    Returns
    -------
    ax : matplotlib axis
        matplotlib figure axis
    """
    if ax is None:
        ax = pp.gca()
    else:
        if xlim is None:
            xlim = ax.get_xlim()
        if ylim is None:
            ylim = ax.get_ylim()

    if not xlim and not ylim:
        raise ValueError('Please supply x and y limits.')

    X, Y = np.meshgrid(np.linspace(xlim[0], xlim[1], res),
                       np.linspace(ylim[0], ylim[1], res))
    x = np.ravel(X)
    y = np.ravel(Y)
    xy = np.vstack([x, y]).T

    Z = np.vstack(decomposition.transform([xy]))[:, obs].reshape(res, res)

    levels = np.linspace(Z.min(), Z.max(), n_levels + 1)

    cnt = ax.contourf(X, Y, Z, cmap=cmap, alpha=alpha, levels=levels)

    for c in cnt.collections:
        c.set_edgecolor("face")

    return ax
