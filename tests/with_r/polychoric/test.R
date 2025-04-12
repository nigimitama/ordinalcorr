library(polycor)

csv_paths <- list.files(path = "./data", pattern = "\\.csv$", full.names = TRUE)
results <- list()
for (path in sort(csv_paths)) {
  data <- read.csv(path)
  
  # polychor() のために ordered factor に変換
  x1 <- as.ordered(data$x1)
  x2 <- as.ordered(data$x2)
  rho <- polychor(x1, x2)
  # cat(basename(path), sprintf("rho = %.4f\n", rho))
  
  # 結果を保存
  results[[length(results) + 1]] <- data.frame(
    file = basename(path),
    rho = rho
  )
}
# リストを1つのデータフレームにまとめてCSVに保存
final_df <- do.call(rbind, results)
write.csv(final_df, file = "results_r.csv", row.names = FALSE)
