"""
Angle Plot
==============
"""

from msmbuilder.example_datasets import FsPeptide
import numpy as np
import msmexplorer as msme
import mdtraj as md

# Load Fs Peptide Data
trajs = FsPeptide().get().trajectories
# Compute angle between the C carbon of residue 1, 12 and 23
atom_triplet = np.array([[0, 128, 260]])


# Calculate the angle for every trajectory and store it in a list
angle_list = []
for t in trajs:
    angle_t = md.compute_angles(t, angle_indices=atom_triplet)
    angle_list.append(angle_t)

# Join all the elements of the list for easier inspection
angle_all_trajs = np.concatenate(angle_list)

# Convert angle from radians to degrees
angle_deg = np.rad2deg(angle_all_trajs)

# Plot the distribution of this angle
f, (left_ax, right_ax) = msme.plot_angle(angle_deg)

# Save the figure in pdf format
f.savefig('angle-dist.pdf')