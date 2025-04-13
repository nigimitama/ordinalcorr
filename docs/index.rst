.. This file should at least contain the root `toctree` directive.

ordinalcorr
===========

`ordinalcorr` is a Python package for computing correlation coefficients designed for ordinal-scale data.


Installation
------------

.. code-block:: bash

   pip install ordinalcorr


Example
-------

Compute correlation coefficient between two ordinal variables

.. code-block:: python

   from ordinalcorr import polychoric_corr
   x = [1, 1, 2, 2, 3, 3]
   y = [0, 0, 0, 1, 1, 1]
   rho = polychoric_corr(x, y)
   print(f"Polychoric correlation: {rho:.3f}")



Table of Contents
-----------------

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   user_guide
   api_reference
