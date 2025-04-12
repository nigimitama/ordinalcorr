import numpy as np
from scipy.stats import norm
from ordinalcorr.types import ArrayLike


def biserial_corr(x: ArrayLike, y: ArrayLike) -> float:
    """
    Compute the biserial correlation coefficient between a continuous variable x
    and a dichotomized variable y (0 or 1), assuming y was split from a latent normal variable.

    Parameters
    ----------
    x : array-like
        Continuous variable.
    y : array-like
        Dichotomous variable (0 and 1), assumed to be derived from a latent normal variable.

    Returns
    -------
    float
        Biserial correlation coefficient.
    """
    x = np.asarray(x)
    y = np.asarray(y)

    assert set(np.unique(y)).issubset({0, 1}), "y must be binary (0/1)"

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
    and a binary variable y (0 or 1), assuming y is a true categorical variable.

    Parameters
    ----------
    x : array-like
        Continuous variable.
    y : array-like
        Binary variable (0 and 1), true categories.

    Returns
    -------
    float
        Point-biserial correlation coefficient.
    """
    x = np.asarray(x)
    y = np.asarray(y)

    assert set(np.unique(y)).issubset({0, 1}), "y must be binary (0/1)"

    x1 = x[y == 1]
    x0 = x[y == 0]

    M1 = np.mean(x1)
    M0 = np.mean(x0)
    s = np.std(x, ddof=1)

    p = np.mean(y)
    q = 1 - p

    return (M1 - M0) / s * np.sqrt(p * q)
