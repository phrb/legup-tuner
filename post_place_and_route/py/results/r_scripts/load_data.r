repository_dir <- "/home/phrb/org/journal"

library(dplyr)
library(tidyr)
library(GGally)
library(plotly)

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

load_data <- function(application, experiments, removed_columns) {
    data <- data.frame()

    for (experiment in experiments) {
        new_data <- read.csv(paste(paste(csv_dir, collapse = ""),
                                   experiment, paste(application,
                                                     ".csv",
                                                     sep = ""),
                                   sep = "/"),
                             header = TRUE, sep = ",")

        new_data <- as.data.frame(new_data)

        new_data["experiment"] <- rep(experiment, nrow(new_data))

        if (ncol(data) == 0) {
            data <- new_data
        } else {
            data <- rbind(data, new_data)
        }
    }

    data <- as.data.frame(data)
    data <- data %>% drop_na()
    data <- data[is.finite(data$WNS),]
    data <- data %>% mutate(MKS = (Cycles / (1000 * FMax)))
    data <- select(data, -one_of(removed_columns))
    return(data)
}
