MSMExplorer: data visualizations for biomolecular dynamics
==========================================================

[![Build Status](https://travis-ci.org/msmexplorer/msmexplorer.svg?branch=master)] (https://travis-ci.org/msmexplorer/msmexplorer)
[![Coverage Status](https://coveralls.io/repos/github/msmexplorer/msmexplorer/badge.svg?branch=master)](https://coveralls.io/github/msmexplorer/msmexplorer?branch=master)
[![License](https://img.shields.io/badge/license-MIT-red.svg?style=flat)]  (https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/docs-latest-blue.svg?style=flat)] (http://msmbuilder.org/msmexplorer/)

<div class="row">
  <a href="http://msmbuilder.org/msmexplorer/development/examples/plot_chord.html">
      <img src="http://msmbuilder.org/msmexplorer/development/_static/plot_chord_thumb.png" height="135" width="135">
  </a>
  <a href="http://msmbuilder.org/msmexplorer/development/examples/plot_free_energy_2d.html">
      <img src="http://msmbuilder.org/msmexplorer/development/_static/plot_free_energy_2d_thumb.png" height="135" width="135">
  </a>
  <a href="http://msmbuilder.org/msmexplorer/development/examples/plot_histogram.html">
      <img src="http://msmbuilder.org/msmexplorer/development/_static/plot_histogram_thumb.png" height="135" width="135">
  </a>
  <a href="http://msmbuilder.org/msmexplorer/development/examples/plot_timescales.html">
      <img src="http://msmbuilder.org/msmexplorer/development/_static/plot_timescales_thumb.png" height="135" width="135">
  </a>
  <a href="http://msmbuilder.org/msmexplorer/development/examples/plot_trace.html">
      <img src="http://msmbuilder.org/msmexplorer/development/_static/plot_trace_thumb.png" height="135" width="135">
  </a>
  <a href="http://msmbuilder.org/msmexplorer/development/examples/plot_voronoi.html">
      <img src="http://msmbuilder.org/msmexplorer/development/_static/plot_voronoi_thumb.png" height="135" width="135">
  </a>
</div>

MSMExplorer is a Python visualization library for statistical models of
biomolecular dynamics. It provides a high-level interface for drawing
attractive statistical graphics with [MSMBuilder](http://msmbuilder.org).


Documentation
-------------

Online documentation is available [here](http://msmbuilder.org/msmexplorer/). It includes IPython notebooks, detailed API documentation, and other useful info.

There are docs for the development version [here](http://msmbuilder.org/msmexplorer/development). These should more or less correspond with the github master branch, but they're not built automatically and thus may fall out of sync at times.

Examples
--------

The documentation has an [example gallery](http://msmbuilder.org/msmexplorer/development/examples/) with short scripts showing how to use different parts of the package.


Dependencies
------------

- Python 3.4+

### Mandatory

-  [numpy](http://www.numpy.org/)

-  [scipy](http://www.scipy.org/)

-  [matplotlib](matplotlib.sourceforge.net)

-  [networkx](https://networkx.github.io/)

-  [pandas](http://pandas.pydata.org/)

-  [seaborn](https://stanford.edu/~mwaskom/software/seaborn/)

-  [statsmodels](http://statsmodels.sourceforge.net/devel/)

-  [corner](http://corner.readthedocs.io/en/latest/)

-  [mdtraj](https://mdtraj.org/)

-  [msmbuilder](https://msmbuilder.org)


Installation
------------

The preferred installation mechanism for `msmexplorer` is with `conda`:

```bash
$ conda install -c omnia msmexplorer
```

If you don't have conda, or are new to scientific python, we recommend that
you download the [Anaconda scientific python distribution](https://store.continuum.io/cshop/anaconda/).

To install from PyPI, just do:

    pip install msmexplorer

You may instead want to use the development version from Github, by running

    pip install git+git://github.com/msmexplorer/msmexplorer.git#egg=msmexplorer


Development
-----------

https://github.com/msmexplorer/msmexplorer

Please [submit](https://github.com/msmexplorer/msmexplorer/issues/new) any bugs you encounter to the Github issue tracker.

License
-------

Released under a MIT license
