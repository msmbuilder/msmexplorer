"""
Chord Diagram
=============
"""
import numpy as np

import msmexplorer as msme


# Create a random square matrix
rs = np.random.RandomState(42)
n, p = 12, 12
d = rs.normal(0, 2, (n, p))
d += np.log(np.arange(1, p + 1)) * -5 + 10

# Plot Chord Diagram
msme.plot_chord(d, threshold=.2)
