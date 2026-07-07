import warnings

import pandas as pd
import numpy as np
from ordinalcorr.polytomous import polychoric, polyserial


def hetcor(
    data: pd.DataFrame,
    n_categories: int = 20,
    n_unique: int | None = None,
    show_method: bool = False,
) -> pd.DataFrame:
    """
    Estimate the heterogeneous correlation matrix.

    The heterogeneous correlation matrix includes:

    - Pearson product-moment correlations between continuous variables
    - Polychoric correlations between ordinal variables
    - Polyserial correlations between continuous and ordinal variables

    Parameters
    ----------
    data : pd.DataFrame
        A DataFrame containing continuous and/or ordinal variables.
        Appropriate correlation coefficients are automatically selected based on the types of variables.

        - Columns with dtype `int` or `float` and number of unique values less than or equal to `n_categories`
          are treated as ordinal variables.
        - Columns with dtype `category` are treated as ordinal variables if they are ordered.

    n_categories : int, default=20
        The maximum number of unique values for an integer column to be considered ordinal.
        If the number of unique values exceeds `n_categories`, the column is treated as continuous.

    n_unique : int, optional
        Deprecated alias for `n_categories`. Will be removed in a future release.

    show_method : bool, default=False
        If True, the upper triangle of the returned matrix contains the name of the
        method used to compute each correlation (`"polychoric"`, `"polyserial"`, or
        `"pearson"`) instead of the numeric value. The diagonal and lower triangle
        remain numeric. Since the result mixes strings and floats, the returned
        DataFrame has `dtype=object` in this case.


    Returns
    -------
    pd.DataFrame
        Estimated heterogeneous correlation matrix.
        If `show_method` is True, the upper triangle holds method-name strings and
        the DataFrame has `dtype=object`.


    Examples
    --------
    >>> from ordinalcorr import hetcor
    >>> import pandas as pd
    >>> import numpy as np
    >>> np.random.seed(0)
    >>> data = pd.DataFrame({
    ...     "continuous": np.random.normal(size=90),
    ...     "ordinal_int": np.repeat([1, 2, 3], 30),
    ...     "ordinal_float": np.repeat([1.0, 2.0], 45),
    ...     "ordinal_category": pd.Series(np.repeat([1, 2, 3], 30)).astype("category").cat.as_ordered(),
    ... })
    >>> hetcor(data).round(3)
                      continuous  ordinal_int  ordinal_float  ordinal_category
    continuous             1.000       -0.257         -0.254            -0.257
    ordinal_int           -0.257        1.000          0.999             1.000
    ordinal_float         -0.254        0.999          1.000             0.999
    ordinal_category      -0.257        1.000          0.999             1.000
    >>> hetcor(data, show_method=True).round(3)
                     continuous ordinal_int ordinal_float ordinal_category
    continuous              1.0  polyserial    polyserial       polyserial
    ordinal_int       -0.257389         1.0    polychoric       polychoric
    ordinal_float     -0.253566    0.998635           1.0       polychoric
    ordinal_category  -0.257389    0.999996      0.998647              1.0
    """
    # NOTE: np.ndarray uses single dtype, so it cannot be a input. so we accept pd.DataFrame only
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Input data must be a pandas.DataFrame")

    if n_unique is not None:
        warnings.warn(
            "The `n_unique` parameter is deprecated and will be removed in a "
            "future release. Use `n_categories` instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        n_categories = n_unique

    is_ordinal = is_cols_ordinal(data, n_categories=n_categories)

    ncols = len(data.columns)
    corr = np.zeros((ncols, ncols), dtype=float)
    method = np.empty((ncols, ncols), dtype=object)
    for i in range(ncols):
        for j in range(i, ncols):
            if i == j:
                corr[i, j] = 1.0
                continue

            if is_ordinal[i] and is_ordinal[j]:
                corr[i, j] = polychoric(data.iloc[:, i], data.iloc[:, j])
                method[i, j] = "polychoric"

            if is_ordinal[i] and not is_ordinal[j]:
                ordinal = data.iloc[:, i]
                continuous = data.iloc[:, j]
                corr[i, j] = polyserial(continuous, ordinal)
                method[i, j] = "polyserial"

            if not is_ordinal[i] and is_ordinal[j]:
                continuous = data.iloc[:, i]
                ordinal = data.iloc[:, j]
                corr[i, j] = polyserial(continuous, ordinal)
                method[i, j] = "polyserial"

            if not is_ordinal[i] and not is_ordinal[j]:
                from scipy.stats import pearsonr

                corr[i, j] = pearsonr(data.iloc[:, i], data.iloc[:, j]).statistic
                method[i, j] = "pearson"

            corr[j, i] = corr[i, j]

    if show_method:
        corr_obj = corr.astype(object)
        for i in range(ncols):
            for j in range(i + 1, ncols):
                corr_obj[i, j] = method[i, j]
        return pd.DataFrame(corr_obj, index=data.columns, columns=data.columns)

    corr_df = pd.DataFrame(corr, index=data.columns, columns=data.columns)
    return corr_df


def is_cols_ordinal(data: pd.DataFrame, n_categories: int) -> list[bool]:
    """Check if the columns of the DataFrame are ordinal."""
    return [
        is_col_ordinal(x=data.iloc[:, j], n_categories=n_categories)
        for j in range(len(data.columns))
    ]


def is_col_ordinal(x: pd.Series, n_categories: int) -> bool:
    """Check if the input is ordinal."""

    if x.dtype.name == "category":
        if x.cat.ordered:
            return True
        raise TypeError(f"The column '{x.name}' is unoredered category.")

    # Judge by the number of unique values, even if the data type is 'float'
    if x.unique().size <= n_categories:
        return True

    return False
