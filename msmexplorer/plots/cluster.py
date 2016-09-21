import numpy as np
from matplotlib import pyplot as pp
from scipy.spatial import Voronoi

from ..utils import msme_colors
from ..palettes import msme_rgb

__all__ = ['plot_voronoi']


@msme_colors
def plot_voronoi(kmeans, ax=None, obs=(0, 1), cluster_centers=True,
                 radius=None, color_palette=None, xlabel=None, ylabel=None,
                 labelsize=14, alpha=0.4):
    """
    Plot voronoi regions in a 2D diagram.

    Parameters
    ----------
    kmeans : msmbuilder.cluster
        MSMBuilder cluster object
    ax : matplotlib axis, optional (default: None)
        Axis to plot on, otherwise uses current axis.
    obs : tuple, optional (default: (0, 1))
        Observables to plot.
    cluster_centers : bool, optional (default: True)
        Whether to plot cluster centers.
    radius : float, optional
        Distance to 'points at infinity'.
    color_palette: list or dict, optional
        Color palette to apply
    xlabel : str, optional
        x-axis label
    ylabel : str, optional
        y-axis label
    labelsize : int, optional (default: 14)
        x- and y-label font size
    alpha : float, optional (default: 0.4)
        The alpha value of the fill

    Returns
    -------
    ax : matplotlib axis
        matplotlib figure axis

    """
    # Adapted from http://stackoverflow.com/questions/20515554/colorize-voronoi-diagram

    if not ax:
        ax = pp.gca()
        we_made_ax = True
    else:
        we_made_ax = False

    if not color_palette:
        color_palette = list(msme_rgb.values())

    if len(obs) != 2:
        assert ValueError('obs must be a tuple')

    vor = Voronoi(kmeans.cluster_centers_[:, obs])

    new_regions = []
    new_vertices = vor.vertices.tolist()

    center = vor.points.mean(axis=0)
    if radius is None:
        radius = vor.points.ptp().max() * 2

    # Construct a map containing all ridges for a given point
    all_ridges = {}
    for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
        all_ridges.setdefault(p1, []).append((p2, v1, v2))
        all_ridges.setdefault(p2, []).append((p1, v1, v2))

    # Reconstruct infinite regions
    for p1, region in enumerate(vor.point_region):
        vertices = vor.regions[region]

        if all([v >= 0 for v in vertices]):
            # finite region
            new_regions.append(vertices)
            continue

        # reconstruct a non-finite region
        ridges = all_ridges[p1]
        new_region = [v for v in vertices if v >= 0]

        for p2, v1, v2 in ridges:
            if v2 < 0:
                v1, v2 = v2, v1
            if v1 >= 0:
                # finite ridge: already in the region
                continue

            # Compute the missing endpoint of an infinite ridge

            t = vor.points[p2] - vor.points[p1]  # tangent
            t /= np.linalg.norm(t)
            n = np.array([-t[1], t[0]])  # normal

            midpoint = vor.points[[p1, p2]].mean(axis=0)
            direction = np.sign(np.dot(midpoint - center, n)) * n
            far_point = vor.vertices[v2] + direction * radius

            new_region.append(len(new_vertices))
            new_vertices.append(far_point.tolist())

        # sort region counterclockwise
        vs = np.asarray([new_vertices[v] for v in new_region])
        c = vs.mean(axis=0)
        angles = np.arctan2(vs[:, 1] - c[1], vs[:, 0] - c[0])
        new_region = np.array(new_region)[np.argsort(angles)]

        # finish
        new_regions.append(new_region.tolist())

    vertices = np.asarray(new_vertices)

    for i, region in enumerate(new_regions):
        color = color_palette[i % len(color_palette)]
        polygon = vertices[region]
        ax.fill(*zip(*polygon), color=color, alpha=alpha)

    if cluster_centers:
        ax.scatter(*kmeans.cluster_centers_.T, c='k')

    if xlabel:
        ax.set_xlabel(xlabel, size=labelsize)

    if ylabel:
        ax.set_ylabel(ylabel, size=labelsize)

    if we_made_ax:
        ax.axis('equal')
        ax.set_xlim((vor.min_bound[0] - 0.1, vor.max_bound[0] + 0.1))
        ax.set_ylim((vor.min_bound[1] - 0.1, vor.max_bound[1] + 0.1))

    return ax
