"""
ordinalcorr - A Python package for ordinal correlation analysis
"""

__version__ = "0.4.3"

from ordinalcorr.polytomous import polychoric, polyserial
from ordinalcorr.dichotomous import biserial, point_biserial, tetrachoric

__all__ = [
    "polychoric",
    "polyserial",
    "biserial",
    "point_biserial",
    "tetrachoric",
]
