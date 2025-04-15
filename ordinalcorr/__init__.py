"""
ordinalcorr - A Python package for ordinal correlation analysis
"""

__version__ = "0.4.3"

from ordinalcorr.polytomous import polychoric_corr, polyserial_corr
from ordinalcorr.dichotomous import biserial_corr, point_biserial_corr, tetrachoric_corr

__all__ = [
    "polychoric_corr",
    "polyserial_corr",
    "biserial_corr",
    "point_biserial_corr",
    "tetrachoric_corr",
]
