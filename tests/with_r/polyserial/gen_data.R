library(MASS)

data_dir <- "./data"
dir.create(data_dir, showWarnings = FALSE)

generate_data <- function(rho = 0.5, bins = 3, n = 1000, seed = 0) {
  set.seed(seed)
  std <- c(2, 1)
  cov <- rho * std[1] * std[2]
  Sigma <- matrix(c(std[1]^2, cov, cov, std[2]^2), nrow = 2)
  X <- mvrnorm(n = n, mu = c(3, 0), Sigma = Sigma)
  df <- data.frame(x = X[, 1], y = X[, 2])
  df$y <- as.integer(cut(df$y, breaks = bins, labels = FALSE)) # 1-indexed, matches cut() labels
  return(df)
}

for (bins in c(2, 3, 5)) {
  for (rho in seq(-1, 0.9, by = 0.1)) {
    df <- generate_data(rho = rho, bins = bins)
    filename <- sprintf("%s/normal_rho=%.2f_bins=%d.csv", data_dir, rho, bins)
    write.csv(df, filename, row.names = FALSE)
  }
}
