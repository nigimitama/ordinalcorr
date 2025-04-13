import pandas as pd
from pathlib import Path

from ordinalcorr import polyserial_corr
from semopy.polycorr import polyserial_corr as semopy_corr


data_dir = Path("./data")
csv_paths = data_dir.glob("*.csv")

results = []
for csv_path in sorted(csv_paths):
    df = pd.read_csv(csv_path)
    rho = polyserial_corr(df["x"], df["y"])
    rho_semopy = semopy_corr(df["x"], df["y"])
    results.append({"file": csv_path.name, "rho": rho, "rho_semopy": rho_semopy})

pd.DataFrame(results).to_csv("results_python.csv", index=False)
