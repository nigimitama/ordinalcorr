class ValidationError(Exception):
    pass


def check_if_zero_variance(x):
    if len(set(x)) == 1:
        raise ValidationError(
            "all elements in the input are the same and zero variance"
        )
