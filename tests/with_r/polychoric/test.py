import pandas as pd
from pathlib import Path

from ordinalcorr import polychoric_corr
from semopy.polycorr import polychoric_corr as semopy_corr


data_dir = Path("./data")
csv_paths = data_dir.glob("*.csv")

results = []
for csv_path in sorted(csv_paths):
    df = pd.read_csv(csv_path)
    rho = polychoric_corr(df["x1"], df["x2"])
    rho_semopy = semopy_corr(df["x1"], df["x2"])
    results.append({"file": csv_path.name, "rho": rho, "rho_semopy": rho_semopy})
    # print(f"{csv_path.name}: {rho:.4f}")

pd.DataFrame(results).to_csv("results_python.csv", index=False)
