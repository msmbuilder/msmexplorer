"""
Stacked Distribution Plot
=========================
"""
from msmbuilder.example_datasets import FsPeptide
from msmbuilder.featurizer import DihedralFeaturizer
from msmbuilder.decomposition import tICA
from msmbuilder.cluster import MiniBatchKMeans
from msmbuilder.msm import MarkovStateModel

import numpy as np

import msmexplorer as msme

rs = np.random.RandomState(42)

# Load Fs Peptide Data
trajs = FsPeptide().get().trajectories

# Extract Backbone Dihedrals
featurizer = DihedralFeaturizer(types=['chi1'])
diheds = featurizer.fit_transform(trajs)

# Perform Dimensionality Reduction
tica_model = tICA(lag_time=2, n_components=2)
tica_trajs = tica_model.fit_transform(diheds)

# Perform Clustering
clusterer = MiniBatchKMeans(n_clusters=12, random_state=rs)
clustered_trajs = clusterer.fit_transform(tica_trajs)

# Construct MSM
msm = MarkovStateModel(lag_time=2)
assignments = msm.fit_transform(clustered_trajs)

# Plot Stacked Distributions
a = np.concatenate(assignments, axis=0)
d = np.concatenate(diheds, axis=0)

# Plot Stacked Distributions of the sine of each Chi1 angle
# within an arbitrary set of states {2, 5, 0}
path_data = [d[a == i][:, ::2] for i in [2, 5, 0]]
msme.plot_stackdist(path_data)
