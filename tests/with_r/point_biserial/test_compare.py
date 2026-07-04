import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from ordinalcorr import point_biserial

HERE = Path(__file__).parent
DATA_DIR = HERE / "data"

pytestmark = pytest.mark.skipif(
    shutil.which("Rscript") is None, reason="Rscript is not available"
)


@pytest.fixture(scope="module")
def results_r() -> pd.DataFrame:
    """Generate test data, estimate rho with the R package 'ltm', and return the results."""
    if not DATA_DIR.exists():
        subprocess.run([sys.executable, "gen_data.py"], cwd=HERE, check=True)
    try:
        subprocess.run(
            ["Rscript", "test.R"], cwd=HERE, check=True, capture_output=True, text=True
        )
    except subprocess.CalledProcessError as e:
        pytest.skip(f"Rscript failed (is the R package 'ltm' installed?): {e.stderr}")
    return pd.read_csv(HERE / "results_r.csv")


def test_point_biserial_matches_r(results_r: pd.DataFrame):
    tol = 0.01
    for _, row in results_r.iterrows():
        df = pd.read_csv(DATA_DIR / row["file"])
        rho_py = point_biserial(df["x"], df["y"])
        assert np.isclose(rho_py, row["rho"], atol=tol), (
            f"{row['file']}: python={rho_py:.4f}, R={row['rho']:.4f}"
        )
