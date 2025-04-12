import warnings
import numpy as np


def check_if_zero_variance(x):
    if len(set(x)) == 1:
        warnings.warn(
            "all elements in the input are the same and zero variance", UserWarning
        )
        return np.nan

    # if x is OK, return x
    return x
