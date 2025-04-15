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


Example
-------

Compute correlation coefficient between two ordinal variables

.. code-block:: python

   from ordinalcorr import polychoric
   x = [1, 1, 2, 2, 3, 3]
   y = [0, 0, 0, 1, 1, 1]
   rho = polychoric(x, y)
   print(f"Polychoric correlation: {rho:.3f}")



Table of Contents
-----------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   user_guide
   api_reference
