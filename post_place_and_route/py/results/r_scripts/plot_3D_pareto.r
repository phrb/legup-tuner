plot_3D_pareto <- function(data) {
    criterion <- low(MKS) * low(Regs) * low(DPS)

    pareto <- psel(data, criterion, top = nrow(data)) 

    pareto <- pareto[with(pareto, order(X)), ]

    p <- plot_ly(pareto, x = ~MKS, y = ~Regs, z = ~DPS, color = ~(.level == 1),
                colors = "Set1") %>%
        add_markers() %>%
        layout(scene = list(annotations = list(list(x = pareto[1, "MKS"],
                                                    y = pareto[1, "Regs"],
                                                    z = pareto[1, "DPS"],
                                                    text = "Starting Point",
                                                    textangle = 0,
                                                    font = list(color = "black",
                                                                size = 12),
                                                    arrowcolor = "black",
                                                    arrowsize = 3,
                                                    arrowwidth = 1,
                                                    arrowhead = 1)),
                            xaxis = list(title = 'MKS'),
                            yaxis = list(title = 'Regs'),
                            zaxis = list(title = 'DSP')))

    return(p)
}
