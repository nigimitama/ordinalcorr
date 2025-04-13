import numpy as np
import pandas as pd

results_r = pd.read_csv("results_r.csv")
results_py = pd.read_csv("results_python.csv")
results = pd.merge(results_r, results_py, on="file", suffixes=("_r", "_py"))
results["diff"] = results["rho_r"] - results["rho_py"]

tol = 0.01
results["is_close"] = np.isclose(results["rho_r"], results["rho_py"], atol=tol)
n_close = results["is_close"].sum()


print(
    f"""
# ----------------------------------------
# Polychoric
# ----------------------------------------
R vs Python results:

{results}

{n_close} out of {len(results)} results are close (within {tol}) to each other.
"""
)
