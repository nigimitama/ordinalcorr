import warnings
import numpy as np
from scipy.stats import norm, multivariate_normal
from scipy.optimize import minimize_scalar
from ordinalcorr.validation import ValidationError, check_if_zero_variance
from ordinalcorr.types import ArrayLike


def univariate_cdf(lower, upper):
    """Compute the univariate cumulative distribution function (CDF) for a standard normal distribution."""
    mean = 0.0
    var = 1.0
    std = np.sqrt(var)
    return norm.cdf(upper, loc=mean, scale=std) - norm.cdf(lower, loc=mean, scale=std)


def bivariate_cdf(lower, upper, rho: float) -> float:
    """Compute the bivariate cumulative distribution function (CDF) for a standard normal distribution."""
    var = 1
    cov = np.array([[var, rho], [rho, var]])

    # Compute probability as difference of CDFs
    # P_ij = Φ₂(τ_{i}, τ_{j}) - Φ₂(τ_{i-1}, τ_{j}) - Φ₂(τ_{i}, τ_{j-1}) + Φ₂(τ_{i-1}, τ_{j-1})
    Phi2 = multivariate_normal(mean=[0, 0], cov=cov).cdf
    return (
        Phi2(upper)
        - Phi2([upper[0], lower[1]])
        - Phi2([lower[0], upper[1]])
        + Phi2(lower)
    )


def estimate_thresholds(values):
    """Estimate thresholds from empirical marginal proportions"""
    inf = 100  # to make log-likelihood smooth, use large value instead of np.inf
    thresholds = []
    levels = np.sort(np.unique(values))
    for level in levels[:-1]:  # exclude top category
        p = np.mean(values <= level)
        thresholds.append(norm.ppf(p))  # τ_i = Φ⁻¹(P(X ≤ i))
    return np.concatenate(([-inf], thresholds, [inf]))


def normalize_ordinal(x: np.ndarray[int]) -> np.ndarray[int]:
    """Normalize ordinal variable to be integer-coded starting from 0."""
    unique_values = np.unique(x)
    value_to_code = {value: code for code, value in enumerate(unique_values)}
    return np.vectorize(value_to_code.get)(x)


def polychoric_corr(x: ArrayLike[int], y: ArrayLike[int]) -> float:
    """
    Estimate the polychoric correlation coefficient between two ordinal variables.

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
    >>> from ordinalcorr import polychoric_corr
    >>> x = [1, 1, 2, 2, 3, 3]
    >>> y = [0, 0, 0, 1, 1, 1]
    >>> polychoric_corr(x, y)

    References
    ----------
    .. [1] Olsson, U. (1979). Maximum likelihood estimation of the polychoric correlation coefficient. Psychometrika, 44(4), 443-460.
    .. [2] Drasgow, F. (1986). Polychoric and polyserial correlations In: Kotz S, Johnson N, editors. The Encyclopedia of Statistics.
    """

    # Step 1: Ensure inputs are numpy arrays and integer-coded
    x = np.asarray(x)
    y = np.asarray(y)

    try:
        check_if_zero_variance(x)
        check_if_zero_variance(y)
    except ValidationError as e:
        warnings.warn(str(e))
        return np.nan

    # Step 2: Identify unique ordinal levels
    x_levels = np.sort(np.unique(x))
    y_levels = np.sort(np.unique(y))

    if x_levels.size <= 1 or y_levels.size <= 1:
        Warning("Both x and y must have at least two unique ordinal levels.")
        return np.nan

    # Step 3: Estimate thresholds from empirical marginal proportions
    tau_x = estimate_thresholds(x)  # thresholds for X: τ_X
    tau_y = estimate_thresholds(y)  # thresholds for Y: τ_Y

    # Step 4: Construct contingency table n_ij
    contingency = np.zeros((len(tau_x) - 1, len(tau_y) - 1), dtype=int)
    for i, xi in enumerate(x_levels):
        for j, yj in enumerate(y_levels):
            contingency[i, j] = np.sum((x == xi) & (y == yj))  # n_ij

    # Step 5: Define negative log-likelihood function based on P_ij = Φ₂(τ_i, τ_j; ρ)
    def neg_log_likelihood(rho):
        log_likelihood = 0.0
        for i in range(len(tau_x) - 1):
            for j in range(len(tau_y) - 1):
                if contingency[i, j] == 0:
                    continue

                lower = [tau_x[i], tau_y[j]]
                upper = [tau_x[i + 1], tau_y[j + 1]]

                p_ij = bivariate_cdf(lower, upper, rho)
                p_ij = max(p_ij, 1e-6)  # soft clipping

                if np.isnan(p_ij):
                    continue

                log_likelihood += contingency[i, j] * np.log(p_ij)

        return -log_likelihood

    # Step 6: Optimize to find MLE for rho
    eps = 1e-10
    result = minimize_scalar(
        neg_log_likelihood, bounds=(-1 + eps, 1 - eps), method="bounded"
    )
    return result.x


def polyserial_corr(x: ArrayLike[float | int], y: ArrayLike[int]) -> float:
    """
    Estimate the polyserial correlation coefficient between a continuous variable x
    and an ordinal variable y using the two-step maximum likelihood estimation.

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
    >>> from ordinalcorr import polyserial_corr
    >>> x = [0.1, 0.1, 0.2, 0.2, 0.3, 0.3]
    >>> y = [0, 0, 0, 1, 1, 2]
    >>> polyserial_corr(x, y)

    References
    ----------
    .. [1] Drasgow, F. (1986). Polychoric and polyserial correlations In: Kotz S, Johnson N, editors. The Encyclopedia of Statistics.
    """
    x = np.asarray(x)
    y = np.asarray(y)

    try:
        check_if_zero_variance(x)
        check_if_zero_variance(y)
    except ValidationError as e:
        warnings.warn(str(e))
        return np.nan

    z = (x - np.mean(x)) / np.std(x, ddof=0)
    y = normalize_ordinal(y)
    tau = estimate_thresholds(y)

    def neg_log_likelihood(rho):
        log_likelihood = 0.0
        for i in range(len(z)):
            j = y[i]
            tau_lower = (tau[j] - rho * z[i]) / np.sqrt(1 - rho**2)
            tau_upper = (tau[j + 1] - rho * z[i]) / np.sqrt(1 - rho**2)
            p_i = univariate_cdf(tau_lower, tau_upper)

            p_i = max(p_i, 1e-6)  # soft clipping
            if np.isnan(p_i):
                continue

            log_likelihood += np.log(p_i)

        return -log_likelihood

    eps = 1e-10
    result = minimize_scalar(
        neg_log_likelihood, bounds=(-1 + eps, 1 - eps), method="bounded"
    )
    return result.x
