"""
Voronoi Plot
============
"""
import numpy as np
from sklearn.cluster import KMeans

import msmexplorer as msme

# Create a random dataset across several variables
rs = np.random.RandomState(42)
n, p = 1000, 2
d = rs.normal(0, 2, (n, p))
d += np.log(np.arange(1, p + 1)) * -5 + 10

# Cluster data using KMeans
kmeans = KMeans()
kmeans.fit(d)

# Plot Voronoi Diagram
msme.plot_voronoi(kmeans, color_palette=msme.palettes.msme_rgb)
