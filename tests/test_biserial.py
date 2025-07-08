import numpy as np
from ordinalcorr import biserial


def test_known_result():
    x = np.repeat([0.1, 0.2, 0.3, 0.4, 0.5], 10)
    y = np.repeat([0, 0, 1, 1, 1], 10)
    rho = biserial(x, y)
    assert 0.9 < rho, f"Expected high rho, got {rho}"


def test_inverse_correlation():
    x = np.tile([1, 2, 3, 4, 5], 10)
    y = np.tile([1, 1, 0, 0, 0], 10)
    rho = biserial(x, y)
    assert rho < -0.9, f"Expected strong negative rho, got {rho}"


def test_no_correlation():
    x = np.tile([1, 2, 3], 20)
    y = np.repeat([0, 1, 0], 20)
    rho = biserial(x, y)
    assert -0.1 < rho < 0.1, f"Expected close to zero rho, got {rho}"


def test_single_category():
    x = np.repeat([1], 10)
    y = np.repeat([0], 10)
    rho = biserial(x, y)
    assert (
        np.isnan(rho) or abs(rho) < 1e-6
    ), f"Expected undefined or near-zero rho, got {rho}"


def test_different_length():
    x = np.repeat([0, 1], 10)
    y = np.repeat([1, 0], 11)
    rho = biserial(x, y)
    assert np.isnan(rho), f"Expected nan, got {rho}"
