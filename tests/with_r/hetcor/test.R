library(polycor)

csv_path = "./data/Orange.csv"
data <- read.csv(csv_path)
result <- hetcor(data)
corr = result$correlations
write.csv(corr, file = "results_r.csv", row.names = FALSE)
