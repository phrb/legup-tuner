repository_dir <- "/home/phrb/org/journal"

load_data <- function(application, experiments, csv_dir) {
    data <- data.frame()

    for (experiment in experiments) {
        new_data <- read.csv(paste(paste(csv_dir, collapse = ""),
                                    experiment, paste(application,
                                                        ".csv",
                                                        sep = ""),
                                    sep = "/"),
                                header = TRUE, sep = ",")

        new_data <- new_data[is.finite(new_data$WNS),]
        new_data <- as.data.frame(new_data)

        if (ncol(data) == 0) {
            data <- new_data
        } else {
            data <- rbind(data, new_data)
        }
    }

    headers <- names(data)
    data    <- as.data.frame(sapply(data, as.numeric))
    data    <- t(na.omit(t(data)))
    return(as.data.frame(data))
}

csv_dir <- c(repository_dir,
             "/legup-tuner/",
             "post_place_and_route/py/results/r_scripts/",
             "data")

plot_dir <- c(repository_dir,
             "/legup-tuner/",
             "post_place_and_route/py/results/r_scripts/",
             "plots")

experiments <- c("balanced", "area", "perf", "perflat")


applications <- c("dfadd", "dfdiv", "dfmul", "sha", "motion", "adpcm",
                  "dfsin", "aes", "blowfish", "gsm", "mips")

hardware_metrics <- c("WNS", "Cycles", "FMax", "LUs", "Pins", "Regs",
                      "Blocks", "RAM", "DPS")

application <- applications[2]
data        <- load_data(application, experiments, csv_dir)

dim(data)
str(data, list.len = 999)

library(GGally)

hw_metrics    <- tail(names(data), n = 9)
hw_parameters <- head(names(data), n = 151 - 9)

dir.create(paste(plot_dir, collapse = ""))

setEPS()

postscript(paste(paste(plot_dir, collapse = ""), paste("ggpairs_",
                                                       application,
                                                       ".eps",
                                                       sep = ""),
                 sep = "/"),
           width = 16, height = 16)

ggpairs_plot <- ggpairs(data, columns = hw_metrics)

print(ggpairs_plot)

dev.off()

ggpairs_plot

my_plot <- plot(data[c(sample(hw_parameters, size = 5), hw_metrics)])

setEPS()

postscript(paste(paste(plot_dir, collapse = ""), paste("random_5_corr_",
                                                       application,
                                                       ".eps",
                                                       sep = ""),
                 sep = "/"),
           width = 16, height = 16)

plot(data[c(sample(hw_parameters, size = 5), hw_metrics)])

dev.off()

ggpairs(data[c(sample(hw_parameters, size = 5), hw_metrics)])

lm(data = head(data[!names(data) %in% (hw_metrics[hw_metrics != "FMax"])]),
   FMax ~ .)

data_bak = data

fixed_param = c()
for(i in names(data)) {
    if(dim(unique(data[i]))[1]==1) { fixed_param = c(fixed_param,i) }
}
fixed_param;
for(i in names(data)) {
    data = data[!is.na(data[,i]),]
    data = data[!is.infinite(data[,i]),]
#    data[,i]=as.numeric(data[,i])
}
data = data[!names(data) %in% (c(fixed_param,hw_metrics[hw_metrics!="FMax"]))]
dim(data)

data=data_bak
summary(lm(data=data,Regs~ set_operation_latency.signed_multiply_64))

library(ggplot2)
ggplot(data=data, aes(y=Regs, x=set_operation_latency.signed_multiply_64, color=set_operation_latency.signed_add_64)) +
    geom_jitter(aes(x=as.factor(set_operation_latency.signed_multiply_64))) +
    geom_smooth(aes(x=as.numeric(set_operation_latency.signed_multiply_64)), method="lm", formula=y~x+I(1/(x+1))) +
    theme_bw()

library(ggplot2)
ggplot(data=data, aes(y=Regs, x=set_operation_latency.signed_add_64, color=set_operation_latency.signed_multiply_64)) +
    geom_jitter(aes(x=as.factor(set_operation_latency.signed_add_64))) +
    geom_smooth(aes(x=as.numeric(set_operation_latency.signed_add_64)), method="lm", formula=y~x) +
    theme_bw()

library(ggplot2)
ggplot(data=data[data$set_operation_latency.signed_multiply_64 ==1,], aes(y=Regs, x=set_operation_latency.signed_add_64)) +
    geom_jitter(aes(x=as.factor(set_operation_latency.signed_add_64))) +
    geom_smooth(aes(x=as.numeric(set_operation_latency.signed_add_64)), method="lm", formula=y~x) +
    theme_bw()
