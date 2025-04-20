.. This file should at least contain the root `toctree` directive.

ordinalcorr
===========

`ordinalcorr` is a Python package for computing correlation coefficients designed for ordinal-scale data.


Installation
------------

ordinalcorr is available at the `PyPI <https://pypi.org/project/ordinalcorr/>`_

.. code-block:: bash

   pip install ordinalcorr


Requirements
~~~~~~~~~~~~

- Python 3.10 or later
- Dependencies:
   - numpy >= 1.23.0
   - scipy >= 1.8.0


Features
--------

Correlation Coefficients
~~~~~~~~~~~~~~~~~~~~~~~~

This package provides several correlation coefficients (e.g. Polyserial and Polychoric)

.. code-block:: python

   >>> from ordinalcorr import polychoric
   >>> x = [1, 1, 2, 2, 3, 3]
   >>> y = [0, 0, 0, 1, 1, 1]
   >>> polychoric(x, y)
   0.9986287922233864


Details can be found in the :doc:`api_reference` and the :doc:`method_selection_guide`.



Heterogeneous Correlation Matrix
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A function for computing the *heterogeneous correlation matrix*—a correlation matrix that includes both continuous and ordinal variables—is also provided.


.. code-block:: python

   >>> from ordinalcorr import hetcor
   >>> import pandas as pd
   >>> data = pd.DataFrame({
   ...     "continuous": [0.1, 0.1, 0.2, 0.2, 0.3, 0.3],
   ...     "dichotomous": [0, 0, 0, 1, 1, 1],
   ...     "polytomous": [1, 1, 3, 3, 2, 2],
   ... })
   >>> hetcor(data)
                continuous  dichotomous  polytomous
   continuous     1.000000     0.989335    0.514870
   dichotomous    0.989335     1.000000    0.549231
   polytomous     0.514870     0.549231    1.000000



Table of Contents
-----------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   user_guide
   api_reference
