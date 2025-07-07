import unittest
import numpy as np
import pandas as pd
from scipy.stats import multivariate_normal
from ordinalcorr.corrmatrix import (
    hetcor,
    is_cols_ordinal,
    polychoric,
    polyserial,
)


class TestHetcor(unittest.TestCase):

    def test_normal_data(self):
        data = pd.DataFrame(
            {
                "continuous": np.repeat([0.1, 0.2, 0.3], 10),
                "dichotomous": np.repeat([0, 1, 1], 10),
                "polytomous": np.repeat([7, 5, 3], 10),
            }
        )
        actual = hetcor(data).to_numpy()
        expect = np.array(
            [
                [1, 1, -1],
                [1, 1, -1],
                [-1, -1, 1],
            ]
        )
        self.assertTrue(np.isclose(actual, expect, atol=1e-2).all())
    
    def test_with_synthetic_data(self):
        multi_normal = generate_data()
        data = pd.DataFrame(
            {
                "continuous": multi_normal["x1"],
                "dichotomous": pd.cut(multi_normal["x2"], bins=2, labels=range(2)).astype(int),
                "polytomous": pd.cut(multi_normal["x2"], bins=3, labels=range(2)).astype(int),
            }
        )
        actual = hetcor(data).to_numpy()
        r_cd = polyserial(data["continuous"], data["dichotomous"])
        r_cp = polyserial(data["continuous"], data["polytomous"])
        r_dp = polychoric(data["dichotomous"], data["polytomous"])
        expect = np.array(
            [
                [1, r_cd, r_cp],
                [r_cd, 1, r_dp],
                [r_cp, r_dp, 1],
            ]
        )
        self.assertTrue(np.isclose(actual, expect, atol=1e-5).all())


def generate_data():
    # Generate data by standard normal distribution
    n = 500
    rho=0.5
    mean = [0, 0]
    std = [1, 1]
    cov = rho * std[0] * std[1]
    Cov = np.array([[std[0] ** 2, cov], [cov, std[1] ** 2]])
    X = multivariate_normal.rvs(mean=mean, cov=Cov, size=n, random_state=0)
    df = pd.DataFrame(X, columns=["x1", "x2"])
    return df



class TestIsColsOrdinal(unittest.TestCase):
    """test helper functions in corrmatrix"""

    def test_two_cols(self):
        data = pd.DataFrame(
            {
                "continuous": np.random.normal(size=30),
                "dichotomous": np.repeat([0, 1, 1], 10),
                "polytomous_int": np.repeat([7, 5, 3], 10),
                "polytomous_float": np.repeat([7.0, 5.0, 3.0], 10),
            }
        )
        actual = is_cols_ordinal(data, n_unique=10)
        expected = [False, True, True, True]
        self.assertEqual(list(actual), expected)


if __name__ == "__main__":
    unittest.main()
