"""
MSM Network Plot
================
"""
from msmbuilder.featurizer import DihedralFeaturizer
from msmbuilder.decomposition import tICA
from msmbuilder.cluster import MiniBatchKMeans
from msmbuilder.msm import MarkovStateModel

import numpy as np

import msmexplorer as msme
from msmexplorer.example_datasets import FsPeptide

rs = np.random.RandomState(42)

# Load Fs Peptide Data
trajs = FsPeptide().get().trajectories

# Extract Backbone Dihedrals
featurizer = DihedralFeaturizer(types=['phi', 'psi'])
diheds = featurizer.fit_transform(trajs)

# Perform Dimensionality Reduction
tica_model = tICA(lag_time=2, n_components=2)
tica_trajs = tica_model.fit_transform(diheds)

# Perform Clustering
clusterer = MiniBatchKMeans(n_clusters=12, random_state=rs)
clustered_trajs = clusterer.fit_transform(tica_trajs)

# Construct MSM
msm = MarkovStateModel(lag_time=2)
msm.fit(clustered_trajs)

# Plot MSM Network
pos = dict(zip(range(clusterer.n_clusters), clusterer.cluster_centers_))
msme.plot_msm_network(msm, pos=pos, node_color='pomegranate',
                      edge_color='carbon')
