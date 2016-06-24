from seaborn.apionly import xkcd_rgb
from .custom import msme_rgb

all_rgb = {}
for d in (msme_rgb, xkcd_rgb):
    all_rgb.update(d)
