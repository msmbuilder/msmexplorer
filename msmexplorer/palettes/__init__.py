from seaborn.apionly import xkcd_rgb
from matplotlib.colors import cnames as mpl_colors

from .custom import msme_rgb

all_colors = {}
for d in (msme_rgb, xkcd_rgb, mpl_colors):
    all_colors.update(d)
