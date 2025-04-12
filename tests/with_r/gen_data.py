import numpy as np
import pandas as pd
from scipy.stats import multivariate_normal
from pathlib import Path

data_dir = Path("./data")
data_dir.mkdir()


# 標準正規分布
def generate_data(rho=0.5):
    n = 1000
    mean = [0, 0]
    std = [1, 1]
    cov = rho * std[0] * std[1]
    Cov = np.array([[std[0] ** 2, cov], [cov, std[1] ** 2]])
    X = multivariate_normal.rvs(mean=mean, cov=Cov, size=n, random_state=0)
    df = pd.DataFrame(X, columns=["x1", "x2"])
    for col in df.columns:
        df[col], _ = pd.cut(df[col], bins=3).factorize()
    return df


if __name__ == "__main__":
    for rho_10x in list(range(0, 11, 1)):
        rho = rho_10x / 10
        df = generate_data(rho=rho)
        df.to_csv(data_dir / f"normal_rho={rho:.2f}.csv", index=False)
