import numpy as np


class ValidationError(Exception):
    pass


def check_if_zero_variance(x):
    if len(set(x)) == 1:
        raise ValidationError(
            "all elements in the input are the same and zero variance"
        )


def check_if_data_is_dichotomous(y):
    is_dichotomous = set(np.unique(y)) == {0, 1}
    if not is_dichotomous:
        raise ValidationError(
            "dichotomous (binary) variable 'y' must be consist of {0, 1}"
        )
