import shutil
import subprocess
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from ordinalcorr import hetcor

HERE = Path(__file__).parent
DATA_DIR = HERE / "data"

pytestmark = pytest.mark.skipif(
    shutil.which("Rscript") is None, reason="Rscript is not available"
)


@pytest.fixture(scope="module")
def results_r() -> pd.DataFrame:
    """Generate test data, estimate the correlation matrix with the R package 'polycor', and return the results."""
    if not (DATA_DIR / "Orange.csv").exists():
        DATA_DIR.mkdir(exist_ok=True)
        subprocess.run(["Rscript", "gen_data.R"], cwd=HERE, check=True)
    try:
        subprocess.run(
            ["Rscript", "test.R"], cwd=HERE, check=True, capture_output=True, text=True
        )
    except subprocess.CalledProcessError as e:
        pytest.skip(f"Rscript failed (is the R package 'polycor' installed?): {e.stderr}")
    return pd.read_csv(HERE / "results_r.csv")


def test_hetcor_matches_r(results_r: pd.DataFrame):
    tol = 0.01
    df = pd.read_csv(DATA_DIR / "Orange.csv")
    actual = hetcor(df).to_numpy()
    expected = results_r.to_numpy()
    assert np.isclose(actual, expected, atol=tol).all(), (
        f"python:\n{actual}\nR:\n{expected}"
    )
