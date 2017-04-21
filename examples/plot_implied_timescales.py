"""
Implied Timescales Plot
===============
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
featurizer = DihedralFeaturizer(types=['phi', 'psi'])
diheds = featurizer.fit_transform(trajs)

# Perform Dimensionality Reduction
tica_model = tICA(lag_time=2, n_components=2)
tica_trajs = tica_model.fit_transform(diheds)

# Perform Clustering
clusterer = MiniBatchKMeans(n_clusters=100, random_state=rs)
clustered_trajs = clusterer.fit_transform(tica_trajs)

lag_times = [1, 10, 50, 100, 200, 250, 500]
msm_objs = []
for lag in lag_times:
    # Construct MSM
    msm = MarkovStateModel(lag_time=lag, n_timescales=5)
    msm.fit(clustered_trajs)
    msm_objs.append(msm)

# Plot Timescales
colors = ['pomegranate', 'beryl', 'tarragon', 'rawdenim', 'carbon']
msme.plot_implied_timescales(msm_objs, color_palette=colors,
                             xlabel='Lag time (frames)',
                             ylabel='Implied Timescales ($ns$)')
