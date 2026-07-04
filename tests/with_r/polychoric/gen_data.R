library(MASS)

data_dir <- "./data"
dir.create(data_dir, showWarnings = FALSE)

generate_data <- function(rho = 0.5, bins = 3, n = 1000, seed = 0) {
  set.seed(seed)
  Sigma <- matrix(c(1, rho, rho, 1), nrow = 2)
  X <- mvrnorm(n = n, mu = c(0, 0), Sigma = Sigma)
  df <- data.frame(x1 = X[, 1], x2 = X[, 2])
  for (col in c("x1", "x2")) {
    df[[col]] <- as.integer(cut(df[[col]], breaks = bins, labels = FALSE)) - 1
  }
  return(df)
}

for (bins in c(2, 3, 5)) {
  for (rho in seq(-1, 0.9, by = 0.1)) {
    df <- generate_data(rho = rho, bins = bins)
    filename <- sprintf("%s/normal_rho=%.2f_bins=%d.csv", data_dir, rho, bins)
    write.csv(df, filename, row.names = FALSE)
  }
}
