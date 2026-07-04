dir.create("./data", showWarnings = FALSE)

data(Orange)
write.csv(Orange, "./data/Orange.csv", row.names = FALSE)
