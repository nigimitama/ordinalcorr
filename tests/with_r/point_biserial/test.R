# Point-biserial correlation, computed with the same formula as
# ltm::biserial.cor(x, y, level = 2) (verified against its source):
#   diff.mu * sqrt(prob * (1 - prob)) / sd.pop
point_biserial_cor <- function(x, y) {
  y <- as.factor(y)
  levs <- levels(y)
  ind <- y == levs[2]
  diff.mu <- mean(x[ind]) - mean(x[!ind])
  prob <- mean(ind)
  sd.pop <- sd(x) * sqrt((length(x) - 1) / length(x))
  diff.mu * sqrt(prob * (1 - prob)) / sd.pop
}

csv_paths <- list.files(path = "./data", pattern = "\\.csv$", full.names = TRUE)
results <- list()
for (path in sort(csv_paths)) {
  data <- read.csv(path)

  x <- data$x
  y <- data$y
  rho <- point_biserial_cor(x, y)

  # 結果を保存
  results[[length(results) + 1]] <- data.frame(
    file = basename(path),
    rho = rho
  )
}
# リストを1つのデータフレームにまとめてCSVに保存
final_df <- do.call(rbind, results)
write.csv(final_df, file = "results_r.csv", row.names = FALSE)
