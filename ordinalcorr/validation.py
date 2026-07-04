from typing import Any
import numpy as np
import numpy.typing as npt


class ValidationError(Exception):
    pass


def check_if_zero_variance(x: npt.NDArray[Any]) -> None:
    if len(set(x)) == 1:
        raise ValidationError(
            "all elements in the input are the same and zero variance"
        )


def check_if_data_is_dichotomous(y: npt.NDArray[Any]) -> None:
    is_dichotomous = set(np.unique(y)) == {0, 1}
    if not is_dichotomous:
        raise ValidationError(
            "dichotomous (binary) variable 'y' must be consist of {0, 1}"
        )


def check_length_are_same(x: npt.NDArray[Any], y: npt.NDArray[Any]) -> None:
    if len(x) != len(y):
        raise ValidationError("length of x and y must be the same")
