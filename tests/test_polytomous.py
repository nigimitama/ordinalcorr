import numpy as np
from ordinalcorr.polytomous import (
    estimate_thresholds,
    normalize_ordinal,
)


def test_estimate_thresholds_1():
    """test helper functions in polytomous"""
    x = np.tile([1, 2, 3], 10)
    tau = estimate_thresholds(x)
    assert np.isclose(tau, [-100.0, -0.4307273, 0.4307273, 100.0]).all()


def test_estimate_thresholds_2():
    x = np.repeat([2, 4, 6], 20)
    tau = estimate_thresholds(x)
    assert np.isclose(tau, [-100.0, -0.4307273, 0.4307273, 100.0]).all()


def test_normalize_ordinal_1():
    x = np.array([1, 2, 3, 1, 2, 3])
    actual = normalize_ordinal(x)
    expected = np.array([0, 1, 2, 0, 1, 2])
    assert actual.tolist() == expected.tolist()


def test_normalize_ordinal_2():
    x = np.array([2, 4, 9])
    actual = normalize_ordinal(x)
    expected = np.array([0, 1, 2])
    assert actual.tolist() == expected.tolist()
