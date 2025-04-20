import pandas as pd
from ordinalcorr import hetcor

csv_path = "./data/Orange.csv"
df = pd.read_csv(csv_path)

pd.DataFrame(hetcor(df)).to_csv("results_python.csv", index=False)
