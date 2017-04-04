.. _changelog:

Changelog
=========


v1.0.0 (March 30, 2017)
-----------------------

New Features
~~~~~~~~~~~~
- ``plot_free_energy`` now accepts a ``return_data`` flag that will return 
  the data used for the free energy plot(#78).
- ``plot_free_energy`` now accepts two extra arguments, ``cbar`` and
  ``cbar_kwargs`` to add a colorbar and control its aesthetics (#73).


Improvements
~~~~~~~~~~~~
- The ``shade`` option now works for ``plot_free_energy`` in the 1D case (#76).
- Fixed an issue where adding cluster centers would break the visualization
if ``ndim`` > 2 (#70).

v0.3.0 (October 24, 2016)
-------------------------

API Changes
~~~~~~~~~~~

- ``side_ax`` in ``plot_trace`` is now optional if ``ax`` is provided (#54)
- ``legend`` in ``plot_trace`` now defaults to True if ``label`` is provided,
  otherwise false. It previously always defaulted to True (#54).
- ``plot_voronoi`` accepts a new parameter ``alpha`` (#55).
- ``plot_voronoi`` will not set axis limits if you specify ``ax`` (#55).


Improvements
~~~~~~~~~~~~

- ``plot_msm_network`` and ``plot_tpaths`` can now handle lists as
  ``node_color`` and ``node_size`` (#61).
- ``extract_palette`` can now handle rgb tuples and lists (#61).


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
