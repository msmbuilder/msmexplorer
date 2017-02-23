.. _installing:

Installing and getting started
------------------------------

To install the released version of msmexplorer, you can use ``pip``:

.. code:: bash

  $ pip install msmexplorer

It's also possible to install the released version using
``conda``:

.. code:: bash

  $ conda install msmexplorer

Alternatively, you can use ``pip`` to install the development version, with the
command:

.. code:: bash

  $ pip install git+git://github.com/msmexplorer/msmexplorer.git#egg=msmexplorer


Another option would be to to clone the `github repository
<https://github.com/msmexplorer/msmexplorer>`_ and install with ``pip install .``
from the source directory. MSMExplorer itself is pure Python, so installation
should be reasonably straightforward.


Dependencies
~~~~~~~~~~~~

-  Python 3.4+

Mandatory dependencies
^^^^^^^^^^^^^^^^^^^^^^

-  `numpy <http://www.numpy.org/>`__

-  `scipy <http://www.scipy.org/>`__

-  `matplotlib <matplotlib.sourceforge.net>`__

-  `networkx <https://networkx.github.io/>`__

-  `pandas <http://pandas.pydata.org/>`__

-  `seaborn <https://stanford.edu/~mwaskom/software/seaborn/>`__

-  `statsmodels <http://statsmodels.sourceforge.net/devel/>`__

-  `corner <http://corner.readthedocs.io/en/latest/>`__

-  `mdtraj <https://mdtraj.org>`__

-  `msmbuilder <https://msmbuilder.org>`__



Importing msmexplorer
~~~~~~~~~~~~~~~~~~~~~

By convention, ``msmexplorer`` is abbreviated to ``msme`` on import.


Bugs
~~~~

Please report any bugs you encounter through the github `issue tracker
<https://github.com/msmexplorer/msmexplorer/issues/new>`_. It will be most
helpful to include a reproducible example. It is difficult debug any issues
without knowing the versions of ``msmexplorer``, ``seaborn``, and
``matplotlib`` you are using, as well as what ``matplotlib`` backend you are
using to draw the plots, so please include those in your bug report.
