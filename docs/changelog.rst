.. _changelog:

Changelog
=========

v0.3.0 (Development)
--------------------

API Changes
~~~~~~~~~~~

- ``plot_voronoi`` accepts a new parameter ``alpha`` (#55).
- ``plot_voronoi`` will not set axis limits if you specify ``ax`` (#55).


New Features
~~~~~~~~~~~~



Improvements
~~~~~~~~~~~~


v0.2.0 (September 15, 2016)
---------------------------

We're pleased to announce the release of MSMExplorer v0.2.0. The focus of this
release is improving plotting reproducibility and utilities. There is also a
major bugfix for ``plot_chord`` and ``plot_free_energy``. We encourage all
users to update to v0.2.0.

API Changes
~~~~~~~~~~~

- ``darkslategrey`` has been renamed to ``carbon`` (#41).
- ``plot_free_energy`` now supports a ``random_state`` option (#40)

New Features
~~~~~~~~~~~~

- ``example_datasets`` has been added. This allows example datasets to be
  pulled from the ``msmb_data`` package (#41).
- ``make_colormap`` has been added in ``msmexplorer.utils``. It creates a
  linear colormap from a color palette (#40).
- ``msme_colors`` has been added in ``msmexplorer.utils``. It allows any
  non-native plotting functions to handle MSMExplorer color strings (#40).

Improvements
~~~~~~~~~~~~

- Test coverage is greatly improved (#43)
- ``plot_free_energy`` now produces correct 1-D free energy plots (#43).
- ``extract_palette`` is now more robust (#40).
- Improve example reproducibility (#40)
- Fix path vertices problem in ``plot_chord`` (#38).


v0.1.0 (August 30, 2016)
------------------------

This is the first stable version of MSMExplorer

New Features
~~~~~~~~~~~~

- Clustering plots: ``plot_voronoi``
- MSM plots: ``plot_pop_resids``, ``plot_msm_network``, ``plot_timescales``
- Projection plots: ``plot_free_energy``, ``plot_histogram``
- TPT plots: ``plot_tpaths``
- Misc. plots: ``plot_chord``, ``plot_trace``
