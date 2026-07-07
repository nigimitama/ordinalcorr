# ordinalcorr: correlation coefficients for ordinal variables

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ordinalcorr)](https://pypi.org/project/ordinalcorr/)
[![PyPI version](https://img.shields.io/pypi/v/ordinalcorr.svg)](https://pypi.org/project/ordinalcorr/)
[![License](https://img.shields.io/pypi/l/ordinalcorr)](https://github.com/nigimitama/ordinalcorr/blob/main/LICENSE)

`ordinalcorr` is a Python package designed to compute correlation coefficients tailored for ordinal-scale data (e.g., Likert items).
It supports polychoric correlation coefficients and other coefficients for ordinal data.

## ✨ Features

### 1️⃣ Correlation Coefficients

This package provides several correlation coefficients (e.g. Polyserial and Polychoric)

| Variable X            | Variable Y            | Method                 | Function     |
| --------------------- | --------------------- | ---------------------- | ------------ |
| continuous            | ordinal (discretized) | Polyserial correlation | `polyserial` |
| ordinal (discretized) | ordinal (discretized) | Polychoric correlation | `polychoric` |

Here is an example:

```python
>>> from ordinalcorr import polychoric
>>> x = [1, 1, 2, 2, 3, 3]
>>> y = [0, 0, 0, 1, 1, 1]
>>> polychoric(x, y)
0.9986287922233864
```

### 2️⃣ Heterogeneous Correlation Matrix

A function for computing the _heterogeneous correlation matrix_—a correlation matrix that includes both continuous and ordinal variables—is also provided.

```python
>>> from ordinalcorr import hetcor
>>> import pandas as pd
>>> import numpy as np
>>> np.random.seed(0)
>>> data = pd.DataFrame({
...     "continuous": np.random.normal(size=90),
...     "dichotomous": np.repeat([0, 1], 45),
...     "polytomous": np.repeat([1, 2, 3], 30),
... })
>>> hetcor(data).round(3)
             continuous  dichotomous  polytomous
continuous        1.000       -0.254      -0.257
dichotomous      -0.254        1.000       0.999
polytomous       -0.257        0.999       1.000
```

## 📦 Installation

ordinalcorr is available at the [PyPI](https://pypi.org/project/ordinalcorr/)

```bash
pip install ordinalcorr
```

### Requirements

- Python 3.10 or later
- Dependencies:
  - numpy >= 1.23.0
  - scipy >= 1.8.0

## 📒 Documentation

[ordinalcorr documentation](https://nigimitama.github.io/ordinalcorr/index.html)

## ⚖️ License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
