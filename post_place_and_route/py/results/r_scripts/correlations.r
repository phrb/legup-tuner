library(dplyr)

setEPS()
postscript("correlations.eps", width = 16, height = 11)

#
# Function adapted from:
#
#   https://little-book-of-r-for-multivariate-analysis.readthedocs.io/en/latest/src/multivariateanalysis.html#calculating-correlations-for-multivariate-data
#
sorted_correlations <- function(data, datapoints) {
    cormatrix <- cor(data)

    diag(cormatrix) <- 0
    cormatrix[lower.tri(cormatrix)] <- 0

    fm <- as.data.frame(as.table(cormatrix))

    names(fm) <- c("First.Variable", "Second.Variable","Correlation")

    hardware_metrics <- c("WNS", "Cycles", "FMax", "LUs", "Pins", "Regs",
                          "Blocks", "RAM", "DPS")

    fm <- dplyr::filter(fm, grepl(paste(hardware_metrics, collapse = "|"),
                                  fm$Second.Variable))

    head(fm[order(abs(fm$Correlation), decreasing = T), ], n = datapoints)
}

csv_dir <- c("~/code/legup-tuner/",
             "post_place_and_route/py/results/r_scripts/",
             "data")

experiments <- c("balanced", "area", "perf", "perflat")

applications <- c("dfadd", "dfdiv", "dfmul", "sha", "motion", "adpcm",
                  "dfsin", "aes", "blowfish", "gsm", "mips")

data       <- data.frame()
clean_data <- data.frame()

application <- applications[2]

for (experiment in experiments) {
    new_data <- read.csv(paste(paste(csv_dir, collapse = ""),
                               experiment, paste(application,
                                                 ".csv",
                                                 sep = ""),
                               sep = "/"),
                         header = TRUE, sep = ",")

    new_data <- as.data.frame(new_data)
    new_data <- new_data[is.finite(new_data$WNS),]

    if (ncol(data) == 0) {
        data <- new_data
    } else {
        data <- rbind(data, new_data)
    }
}

names <- c("WNS","RAM")
idx   <- match(names, names(data))
data  <- sapply(data, as.numeric)

correlation <- sorted_correlations(data, 120)

print("120 Largest Correlations:")
#print(correlation)

print("Scatter Plots of the 10 Largest Correlations")
short_correlation <- correlation[1:30, ]

old.par <- par(mfrow = c(5, 6))

for (i in 1:nrow(short_correlation)) {
    first  <- as.character(short_correlation[i, 'First.Variable'])
    second <- as.character(short_correlation[i, 'Second.Variable'])

    plot(data[, first], data[, second], xlab = first, ylab = second)
}

par(old.par)
dev.off()
