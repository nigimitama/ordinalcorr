import warnings
import numpy as np
from scipy.stats import norm
from ordinalcorr.types import ArrayLike
from ordinalcorr.validation import (
    ValidationError,
    check_if_data_is_dichotomous,
    check_if_zero_variance,
)


def biserial_corr(x: ArrayLike[float | int], y: ArrayLike[int]) -> float:
    """
    Compute the biserial correlation coefficient between a continuous variable x
    and a dichotomized variable y (0 or 1), assuming y was split from a latent continuous variable.

    Parameters
    ----------
    x : array-like
        Continuous variable.
    y : array-like
        Dichotomous variable (0 and 1), assumed to be derived from a latent continuous variable.

    Returns
    -------
    float
        Biserial correlation coefficient.

    Examples
    --------
    >>> from ordinalcorr import biserial_corr
    >>> x = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
    >>> y = np.array([0, 0, 1, 1, 1])
    >>> biserial_corr(x, y)

    """
    x = np.asarray(x)
    y = np.asarray(y)

    try:
        check_if_zero_variance(x)
        check_if_zero_variance(y)
    except ValidationError as e:
        warnings.warn(str(e))
        return np.nan

    try:
        check_if_data_is_dichotomous(y)
    except ValidationError as e:
        warnings.warn(str(e))
        return np.nan

    x1 = x[y == 1]
    x0 = x[y == 0]
    M1 = np.mean(x1)
    M0 = np.mean(x0)
    s = np.std(x, ddof=1)

    p = np.mean(y)
    q = 1 - p
    z = norm.ppf(p)
    phi = norm.pdf(z)

    return (M1 - M0) / s * (p * q) / phi


def point_biserial_corr(x: ArrayLike, y: ArrayLike) -> float:
    """
    Compute the point-biserial correlation between a continuous variable x
    and a dichotomous variable y (0 or 1), assuming y is a true dichotomous variable.

    Parameters
    ----------
    x : array-like
        Continuous variable.
    y : array-like
        Dichotomous variable (0 and 1).

    Returns
    -------
    float
        Point-biserial correlation coefficient.


    Examples
    --------
    >>> from ordinalcorr import point_biserial_corr
    >>> x = np.array([0.1, 0.2, 0.3, 0.4, 0.5])
    >>> y = np.array([0, 0, 1, 1, 1])
    >>> point_biserial_corr(x, y)

    References
    ----------
    .. [1] Lev, J. (1949). The point biserial coefficient of correlation. The Annals of Mathematical Statistics, 20(1), 125-126.
    .. [2] Kornbrot, D. (2014). Point biserial correlation. Wiley StatsRef: Statistics Reference Online.
    """
    x = np.asarray(x)
    y = np.asarray(y)

    try:
        check_if_zero_variance(x)
        check_if_zero_variance(y)
    except ValidationError as e:
        warnings.warn(str(e))
        return np.nan

    try:
        check_if_data_is_dichotomous(y)
    except ValidationError as e:
        warnings.warn(str(e))
        return np.nan

    x1 = x[y == 1]
    x0 = x[y == 0]

    M1 = np.mean(x1)
    M0 = np.mean(x0)
    s = np.std(x, ddof=1)

    p = np.mean(y)
    q = 1 - p

    return (M1 - M0) / s * np.sqrt(p * q)
