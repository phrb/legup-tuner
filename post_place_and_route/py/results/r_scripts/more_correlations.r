repository_dir <- "/home/phrb/org/journal"

library(dplyr)
library(GGally)

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

hardware_metrics <- c("WNS", "Cycles", "FMax", "LUs", "Pins", "Regs",
                      "Blocks", "RAM", "DPS")

dir.create(paste(plot_dir, collapse = ""))

#
# Function adapted from:
#
#   https://little-book-of-r-for-multivariate-analysis.readthedocs.io/en/latest/src/multivariateanalysis.html#calculating-correlations-for-multivariate-data
#
sorted_correlations <- function(data, datapoints) {
    names(data) <- c("First.Variable", "Second.Variable","Correlation")

    #
    # Restricting comparisons to correlations that contain a hardware metric
    #
    data <- dplyr::filter(data, grepl(paste(hardware_metrics,
                                            collapse = "|"),
                                      data$Second.Variable))

    head(data[order(abs(data$Correlation), decreasing = T), ],
         n = datapoints)
}

load_data <- function(application, experiments) {
    data       <- data.frame()

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

    data  <- as.data.frame(sapply(data, as.numeric))
    return(data)
}

plot_correlations <- function(application, experiments, cor_method,
                              plot_columns) {
    data <- load_data(application, experiments)

    cormatrix <- cor(data, method = cor_method)
    diag(cormatrix) <- 0
    cormatrix[lower.tri(cormatrix)] <- 0
    cormatrix <- as.data.frame(as.table(cormatrix))

    correlation <- sorted_correlations(cormatrix, 120)

    print(paste("Generating 120 strongest correlations for '", application,
                "'...", sep = ""))

    write.csv(correlation, file = paste(paste(plot_dir, collapse = ""),
                                        paste(cor_method, "_", application,
                                              ".csv", sep = ""), sep = "/"))

    print(paste(paste("CSV generated at ", 
                      paste(plot_dir, collapse = ""),
                      sep = ""), paste(cor_method, "_", application,
                                       ".csv", sep = ""),
                sep = "/"))

    short_correlation <- correlation[1:plot_columns, ]

    print(paste("Generating scatter plots of the ",
                plot_columns, " strongest correlations for '",
                application, "'...", sep = ""))

    postscript(paste(paste(plot_dir, collapse = ""), paste(cor_method,
                                                           "_",
                                                           application,
                                                           ".eps",
                                                           sep = ""),
                     sep = "/"),
               width = 20, height = 20)
    
    columns <- unique(c(as.vector(short_correlation$First.Variable),
                        as.vector(short_correlation$Second.Variable)))

    ggpairs_plot <- ggpairs(data, columns = columns)
    
    print(ggpairs_plot)

    print(paste(paste("Plot generated at ",
                      paste(plot_dir, collapse = ""),
                      sep = ""), paste(cor_method, "_", application,
                                       ".eps", sep = ""),
                sep = "/"))

    dev.off()
    
    return(short_correlation)
}

plot_correlation_columns <- function (data, correlations, cor_method,
                                      application) {
    postscript(paste(paste(plot_dir, collapse = ""), paste(cor_method,
                                                           "_largest_",
                                                           application,
                                                           ".eps",
                                                           sep = ""),
                     sep = "/"),
               width = 20, height = 20)

    columns <- unique(c(as.vector(correlations$First.Variable),
                        as.vector(correlations$Second.Variable)))

    ggpairs_plot <- ggpairs(data, columns = columns)

    print(ggpairs_plot)

    print(paste(paste("Plot generated at ",
                      paste(plot_dir, collapse = ""),
                      sep = ""), paste(cor_method, "_largest_",
                                       application, ".eps",
                                       sep = ""),
                sep = "/"))

    dev.off()
}

application <- "dfdiv"

cor_pearson <- plot_correlations(application, experiments, "pearson", 10)
cor_spearman <- plot_correlations(application, experiments, "spearman", 10)
cor_kendall <- plot_correlations(application, experiments, "kendall", 10)

print(cor_pearson)
print(cor_spearman)
print(cor_kendall)

correlations <- inner_join(cor_pearson[c("First.Variable",
                                         "Second.Variable")],
                           cor_spearman[c("First.Variable",
                                          "Second.Variable")])

plot_correlation_columns(load_data(application, experiments), correlations,
                         "pearson_spearman", application)

correlations <- inner_join(cor_pearson[c("First.Variable",
                                         "Second.Variable")],
                           cor_kendall[c("First.Variable",
                                         "Second.Variable")])

plot_correlation_columns(load_data(application, experiments), correlations,
                         "pearson_kendall", application)

correltions <- inner_join(cor_spearman[c("First.Variable",
                                         "Second.Variable")],
                          cor_kendall[c("First.Variable",
                                        "Second.Variable")])
plot_correlation_columns(load_data(application, experiments), correlations,
                         "spearman_kendall", application)

correlations <- inner_join(inner_join(cor_pearson[c("First.Variable",
                                                    "Second.Variable")],
                                      cor_spearman[c("First.Variable",
                                                     "Second.Variable")]),
                           cor_kendall[c("First.Variable",
                                         "Second.Variable")])

plot_correlation_columns(load_data(application, experiments), correlations,
                         "pearson_spearman_kendall", application)
