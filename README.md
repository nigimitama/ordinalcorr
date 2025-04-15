# ordinalcorr: correlation coefficients for ordinal variables

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ordinalcorr)](https://pypi.org/project/ordinalcorr/)
[![PyPI version](https://img.shields.io/pypi/v/ordinalcorr.svg)](https://pypi.org/project/ordinalcorr/)
[![License](https://img.shields.io/pypi/l/ordinalcorr)](https://github.com/nigimitama/ordinalcorr/blob/main/LICENSE)

`ordinalcorr` is a Python package designed to compute correlation coefficients tailored for ordinal-scale data (e.g., Likert items).
It supports polychoric correlation coefficients and other coefficients for ordinal data.

## 📦 Installation

```bash
pip install ordinalcorr
```

## ✨ Features

This package provides several correlation coefficients for many types of variables

| Variable X            | Variable Y            | Method                     | Function         |
| --------------------- | --------------------- | -------------------------- | ---------------- |
| binary (discretized)  | binary (discretized)  | Tetrachoric correlation    | `tetrachoric`    |
| ordinal (discretized) | ordinal (discretized) | Polychoric correlation     | `polychoric`     |
| continuous            | ordinal (discretized) | Polyserial correlation     | `polyserial`     |
| continuous            | binary (discretized)  | Biserial correlation       | `biserial`       |
| continuous            | binary                | Point-Biserial correlation | `point_biserial` |

### Example

Here is an example for computing correlation coefficient between two ordinal variables

```python
from ordinalcorr import polychoric

x = [1, 1, 2, 2, 3, 3]
y = [0, 0, 0, 1, 1, 1]

rho = polychoric(x, y)
print(f"Polychoric correlation: {rho:.3f}")
```

## 📒 Document

[Full document is here](https://nigimitama.github.io/ordinalcorr/index.html)

## ⚖️ License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.
