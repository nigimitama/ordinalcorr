# ordinalcorr: correlation coefficients for ordinal variables

[![PyPI version](https://img.shields.io/pypi/v/ordinalcorr.svg)](https://pypi.org/project/ordinalcorr/)
![License](https://img.shields.io/pypi/l/ordinalcorr)
[![Unit Tests](https://github.com/nigimitama/ordinalcorr/actions/workflows/test.yml/badge.svg)](https://github.com/nigimitama/ordinalcorr/actions/workflows/test.yml)

A Python package for computing correlation coefficients designed for **ordinal-scale data** (e.g., Likert items). Supports polychoric correlation and other ordinal association measures.

## 📦 Installation

```bash
pip install ordinalcorr
```

## ✨ Features

This package provides several correlation coefficients for many types of variables

| Variable X | Variable Y                           | Method                     | Function              |
| ---------- | ------------------------------------ | -------------------------- | --------------------- |
| binary     | binary                               | Tetrachoric correlation    | `tetrachoric_corr`    |
| ordinal    | ordinal                              | Polychoric correlation     | `polychoric_corr`     |
| continuous | ordinal                              | Polyserial correlation     | `polyserial_corr`     |
| continuous | binary (discretized from continuous) | Biserial correlation       | `biserial_corr`       |
| continuous | binary                               | Point-Biserial correlation | `point_biserial_corr` |

### Example

Here is an example for computing correlation coefficient between two ordinal variables

```python
from ordinalcorr import polychoric_corr

x = [1, 1, 2, 2, 3, 3]
y = [0, 0, 0, 1, 1, 1]

rho = polychoric_corr(x, y)
print(f"Polychoric correlation: {rho:.3f}")
```

## 📒 Document

[Full document is here](https://nigimitama.github.io/ordinalcorr/index.html)

## ⚖️ License

[MIT License](./LICENSE)
