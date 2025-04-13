import numpy as np
from scipy.stats import norm, multivariate_normal
from scipy.optimize import minimize_scalar
from ordinalcorr.validation import check_if_zero_variance
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


def polychoric_corr(x: ArrayLike, y: ArrayLike) -> float:
    """
    Estimate the polychoric correlation coefficient between two ordinal variables.

    Parameters
    ----------
    x : array_like
        Ordinal variable X (integer-coded).
    y : array_like
        Ordinal variable Y (integer-coded).

    Returns
    -------
    float
        Estimated polychoric correlation coefficient (rho).
    """

    # Step 1: Ensure inputs are numpy arrays and integer-coded
    x = np.asarray(x)
    y = np.asarray(y)

    x = check_if_zero_variance(x)
    y = check_if_zero_variance(y)

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


def polyserial_corr(x: ArrayLike, y: np.ndarray) -> float:
    """
    Estimate the polyserial correlation coefficient between a continuous variable x
    and an ordinal variable y using maximum likelihood estimation.

    Parameters
    ----------
    x : array_like
        Continuous variable (standardized recommended).
    y : array_like
        Ordinal variable (integer-coded, ordered categories).

    Returns
    -------
    float
        Estimated polyserial correlation coefficient (rho).
    """
    x = np.asarray(x)
    y = np.asarray(y)

    x = check_if_zero_variance(x)
    y = check_if_zero_variance(y)

    z = (x - np.mean(x)) / np.std(x)
    tau = estimate_thresholds(y)

    def neg_log_likelihood(rho):
        log_likelihood = 0.0
        for zi, yi in zip(z, y):
            tau_lower = (tau[yi] - rho * zi) / np.sqrt(1 - rho**2)
            tau_upper = (tau[yi + 1] - rho * zi) / np.sqrt(1 - rho**2)
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
