"""Compare ordinalcorr.hetcor against a pre-computed R (polycor::hetcor) result.

The fixtures under tests/with_r/hetcor/ (data/Orange.csv and results_r.csv)
are committed to the repo and regenerated via tests/with_r/run_test.sh, so
this test does not require R or Docker to run.
"""

from pathlib import Path

import numpy as np
import pandas as pd

from ordinalcorr import hetcor

FIXTURE_DIR = Path(__file__).parent / "with_r" / "hetcor"


def test_matches_r_result():
    df = pd.read_csv(FIXTURE_DIR / "data" / "Orange.csv")
    corr_py = hetcor(df)

    corr_r = pd.read_csv(FIXTURE_DIR / "results_r.csv")
    corr_r.index = corr_py.index

    assert np.isclose(
        corr_py.values, corr_r.values, atol=0.02
    ).all(), f"R:\n{corr_r}\n\nPython:\n{corr_py}"
