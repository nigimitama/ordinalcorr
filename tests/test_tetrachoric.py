import unittest
import numpy as np
from ordinalcorr import tetrachoric_corr
from ordinalcorr.validation import ValidationError  # Assuming this package is installed


class TestTetrachoricCorr(unittest.TestCase):

    def test_positive_correlation(self):
        x = np.repeat([0, 1], 10)
        y = np.repeat([0, 1], 10)
        rho = tetrachoric_corr(x, y)
        self.assertTrue(0.9 < rho <= 1, f"Expected high rho, got {rho}")

    def test_inverse_correlation(self):
        x = np.tile([0, 1], 10)
        y = np.tile([1, 0], 10)
        rho = tetrachoric_corr(x, y)
        self.assertTrue(-1 <= rho < -0.9, f"Expected strong negative rho, got {rho}")

    def test_no_correlation(self):
        x = np.repeat([0, 1, 0, 1], 20)
        y = np.repeat([0, 0, 1, 1], 20)
        rho = tetrachoric_corr(x, y)
        self.assertTrue(-0.1 < rho < 0.1, f"Expected close to zero rho, got {rho}")

    def test_single_category(self):
        x = np.repeat([1], 10)
        y = np.repeat([0], 10)
        rho = tetrachoric_corr(x, y)
        self.assertTrue(
            np.isnan(rho),
            f"Expected undefined or near-zero rho, got {rho}",
        )

    def test_validation_for_zero_variance(self):
        x = np.repeat([0], 10)
        y = np.repeat([1], 10)
        rho = tetrachoric_corr(x, y)
        self.assertTrue(
            np.isnan(rho),
            f"Expected undefined or near-zero rho, got {rho}",
        )

    def test_validation_for_polytomous_variables(self):
        x = np.repeat([0, 1, 2], 10)
        y = np.repeat([0, 1, 0], 10)
        rho = tetrachoric_corr(x, y)
        self.assertTrue(
            np.isnan(rho),
            f"Expected undefined or near-zero rho, got {rho}",
        )


if __name__ == "__main__":
    unittest.main()
