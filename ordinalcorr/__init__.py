"""
ordinalcorr - correlation coefficients for ordinal-scale variables
"""

__version__ = "0.6.1"

from ordinalcorr.polytomous import polychoric, polyserial
from ordinalcorr.dichotomous import biserial, point_biserial, tetrachoric
from ordinalcorr.corrmatrix import hetcor

__all__ = [
    "polychoric",
    "polyserial",
    "biserial",
    "point_biserial",
    "tetrachoric",
    "hetcor",
]
