repository_dir <- "/home/phrb/org/journal"

library(dplyr)

setEPS()

csv_dir <- c(repository_dir,
             "/legup-tuner/",
             "post_place_and_route/py/results/r_scripts/",
             "data")

plot_dir <- c(repository_dir,
              "/legup-tuner/",
              "post_place_and_route/py/results/r_scripts/",
              "correlations")

experiments <- c("balanced", "area", "perf", "perflat")

applications <- c("dfadd", "dfdiv", "dfmul", "sha", "motion", "adpcm",
                  "dfsin", "aes", "blowfish", "gsm", "mips")

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

    #
    # Restricting comparisons to correlations that contain a hardware metric
    #
    fm <- dplyr::filter(fm, grepl(paste(hardware_metrics, collapse = "|"),
                                  fm$Second.Variable))

    head(fm[order(abs(fm$Correlation), decreasing = T), ], n = datapoints)
}

plot_application_correlations <- function() {
    dir.create(paste(plot_dir, collapse = ""))

    for (application in applications) {
        data       <- data.frame()
        clean_data <- data.frame()

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

        data  <- sapply(data, as.numeric)

        correlation <- sorted_correlations(data, 120)

        print(paste("Generating 120 strongest correlations for '", application,
                    "'...", sep = ""))

        write.csv(correlation, file = paste(paste(plot_dir, collapse = ""),
                                            paste("correlations_", application,
                                                  ".csv", sep = ""), sep = "/"))
        print(paste("Generating scatter plots of the 30 strongest correlations for '",
                    application, "'...", sep = ""))

        print(paste(paste("CSV generated at ", 
                          paste(plot_dir, collapse = ""),
                          sep = ""), paste("correlations_", application,
                                           ".csv", sep = ""),
                    sep = "/"))

        short_correlation <- correlation[1:30, ]

        postscript(paste(paste(plot_dir, collapse = ""), paste("correlations_",
                                                               application,
                                                               ".eps",
                                                               sep = ""),
                         sep = "/"),
                   width = 16, height = 11)

        old.par <- par(mfrow = c(5, 6))

        for (i in 1:nrow(short_correlation)) {
            first  <- as.character(short_correlation[i, 'First.Variable'])
            second <- as.character(short_correlation[i, 'Second.Variable'])

            plot(data[, first], data[, second], xlab = first, ylab = second)
        }

        print(paste(paste("Plot generated at ",
                          paste(plot_dir, collapse = ""),
                          sep = ""), paste("correlations_", application,
                                           ".eps", sep = ""),
                    sep = "/"))

        par(old.par)
        dev.off()
    }
}

plot_application_correlations()
