from seaborn.apionly import xkcd_rgb
from matplotlib import colors
from matplotlib.colors import cnames as mpl_colors

from .custom import msme_rgb

__all__ = ['all_colors', 'msme_rgb', 'xkcd_rgb']

all_colors = {}
for d in (msme_rgb, xkcd_rgb, mpl_colors):
    all_colors.update(d)

# Add the single letter colors.
for name, rgb in colors.ColorConverter.colors.items():
    hex_ = colors.rgb2hex(rgb)
    all_colors.update(((name, hex_), ))
