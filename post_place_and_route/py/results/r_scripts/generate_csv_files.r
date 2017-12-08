library(dplyr)
library(tidyr)
library(jsonlite)

runs         <- 10
tuning_time  <- 5400

repository   <- "~/code/legup-tuner"
results      <- "post_place_and_route/py/results"

output_dir   <- paste(repository, results, "r_scripts/data", sep = "/")

experiments  <- c("default_stratixV_perf", "default_stratixV_perflat",
                  "default_stratixV_area", "default_stratixV_balanced")

applications <- c("dfadd", "dfdiv", "dfmul", "sha", "motion", "adpcm",
                  "dfsin", "aes", "blowfish", "gsm", "mips")

txt_measurements <- c("log_details.txt", "best_cycles_log.txt",
                      "best_fmax_log.txt", "best_lu_log.txt",
                      "best_pins_log.txt", "best_regs_log.txt",
                      "best_block_log.txt", "best_ram_log.txt",
                      "best_dps_log.txt")

json_configurations <- "best_log.json"

headers <- c("WNS", "Cycles", "FMax", "LUs", "Pins", "Regs", "Blocks", "RAM",
             "DPS")

#
# This function merges columns and fills missing rows with 'NA'.
# This happens in this dataset because of unsynchronized logging,
# where the last configuration was saved twice in one of the log
# files. Will require to later clean the lines with 'NA's.
#
# Function from:
#
#    https://stackoverflow.com/questions/7962267/cbind-a-df-with-an-empty-df-cbind-fill
#
#
cbind.fill <- function(...){
    nm <- list(...)
    nm <- lapply(nm, as.matrix)
    n <- max(sapply(nm, nrow))
    do.call(cbind, lapply(nm, function (x)
        rbind(x, matrix(, n-nrow(x), ncol(x)))))
}

dir.create(output_dir)

for (experiment in experiments) {
    dir.create(paste(output_dir, strsplit(experiment, "_")[[1]][3], sep = "/"))

    for (application in applications) {
        data <- data.frame()

        for (iteration in 1:runs) {
            target_file <- (paste(repository, results, experiment,
                                  paste(application, tuning_time, iteration,
                                        sep = "_"), json_configurations,
                                  sep = "/"))

            if (file.exists(target_file)) {
                configuration <- fromJSON(target_file)
            }

            columns <- data.frame()

            for (measurement in txt_measurements) {
                target_file <- paste(repository, results, experiment,
                                     paste(application, tuning_time, iteration,
                                           sep = "_"), measurement,
                                     sep = "/")

                if (file.exists(target_file)) {
                    new_column <- read.table(target_file, header = FALSE)[2]

                    if (ncol(columns) == 0) {
                        columns <- new_column
                    } else {
                        columns = cbind.fill(columns, new_column)
                    }
                }
            }

            if (ncol(columns) != 0) {
                colnames(columns) <- headers

                columns = cbind.fill(configuration, columns)

                if (nrow(data) == 0) {
                    data <- columns
                } else {
                    data = bind_rows(as.data.frame(data),
                                     as.data.frame(columns))
                }
            }
        }

        data <- data[complete.cases(data), ]

        write.csv(data, file = paste(paste(output_dir, strsplit(experiment,
                                                                "_")[[1]][3],
                                           application, sep = "/"), ".csv",
                                     sep = ""))
    }
}
