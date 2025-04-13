import unittest
import numpy as np
from ordinalcorr.validation import (
    ValidationError,
    check_if_zero_variance,
)  # Assuming this package is installed


class TestValidation(unittest.TestCase):
    """test helper functions in polytomous"""

    def test_check_if_zero_variance(self):
        # expected passing the check
        x = np.repeat([2, 4, 6], 10)
        check_if_zero_variance(x)

        # expected error
        x = np.repeat([42], 10)
        with self.assertRaises(ValidationError):
            check_if_zero_variance(x)


if __name__ == "__main__":
    unittest.main()
