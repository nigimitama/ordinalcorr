import warnings
from typing import Any, Sequence
import numpy as np
import numpy.typing as npt
from scipy.special import ndtr, owens_t
from scipy.stats import norm
from scipy.optimize import minimize_scalar
from ordinalcorr.validation import (
    ValidationError,
    check_if_zero_variance,
    check_length_are_same,
)


def univariate_cdf(
    lower: npt.ArrayLike, upper: npt.ArrayLike
) -> npt.NDArray[np.float64]:
    """Compute the univariate cumulative distribution function (CDF) for a standard normal distribution.

    P(lower < X <= upper) = Φ(upper) - Φ(lower)

    where Φ is the CDF of the standard normal distribution.
    Accepts scalars or arrays (evaluated elementwise).
    """
    return ndtr(upper) - ndtr(lower)


def bivariate_normal_cdf(
    h: npt.ArrayLike, k: npt.ArrayLike, rho: float
) -> npt.NDArray[np.float64]:
    """Compute the standard bivariate normal CDF Φ₂(h, k; ρ) using Owen's T function.

    Φ₂(h, k; ρ) = (Φ(h) + Φ(k)) / 2 − T(h, a_h) − T(k, a_k) − δ

    where a_h = (k − ρh) / (h·√(1−ρ²)), a_k = (h − ρk) / (k·√(1−ρ²)),
    and δ = 1/2 if h·k < 0, otherwise 0.

    This closed form is exact and vectorized in h and k.

    References
    ----------
    .. [1] Owen, D. B. (1956). Tables for computing bivariate normal probabilities.
           The Annals of Mathematical Statistics, 27(4), 1075-1090.
    """
    rho = float(np.clip(rho, -1 + 1e-12, 1 - 1e-12))
    # nudge exact zeros to avoid 0/0 in a_h and a_k; owens_t evaluates infinite
    # and near-infinite a exactly, so this equals the h→0 limit at machine precision
    tiny = 1e-100
    h = np.where(h == 0, tiny, np.asarray(h, dtype=float))
    k = np.where(k == 0, tiny, np.asarray(k, dtype=float))

    denom = np.sqrt((1.0 - rho) * (1.0 + rho))
    t_h = owens_t(h, (k - rho * h) / (h * denom))
    t_k = owens_t(k, (h - rho * k) / (k * denom))
    delta = np.where(h * k < 0, 0.5, 0.0)
    return np.clip(0.5 * (ndtr(h) + ndtr(k)) - t_h - t_k - delta, 0.0, 1.0)


def bivariate_cdf(lower: Sequence[float], upper: Sequence[float], rho: float) -> float:
    """Compute the rectangle probability for a standard bivariate normal distribution.

    P(lower_x < X <= upper_x, lower_y < Y <= upper_y)
        = Φ₂(upper_x, upper_y) - Φ₂(lower_x, upper_y) - Φ₂(upper_x, lower_y) + Φ₂(lower_x, lower_y)

    where Φ₂ is the CDF of the bivariate normal distribution with correlation coefficient ρ.
    """
    h = np.array([upper[0], lower[0], upper[0], lower[0]])
    k = np.array([upper[1], upper[1], lower[1], lower[1]])
    Phi2 = bivariate_normal_cdf(h, k, rho)
    return float(Phi2[0] - Phi2[1] - Phi2[2] + Phi2[3])


def estimate_thresholds(values: npt.NDArray[Any]) -> npt.NDArray[np.float64]:
    r"""Estimate thresholds from empirical marginal proportions"""
    inf = 100  # to make log-likelihood smooth, use large value instead of np.inf
    _, counts = np.unique(values, return_counts=True)
    cum_p = np.cumsum(counts)[:-1] / values.size  # P(X ≤ i), exclude top category
    thresholds = norm.ppf(cum_p)  # τ_i = Φ⁻¹(P(X ≤ i))
    return np.concatenate(([-inf], thresholds, [inf]))


def normalize_ordinal(x: npt.NDArray[Any]) -> npt.NDArray[np.int_]:
    r"""Normalize ordinal variable to be integer-coded starting from 0."""
    _, codes = np.unique(x, return_inverse=True)
    return codes


