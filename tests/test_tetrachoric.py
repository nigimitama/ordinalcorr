import numpy as np
import pytest
from ordinalcorr import tetrachoric, polychoric


def test_positive_correlation():
    x = np.repeat([0, 1], 10)
    y = np.repeat([0, 1], 10)
    rho = tetrachoric(x, y)
    assert 0.9 < rho <= 1, f"Expected high rho, got {rho}"


def test_inverse_correlation():
    x = np.tile([0, 1], 10)
    y = np.tile([1, 0], 10)
    rho = tetrachoric(x, y)
    assert -1 <= rho < -0.9, f"Expected strong negative rho, got {rho}"


def test_no_correlation():
    x = np.repeat([0, 1, 0, 1], 20)
    y = np.repeat([0, 0, 1, 1], 20)
    rho = tetrachoric(x, y)
    assert -0.1 < rho < 0.1, f"Expected close to zero rho, got {rho}"


def test_single_category():
    x = np.repeat([1], 10)
    y = np.repeat([0], 10)
    rho = tetrachoric(x, y)
    assert np.isnan(rho), f"Expected undefined or near-zero rho, got {rho}"


def test_different_length():
    x = np.repeat([0, 1], 10)
    y = np.repeat([1, 0], 11)
    rho = tetrachoric(x, y)
    assert np.isnan(rho), f"Expected nan, got {rho}"


def test_validation_for_zero_variance():
    x = np.repeat([0], 10)
    y = np.repeat([1], 10)
    rho = tetrachoric(x, y)
    assert np.isnan(rho), f"Expected undefined or near-zero rho, got {rho}"


def test_validation_for_polytomous_variables():
    x = np.repeat([0, 1, 2], 10)
    y = np.repeat([0, 1, 0], 10)
    rho = tetrachoric(x, y)
    assert np.isnan(rho), f"Expected undefined or near-zero rho, got {rho}"


def test_tetrachoric_polychoric_equivalence():
    test_cases = [
        (np.repeat([0, 1], 10), np.repeat([0, 1], 10)),
        (np.repeat([0, 1], 10), np.repeat([1, 0], 10)),
        (np.repeat([1, 0], 10), np.repeat([0, 1], 10)),
        (np.repeat([1, 0], 10), np.repeat([1, 0], 10)),
    ]
    for x, y in test_cases:
        rho_tetrachoric = tetrachoric(x, y)
        rho_polychoric = polychoric(x, y)
        assert rho_tetrachoric == pytest.approx(rho_polychoric)
