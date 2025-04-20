import unittest
import numpy as np
import pandas as pd
from ordinalcorr.corrmatrix import (
    hetcor,
    is_cols_ordinal,
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


class TestIsColsOrdinal(unittest.TestCase):
    """test helper functions in corrmatrix"""

    def test_two_cols(self):
        data = pd.DataFrame(
            {
                "continuous": np.repeat([0.1, 0.2, 0.3], 10),
                "dichotomous": np.repeat([0, 1, 1], 10),
                "polytomous": np.repeat([7, 5, 3], 10),
            }
        )
        actual = is_cols_ordinal(data, n_unique=10)
        expected = [False, True, True]
        self.assertEqual(list(actual), expected)


if __name__ == "__main__":
    unittest.main()
