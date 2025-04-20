import numpy as np
import pandas as pd


print(
    f"""
# ----------------------------------------
# Polychoric
# ----------------------------------------
R vs Python results:

"""
)


res_r = pd.read_csv("results_r.csv")
res_py = pd.read_csv("results_python.csv")

print("R results:")
print(res_r)
print("\nPython results:")
print(res_py)


diff = res_r - res_py
print("\nDifference:")
print(diff)

print("\nisClose:")
print(diff.abs() < 0.01)
