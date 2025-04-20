import pandas as pd
import numpy as np
from ordinalcorr.polytomous import polychoric, polyserial


def hetcor(data: pd.DataFrame, n_unique: int = 20) -> pd.DataFrame:
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

        - Columns with dtype `float` are treated as continuous variables.
        - Columns with dtype `int` and number of unique values less than or equal to `n_unique`
          are treated as ordinal variables.
        - Columns with dtype `category` are treated as ordinal variables if they are ordered.

    n_unique : int, default=20
        The maximum number of unique values for an integer column to be considered ordinal.
        If the number of unique values exceeds `n_unique`, the column is treated as continuous.


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
    >>> hetcor(data)
    """
    # NOTE: np.ndarray uses single dtype, so it cannot be a input. so we accept pd.DataFrame only
    if not isinstance(data, pd.DataFrame):
        raise TypeError("Input data must be a pandas.DataFrame")

    is_col_ordinal = is_cols_ordinal(data, n_unique=n_unique)

    ncols = len(data.columns)
    corr = np.zeros((ncols, ncols), dtype=float)
    for i in range(ncols):
        for j in range(i, ncols):
            if i == j:
                corr[i, j] = 1.0
                continue

            if is_col_ordinal[i] and is_col_ordinal[j]:
                corr[i, j] = polychoric(data.iloc[:, i], data.iloc[:, j])

            if is_col_ordinal[i] and not is_col_ordinal[j]:
                ordinal = data.iloc[:, i]
                continuous = data.iloc[:, j]
                corr[i, j] = polyserial(continuous, ordinal)

            if not is_col_ordinal[i] and is_col_ordinal[j]:
                continuous = data.iloc[:, i]
                ordinal = data.iloc[:, j]
                corr[i, j] = polyserial(continuous, ordinal)

            if not is_col_ordinal[i] and not is_col_ordinal[j]:
                from scipy.stats import pearsonr

                corr[i, j] = pearsonr(data.iloc[:, i], data.iloc[:, j]).statistic

            corr[j, i] = corr[i, j]
    corr_df = pd.DataFrame(corr, index=data.columns, columns=data.columns)
    return corr_df


def is_cols_ordinal(data: pd.DataFrame, n_unique: int) -> list[bool]:
    """Check if the columns of the DataFrame are ordinal."""
    results = [None] * len(data.columns)
    for j in range(len(data.columns)):
        results[j] = is_col_ordinal(x=data.iloc[:, j], n_unique=n_unique)
    return results


def is_col_ordinal(x: pd.Series, n_unique: int) -> bool:
    """Check if the input is ordinal."""
    if "int" in x.dtype.name.lower() and x.unique().size <= n_unique:
        return True

    if x.dtype.name == "category":
        if x.cat.ordered:
            return True
        raise TypeError(f"The column '{x.name}' is unoredered category.")

    return False
