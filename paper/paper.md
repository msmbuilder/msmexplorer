---
title: 'MSMExplorer: Data Visualizations for Biomolecular Dynamics'
tags:
  - Python
  - plotting
  - molecular dynamics
  - markov model
authors:
  - name: Carlos X. Hernández
    orcid: 0000-0002-8146-5904
    affiliation: 1
  - name: Matthew P. Harrigan
    orcid: 0000-0001-9412-0553
    affiliation: 1
  - name: Mohammad M. Sultan
    orcid: 0000-0001-5578-6328
    affiliation: 1
  - name: Vijay S. Pande
    affiliation: 1
affiliations:
  - name: Stanford University
    index: 1
date: 1 March 2017
bibliography: paper.bib
repository: https://github.com/msmexplorer/msmexplorer
archive_doi: https://doi.org/10.5281/zenodo.162942
---


# Summary

*MSMExplorer* is a Python package for visualizing data generated from
biomolecular dynamics. While molecular visualizations have been a large focus
of the molecular dynamics (MD) community [@vmd, @pymol], data visualizations
for the analyses of MD trajectories have been less developed. *MSMExplorer*
seeks to fill this niche by providing publication-quality statistical
plots with an easy-to-use Python API that works seamlessly with commonly used
Python libraries, such as ``numpy`` and ``scikit-learn``
[@numpy, @scikit-learn]. Additionally, plots are generated using already
established plotting libraries, like ``seaborn``, to provide a consistent
aesthetic [@seaborn, @matplotlib, @networkx, @corner].


Plotting functionality in *MSMExplorer* is centered around the statistical
tools available in ``msmbuilder`` [@msmbuilder]. Because of this focus, in
addition to standard time-series plots, users can choose to plot more involved
measures, such as Gibbs free energy and implied timescales estimated from
Markov models.


*MSMExplorer* is actively developed and maintained by researchers at Stanford
University. Source code for *MSMExplorer* is hosted on GitHub and is
continuously archived to Zenodo [@msme_archive]. Full documentation, including
a practical example gallery, can be found at
[http://msmbuilder.org/msmexplorer](http://msmbuilder.org/msmexplorer).


# References
