import numpy as np
import pandas as pd

results_r = pd.read_csv("results_r.csv")
results_py = pd.read_csv("results_python.csv")
results = pd.merge(results_r, results_py, on="file", suffixes=("_r", "_py"))
results["diff"] = results["rho_r"] - results["rho_py"]
results["is_close"] = np.isclose(results["rho_r"], results["rho_py"], atol=0.001)

print(
    f"""
# ----------------------------------------
# Polyserial
# ----------------------------------------
R vs Python results:

{results}
"""
)
