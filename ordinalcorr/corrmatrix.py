import warnings

import pandas as pd
import numpy as np
from ordinalcorr.polytomous import polychoric, polyserial


def hetcor(
    data: pd.DataFrame,
    n_categories: int = 20,
    n_unique: int | None = None,
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


    Returns
    -------
    pd.DataFrame
        Estimated heterogeneous correlation matrix.


    Examples
    --------
    >>> from ordinalcorr import hetcor
    >>> import pandas as pd
    >>> data = pd.DataFrame({
    ...     "continuous": [0.1, 0.1, 0.2, 0.2, 0.3, 0.3],
    ...     "ordinal": [0, 0, 0, 1, 1, 2],
    ... })
    >>> hetcor(data).round(4)
                continuous  ordinal
    continuous      1.0000   0.9984
    ordinal         0.9984   1.0000
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
    for i in range(ncols):
        for j in range(i, ncols):
            if i == j:
                corr[i, j] = 1.0
                continue

            if is_ordinal[i] and is_ordinal[j]:
                corr[i, j] = polychoric(data.iloc[:, i], data.iloc[:, j])

            if is_ordinal[i] and not is_ordinal[j]:
                ordinal = data.iloc[:, i]
                continuous = data.iloc[:, j]
                corr[i, j] = polyserial(continuous, ordinal)

            if not is_ordinal[i] and is_ordinal[j]:
                continuous = data.iloc[:, i]
                ordinal = data.iloc[:, j]
                corr[i, j] = polyserial(continuous, ordinal)

            if not is_ordinal[i] and not is_ordinal[j]:
                from scipy.stats import pearsonr

                corr[i, j] = pearsonr(data.iloc[:, i], data.iloc[:, j]).statistic

            corr[j, i] = corr[i, j]
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
