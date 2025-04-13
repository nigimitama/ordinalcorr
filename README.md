# ordinalcorr: correlation coefficients for ordinal variables

[![PyPI version](https://img.shields.io/pypi/v/ordinalcorr.svg)](https://pypi.org/project/ordinalcorr/)
![License](https://img.shields.io/pypi/l/ordinalcorr)
[![Unit Tests](https://github.com/nigimitama/ordinalcorr/actions/workflows/test.yml/badge.svg)](https://github.com/nigimitama/ordinalcorr/actions/workflows/test.yml)

A Python package for computing correlation coefficients designed for **ordinal-scale data** (e.g., Likert items). Supports polychoric correlation and other ordinal association measures.

## 📦 Installation

```bash
pip install ordinalcorr
```

## 📘 Features

### Polychoric correlation

Compute correlation coefficient between two ordinal variables

```python
from ordinalcorr import polychoric_corr

x = [1, 1, 2, 2, 3, 3]
y = [0, 0, 0, 1, 1, 1]

rho = polychoric_corr(x, y)
print(f"Polychoric correlation: {rho:.3f}")
```

### Polyserial correlation

Compute correlation coefficient between continuous variable and ordinal variable

```python
from ordinalcorr import polyserial_corr

x = [0.1, 0.1, 0.2, 0.2, 0.3, 0.3]
y = [0, 0, 0, 1, 1, 2]

rho = polyserial_corr(x, y)
print(f"Polyserial correlation: {rho:.3f}")
```
