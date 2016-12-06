"""
MSMExplorer Colors
==================
"""
import seaborn as sns
import matplotlib.pyplot as pp

from msmexplorer.palettes import msme_rgb

names, values = zip(*msme_rgb.items())

sns.palplot(values, size=3)
pp.xticks(range(len(names)), names, size=20)