def polychoric(x: npt.ArrayLike, y: npt.ArrayLike) -> float:
    r"""
    Estimate the polychoric correlation coefficient between two ordinal variables.

    The polychoric correlation assumes that the two observed ordinal variables
    are thresholded representations of underlying continuous variables that follow
    a bivariate normal distribution.


    Parameters
    ----------
    x : array_like (int)
        Ordinal variable.
    y : array_like (int)
        Ordinal variable.

    Returns
    -------
    float
        Estimated polychoric correlation coefficient.

    Examples
    --------
    >>> from ordinalcorr import polychoric
    >>> x = [1, 1, 2, 2, 3, 3]
    >>> y = [0, 0, 0, 1, 1, 1]
    >>> round(float(polychoric(x, y)), 4)
    0.9986

    References
    ----------
    .. [1] Olsson, U. (1979). Maximum likelihood estimation of the polychoric correlation coefficient. Psychometrika, 44(4), 443-460.
    .. [2] Drasgow, F. (1986). Polychoric and polyserial correlations In: Kotz S, Johnson N, editors. The Encyclopedia of Statistics.
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

    x_levels = np.sort(np.unique(x))
    y_levels = np.sort(np.unique(y))

    if x_levels.size <= 1 or y_levels.size <= 1:
        Warning("Both x and y must have at least two unique ordinal levels.")
        return np.nan

    tau_x = estimate_thresholds(x)  # thresholds for X: τ_X
    tau_y = estimate_thresholds(y)  # thresholds for Y: τ_Y

    contingency = np.zeros((len(tau_x) - 1, len(tau_y) - 1), dtype=int)
    for i, xi in enumerate(x_levels):
        for j, yj in enumerate(y_levels):
            contingency[i, j] = np.sum((x == xi) & (y == yj))  # n_ij

    # evaluate Φ₂ once on the grid of all threshold corners, then take
    # P(τ_x[i] < X <= τ_x[i+1], τ_y[j] < Y <= τ_y[j+1]) by 2D differencing
    grid_x, grid_y = np.meshgrid(tau_x, tau_y, indexing="ij")

    def neg_log_likelihood(rho: float) -> float:
        Phi2 = bivariate_normal_cdf(grid_x, grid_y, rho)
        p = Phi2[1:, 1:] - Phi2[:-1, 1:] - Phi2[1:, :-1] + Phi2[:-1, :-1]
        p = np.maximum(p, 1e-6)  # soft clipping
        mask = (contingency > 0) & ~np.isnan(p)
        return -np.sum(contingency[mask] * np.log(p[mask]))

    result = minimize_scalar(neg_log_likelihood, bounds=(-1, 1), method="bounded")
    return float(result.x)


def polyserial(x: npt.ArrayLike, y: npt.ArrayLike) -> float:
    r"""
    Estimate the polyserial correlation coefficient between a continuous variable :math:`x`
    and an ordinal variable :math:`y` using the two-step maximum likelihood estimation.

    The polyserial correlation assumes that the ordinal variable :math:`y` is a thresholded
    representation of latent continuous variable that follows a normal distribution.


    Parameters
    ----------
    x : array_like (float | int)
        Continuous variable.
    y : array_like (int)
        Ordinal variable.

    Returns
    -------
    float
        Estimated polyserial correlation coefficient.

    Examples
    --------
    >>> from ordinalcorr import polyserial
    >>> x = [0.1, 0.1, 0.2, 0.2, 0.3, 0.3]
    >>> y = [0, 0, 0, 1, 1, 2]
    >>> round(polyserial(x, y), 4)
    0.9017

    References
    ----------
    .. [1] Drasgow, F. (1986). Polychoric and polyserial correlations In: Kotz S, Johnson N, editors. The Encyclopedia of Statistics.
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

    z = (x - np.mean(x)) / np.std(x, ddof=0)
    y = normalize_ordinal(y)
    tau = estimate_thresholds(y)
    tau_lower = tau[y]  # τ_{y_i}
    tau_upper = tau[y + 1]  # τ_{y_i + 1}

    def neg_log_likelihood(rho: float) -> float:
        scale = np.sqrt(1 - rho**2)
        p = univariate_cdf((tau_lower - rho * z) / scale, (tau_upper - rho * z) / scale)
        p = np.maximum(p, 1e-6)  # soft clipping
        return -np.sum(np.log(p, where=~np.isnan(p), out=np.zeros_like(p)))

    result = minimize_scalar(neg_log_likelihood, bounds=(-1, 1), method="bounded")
    return float(result.x)
