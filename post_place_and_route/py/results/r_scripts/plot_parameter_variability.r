count_uniques <- function(x, n) {
  uniques <- length(unique(x))
  if (uniques >= n) {
      return(uniques)
  } else {
      return(NA)
  }
}

clear_uniques <- function(x, y) {
    uniques <- as.data.frame(y)
    return(c(x, dim(na.omit(uniques))[1]))
}

plot_uniques <- function(range, data) {
    uniques <- sapply(range,
                      function(x) clear_uniques(x, 
                                                apply(data, 2,
                                                      function(y) count_uniques(y,
                                                                                x))))
    uniques <- as.data.frame(t(uniques))
    names(uniques) <- c("Distinct.Values", "Parameters")

    ggplot(uniques, aes(x = Distinct.Values, y = Parameters)) +
          geom_point() + geom_line() +
          scale_x_continuous(breaks = seq(min(uniques$Distinct.Values),
                                          max(uniques$Distinct.Values),
                                          by = 2)) +
          scale_y_continuous(breaks = seq(min(uniques$Parameters),
                                          max(uniques$Parameters),
                                          by = 10))
}

get_parameters_with_values <- function(threshold, data) {
    uniques <- apply(data, 2, function(y) count_uniques(y, threshold))
    uniques <- na.omit(uniques)
    parameters <- names(uniques)
    return(parameters[!(parameters %in% c("MKS", "Regs", "DPS", "X"))])
}
