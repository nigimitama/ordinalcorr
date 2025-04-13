.. toctree::
   :maxdepth: 2
   :caption: Contents:

User Guide
==========

Method Selection Guide
----------------------

The following table shows which correlation method to use based on your variable types:

+----------------+--------------------------------------+-----------------------------------------------+
| Variable X     | Variable Y                           | Method                                        |
+================+======================================+===============================================+
| ordinal        | ordinal                              | :py:func:`ordinalcorr.polychoric_corr`        |
+----------------+--------------------------------------+-----------------------------------------------+
| continuous     | ordinal                              | :py:func:`ordinalcorr.polyserial_corr`        |
+----------------+--------------------------------------+-----------------------------------------------+
| continuous     | binary (discretized from continuous) | :py:func:`ordinalcorr.biserial_corr`          |
+----------------+--------------------------------------+-----------------------------------------------+
| continuous     | binary                               | :py:func:`ordinalcorr.point_biserial_corr`    |
+----------------+--------------------------------------+-----------------------------------------------+
