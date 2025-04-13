library(polycor)

csv_paths <- list.files(path = "./data", pattern = "\\.csv$", full.names = TRUE)
results <- list()
for (path in sort(csv_paths)) {
  data <- read.csv(path)
  
  x <- data$x
  y <- as.ordered(data$y)
  rho <- polyserial(x, y)
  
  # 結果を保存
  results[[length(results) + 1]] <- data.frame(
    file = basename(path),
    rho = rho
  )
}
# リストを1つのデータフレームにまとめてCSVに保存
final_df <- do.call(rbind, results)
write.csv(final_df, file = "results_r.csv", row.names = FALSE)
