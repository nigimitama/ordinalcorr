import unittest
import numpy as np
import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.absolute()
sys.path.append(project_root)

from ordinalcorr.polytomous import polychoric_corr


class TestPolychoricCorr(unittest.TestCase):

    def test_known_result(self):
        x = np.repeat([1, 2, 3], 10)
        y = np.repeat([1, 2, 3], 10)
        rho = polychoric_corr(x, y)
        self.assertTrue(0.9 < rho < 1.0, f"Expected high rho, got {rho}")

    def test_inverse_correlation(self):
        x = np.tile([1, 2, 3], 10)
        y = np.tile([3, 2, 1], 10)
        rho = polychoric_corr(x, y)
        self.assertTrue(-1.0 < rho < -0.9, f"Expected strong negative rho, got {rho}")

    def test_no_correlation(self):
        x = np.tile([1, 2, 3], 20)
        y = np.repeat([1, 2, 3], 20)
        rho = polychoric_corr(x, y)
        self.assertTrue(-0.1 < rho < 0.1, f"Expected close to zero rho, got {rho}")

    def test_single_category(self):
        x = np.repeat([1], 10)
        y = np.repeat([0], 10)
        rho = polychoric_corr(x, y)
        self.assertTrue(
            np.isnan(rho) or abs(rho) < 1e-6,
            f"Expected undefined or near-zero rho, got {rho}",
        )


if __name__ == "__main__":
    unittest.main()
