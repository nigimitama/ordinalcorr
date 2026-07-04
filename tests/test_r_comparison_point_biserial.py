"""Compare ordinalcorr.point_biserial against pre-computed R results.

The fixtures under tests/with_r/point_biserial/ (data/*.csv and results_r.csv)
are committed to the repo and regenerated via tests/with_r/run_test.sh, so
this test does not require R or Docker to run.
"""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from ordinalcorr import point_biserial

FIXTURE_DIR = Path(__file__).parent / "with_r" / "point_biserial"
_results_r = pd.read_csv(FIXTURE_DIR / "results_r.csv")


@pytest.mark.parametrize(
    "file,rho_r",
    list(_results_r[["file", "rho"]].itertuples(index=False)),
    ids=_results_r["file"].tolist(),
)
def test_matches_r_result(file, rho_r):
    df = pd.read_csv(FIXTURE_DIR / "data" / file)
    rho_py = point_biserial(df["x"], df["y"])
    assert np.isclose(rho_r, rho_py, atol=0.01), f"{file}: R={rho_r}, Python={rho_py}"
