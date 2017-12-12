repository_dir <- "/home/phrb/org/journal"

library(dplyr)

csv_dir <- c(repository_dir,
             "/legup-tuner/",
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

    new_data       <- as.data.frame(new_data)
    new_clean_data <- new_data[is.finite(new_data$WNS),]

    if (ncol(data) == 0) {
        data <- new_data
    } else {
        data <- rbind(data, new_data)
    }

    if (ncol(clean_data) == 0) {
        clean_data <- new_clean_data
    } else {
        clean_data <- rbind(clean_data, new_clean_data)
    }
}

names <- c("WNS","RAM")

idx <- match(names, names(data))

print("Data with 'WNS == Inf' rows:")

print("Mean:")
sapply(data[idx[1]:idx[2]], mean)

print("Standard Deviation:")
sapply(data[idx[1]:idx[2]], sd)

print("Data without 'WNS == Inf' rows:")

print("Mean:")
sapply(clean_data[idx[1]:idx[2]], mean)

print("Standard Deviation:")
sapply(clean_data[idx[1]:idx[2]], sd)
