library(dplyr)

setEPS()

csv_dir <- c("~/code/legup-tuner/",
             "post_place_and_route/py/results/r_scripts/",
             "data")

plot_dir <- c("~/code/legup-tuner/",
             "post_place_and_route/py/results/r_scripts/",
             "scree_plots")

experiments <- c("balanced", "area", "perf", "perflat")

applications <- c("dfadd", "dfdiv", "dfmul", "sha", "motion", "adpcm",
                  "dfsin", "aes", "blowfish", "gsm", "mips")

hardware_metrics <- c("WNS", "Cycles", "FMax", "LUs", "Pins", "Regs", "Blocks",
                      "RAM", "DPS")

plot_scree_pca <- function() {
    dir.create(paste(plot_dir, collapse = ""))

    for (application in applications) {
        data <- data.frame()

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

        headers <- names(data)
        data  <- as.data.frame(sapply(data, as.numeric))

        standardised_data <- as.data.frame(scale(data[, !(names(data) %in% hardware_metrics)]))

        data.pca <- prcomp(t(na.omit(t(standardised_data))))

        print(paste("Generating scree plots of PCA for '",
                    application, "'...", sep = ""))

        postscript(paste(paste(plot_dir, collapse = ""), paste("scree_",
                                                               application,
                                                               ".eps",
                                                               sep = ""),
                         sep = "/"),
                   width = 16, height = 11)

        screeplot(data.pca, type = "lines")

        dev.off()
    }
}

plot_scree_pca()
