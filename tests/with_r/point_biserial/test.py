import pandas as pd
from pathlib import Path

from ordinalcorr import point_biserial
from scipy.stats import pointbiserialr


data_dir = Path("./data")
csv_paths = data_dir.glob("*.csv")

results = []
for csv_path in sorted(csv_paths):
    df = pd.read_csv(csv_path)
    rho = point_biserial(df["x"], df["y"])
    rho_scipy, _ = pointbiserialr(df["x"], df["y"])
    results.append({"file": csv_path.name, "rho": rho, "rho_scipy": rho_scipy})

pd.DataFrame(results).to_csv("results_python.csv", index=False)
