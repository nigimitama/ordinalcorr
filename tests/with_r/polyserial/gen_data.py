import numpy as np
import pandas as pd
from scipy.stats import multivariate_normal
from pathlib import Path

data_dir = Path("./data")


def generate_data(rho=0.5, bins=3):
    # Generate data by standard normal distribution
    n = 1000
    mean = [0, 0]
    std = [1, 1]
    cov = rho * std[0] * std[1]
    Cov = np.array([[std[0] ** 2, cov], [cov, std[1] ** 2]])
    X = multivariate_normal.rvs(mean=mean, cov=Cov, size=n, random_state=0)
    df = pd.DataFrame(X, columns=["x", "y"])
    df["y"], _ = pd.cut(df["y"], bins=bins).factorize()
    df["y"] = df["y"] + 1  # Start from 1 instead of 0
    return df


if __name__ == "__main__":
    data_dir.mkdir()

    for bins in [2, 3, 5]:
        for rho_10x in list(range(0, 11, 1)):
            rho = rho_10x / 10
            df = generate_data(rho=rho, bins=bins)
            df.to_csv(data_dir / f"normal_rho={rho:.2f}_bins={bins}.csv", index=False)
