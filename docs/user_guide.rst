.. toctree::
   :maxdepth: 2
   :caption: Contents:

User Guide
==========

Method Selection Guide
----------------------

The following table shows which correlation method to use based on your variable types:

+----------------------------+----------------------------+------------------------------------------------------------+
| Variable X                 | Variable Y                 | Method                                                     |
+============================+============================+============================================================+
| dichotomous (discretized)  | dichotomous (discretized)  | :py:func:`ordinalcorr.tetrachoric_corr`                    |
+----------------------------+----------------------------+------------------------------------------------------------+
| polytomous (discretized)   | polytomous (discretized)   | :py:func:`ordinalcorr.polychoric_corr`                     |
+----------------------------+----------------------------+------------------------------------------------------------+
| continuous                 | polytomous (discretized)   | :py:func:`ordinalcorr.polyserial_corr`                     |
+----------------------------+----------------------------+------------------------------------------------------------+
| continuous                 | dichotomous (discretized)  | :py:func:`ordinalcorr.biserial_corr`                       |
+----------------------------+----------------------------+------------------------------------------------------------+
| continuous                 | dichotomous                | :py:func:`ordinalcorr.point_biserial_corr`                 |
+----------------------------+----------------------------+------------------------------------------------------------+

Where:

- **dichotomous** variable: An ordinal variable with exactly two categories (e.g., Yes/No, 0/1).
- **polytomous** variable: An ordinal variable with more than two categories (e.g., Likert scale with 5 options).
- **discretized**: Indicates that the variable is assumed to originate from an underlying continuous latent distribution, and that observed categories result from applying thresholds to this latent variable.

