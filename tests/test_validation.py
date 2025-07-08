import numpy as np
import pytest
from ordinalcorr.validation import (
    ValidationError,
    check_if_zero_variance,
)


def test_check_if_zero_variance():
    """test helper functions in polytomous"""
    # expected passing the check
    x = np.repeat([2, 4, 6], 10)
    check_if_zero_variance(x)

    # expected error
    x = np.repeat([42], 10)
    with pytest.raises(ValidationError):
        check_if_zero_variance(x)
