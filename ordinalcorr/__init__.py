"""
ordinalcorr - A Python package for ordinal correlation analysis
"""

__version__ = "0.2.1"

from ordinalcorr.polytomous import polychoric_corr, polyserial_corr

__all__ = ["polychoric_corr", "polyserial_corr"]
