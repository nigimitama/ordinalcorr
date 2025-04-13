import unittest
import numpy as np
from ordinalcorr import biserial_corr  # Assuming this package is installed


class TestBiserialCorr(unittest.TestCase):

    def test_known_result(self):
        x = np.repeat([0.1, 0.2, 0.3, 0.4, 0.5], 10)
        y = np.repeat([0, 0, 1, 1, 1], 10)
        rho = biserial_corr(x, y)
        self.assertTrue(0.9 < rho, f"Expected high rho, got {rho}")

    def test_inverse_correlation(self):
        x = np.tile([1, 2, 3, 4, 5], 10)
        y = np.tile([1, 1, 0, 0, 0], 10)
        rho = biserial_corr(x, y)
        self.assertTrue(rho < -0.9, f"Expected strong negative rho, got {rho}")

    def test_no_correlation(self):
        x = np.tile([1, 2, 3], 20)
        y = np.repeat([0, 1, 0], 20)
        rho = biserial_corr(x, y)
        self.assertTrue(-0.1 < rho < 0.1, f"Expected close to zero rho, got {rho}")

    def test_single_category(self):
        x = np.repeat([1], 10)
        y = np.repeat([0], 10)
        rho = biserial_corr(x, y)
        self.assertTrue(
            np.isnan(rho) or abs(rho) < 1e-6,
            f"Expected undefined or near-zero rho, got {rho}",
        )


if __name__ == "__main__":
    unittest.main()
