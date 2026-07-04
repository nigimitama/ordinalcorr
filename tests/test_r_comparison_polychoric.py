"""Compare ordinalcorr.polychoric against pre-computed R (polycor::polychor) results.

The fixtures under tests/with_r/polychoric/ (data/*.csv and results_r.csv)
are committed to the repo and regenerated via tests/with_r/run_test.sh, so
this test does not require R or Docker to run.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from ordinalcorr import polychoric

FIXTURE_DIR = Path(__file__).parent / "with_r" / "polychoric"
_results_r = pd.read_csv(FIXTURE_DIR / "results_r.csv")


def _tolerance(rho_r: float, rho_py: float) -> float:
    # Near |rho| = 1 the polychoric likelihood is nearly flat, so R and
    # ordinalcorr's optimizer can settle on noticeably different boundary
    # estimates. Allow more slack there; elsewhere require close agreement.
    if abs(rho_r) > 0.95 or abs(rho_py) > 0.95:
        return 0.15
    return 0.05


@pytest.mark.parametrize(
    "file,rho_r",
    list(_results_r[["file", "rho"]].itertuples(index=False)),
    ids=_results_r["file"].tolist(),
)
def test_matches_r_result(file, rho_r):
    df = pd.read_csv(FIXTURE_DIR / "data" / file)
    rho_py = polychoric(df["x1"], df["x2"])
    tol = _tolerance(rho_r, rho_py)
    assert np.isclose(rho_r, rho_py, atol=tol), f"{file}: R={rho_r}, Python={rho_py}"
