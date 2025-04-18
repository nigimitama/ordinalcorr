import warnings
import numpy as np
from scipy.stats import norm, multivariate_normal
from scipy.optimize import minimize_scalar
from ordinalcorr.types import ArrayLike
from ordinalcorr.validation import (
    ValidationError,
    check_if_data_is_dichotomous,
    check_if_zero_variance,
    check_length_are_same,
)


def biserial(x: ArrayLike[float | int], y: ArrayLike[int]) -> float:
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
    >>> from ordinalcorr import biserial
    >>> x = [0.1, 0.2, 0.3, 0.4, 0.5]
    >>> y = [0, 0, 1, 1, 1]
    >>> biserial(x, y)

    :Details:

    The biserial correlation coefficient is defined as:

    .. math::

        r_{b} = r_{pb} \\cdot \\frac{\\sqrt{p (1 - p)}}{\\phi(z)}
        = \\frac{\\bar{X}_1 - \\bar{X}_0}{s_X} \\cdot \\frac{p (1 - p)}{\\phi(z)}

    where

    - :math:`r_{pb}` is the point-biserial correlation coefficient
    - :math:`\\bar{X}_1` and :math:`\\bar{X}_0` are the means of the continuous variable for the two categories of the dichotomous variable
        - :math:`\\bar{X}_1 = \\frac{1}{n_1} \\sum_{i:Y_i = 1} X_i, \\quad n_1 = |\\{i: Y_i = 1\\}|`
        - :math:`\\bar{X}_0 = \\frac{1}{n_0} \\sum_{i:Y_i = 0} X_i, \\quad n_0 = |\\{i: Y_i = 0\\}|`
    - :math:`s_X` is the standard deviation of the continuous variable
        - :math:`s_X = \\sqrt{\\frac{1}{n} \\sum_{i=1}^{n} (X_i - \\bar{X})^2}, \\quad n = n_1 + n_0`
    - :math:`p` is the proportion of `Y = 1` of the dichotomous variable
        - :math:`p = \\frac{n_1}{n}`
    - :math:`\\phi(z)` is the probability density function of the standard normal distribution
    - :math:`z` is the percentile of :math:`p` in the standard normal distribution


    """
    rho_pbi = point_biserial(x, y)
    if np.isnan(rho_pbi):
        return np.nan

    # calculate the correction factor
    p = np.mean(y)
    q = 1 - p
    z = norm.ppf(p)
    c = np.sqrt(p * q) / norm.pdf(z)
    return rho_pbi * c


def point_biserial(x: ArrayLike, y: ArrayLike) -> float:
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
    >>> from ordinalcorr import point_biserial
    >>> x = [0.1, 0.2, 0.3, 0.4, 0.5]
    >>> y = [0, 0, 1, 1, 1]
    >>> point_biserial(x, y)


    :Details:

    The point-biserial correlation coefficient is defined as:

    .. math::

        r_{pb} = \\frac{\\bar{X}_1 - \\bar{X}_0}{s_X} \\sqrt{p \\times (1 - p)}

    where

    - :math:`\\bar{X}_1` and :math:`\\bar{X}_0` are the means of the continuous variable for the two categories of the dichotomous variable
        - :math:`\\bar{X}_1 = \\frac{1}{n_1} \\sum_{i:Y_i = 1} X_i, \\quad n_1 = |\\{i: Y_i = 1\\}|`
        - :math:`\\bar{X}_0 = \\frac{1}{n_0} \\sum_{i:Y_i = 0} X_i, \\quad n_0 = |\\{i: Y_i = 0\\}|`
    - :math:`s_X` is the standard deviation of the continuous variable
        - :math:`s_X = \\sqrt{\\frac{1}{n} \\sum_{i=1}^{n} (X_i - \\bar{X})^2}, \\quad n = n_1 + n_0`
    - :math:`p` is the proportion of `Y = 1` of the dichotomous variable
        - :math:`p = \\frac{n_1}{n}`

    Note that the point-biserial correlation coefficient is equivalent to the Pearson correlation coefficient between the continuous variable and the dichotomous variable.

    References
    ----------
    .. [1] Lev, J. (1949). The point biserial coefficient of correlation. The Annals of Mathematical Statistics, 20(1), 125-126.
    .. [2] Kornbrot, D. (2014). Point biserial correlation. Wiley StatsRef: Statistics Reference Online.
    """
    x = np.asarray(x)
    y = np.asarray(y)

    try:
        check_length_are_same(x, y)
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
    s = np.std(x, ddof=0)

    p = np.mean(y)
    q = 1 - p

    return (M1 - M0) / s * np.sqrt(p * q)


def tetrachoric(x: ArrayLike[int], y: ArrayLike[int]) -> float:
    """
    Estimate the tetrachoric correlation coefficient between two dichotomous variables.

    The tetrachoric correlation assumes that the two observed dichotomous variables
    are thresholded representations of underlying continuous variables that follow
    a bivariate normal distribution.

    This method is appropriate when both variables are dichotomous (e.g., yes/no,
    success/failure) but believed to originate from an underlying normally
    distributed process.


    Parameters
    ----------
    x : array-like
        Dichotomous variable (consisting of 0 and 1).
    y : array-like
        Dichotomous variable (consisting of 0 and 1).

    Returns
    -------
    float
        Tetrachoric correlation coefficient.


    Examples
    --------
    >>> from ordinalcorr import tetrachoric
    >>> x = [0, 0, 1, 1, 1]
    >>> y = [0, 1, 0, 1, 1]
    >>> tetrachoric(x, y)

    """
    # NOTE: The estimation is the same as polyserial with dichotomous variables.
    # However, this is a bit smaller computational complexity and faster than polyserial.
    x = np.asarray(x)
    y = np.asarray(y)

    try:
        check_length_are_same(x, y)
        check_if_zero_variance(x)
        check_if_zero_variance(y)
        check_if_data_is_dichotomous(x)
        check_if_data_is_dichotomous(y)
    except ValidationError as e:
        warnings.warn(str(e))
        return np.nan

    n = len(x)
    n00 = np.sum((x == 0) & (y == 0))
    n01 = np.sum((x == 0) & (y == 1))
    n10 = np.sum((x == 1) & (y == 0))
    n11 = np.sum((x == 1) & (y == 1))

    px0 = (n00 + n01) / n
    py0 = (n00 + n10) / n

    tau_x = norm.ppf(px0)
    tau_y = norm.ppf(py0)

    def neg_log_likelihood(rho):
        phi_x = norm.cdf(tau_x)
        phi_y = norm.cdf(tau_y)

        cov = np.array([[1, rho], [rho, 1]])
        p00 = multivariate_normal.cdf([tau_x, tau_y], mean=[0, 0], cov=cov)
        p01 = phi_x - p00
        p10 = phi_y - p00
        p11 = 1 - phi_x - phi_y + p00

        probs = np.array([p00, p01, p10, p11])
        counts = np.array([n00, n01, n10, n11])

        assert np.all(probs >= 0), f"{probs=}"

        return -(counts @ np.log(probs))

    eps = 1e-10
    result = minimize_scalar(
        neg_log_likelihood, bounds=(-1 + eps, 1 - eps), method="bounded"
    )
    return result.x
