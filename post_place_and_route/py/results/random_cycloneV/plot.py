#! /usr/bin/python

import re
import os
import matplotlib as mpl

import math

mpl.use('agg')

import matplotlib.pyplot as plt
import numpy as np

def config_matplotlib():
    plt.rc('text', usetex = True)
    plt.rc('font', family = 'serif')

    font = {'family' : 'serif',
            'size'   : 18}

    mpl.rc('font', **font)

def autolabel(rects, ax):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width() / 2., height + .01,
                '%.2f' % height,
                ha = 'center', va = 'bottom')

def plot_sct(data_x,
             data_y,
#             data_error_y,
             plot_name,
             title,
             xlabel,
             ylabel):
    fig = plt.figure(1, figsize=(10, 8))
    ax  = fig.add_subplot(111)

    ax.scatter(data_x, data_y)
#    ax.errorbar(data_x, data_y, yerr = data_error_y, linestyle="None")

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.tight_layout()

    fig.savefig("{0}.eps".format(plot_name), format = 'eps', dpi = 1000)

    plt.clf()

def plot_sct_cmp(data_x,
                 data_y,
                 labels,
                 plot_name,
                 title,
                 xlabel,
                 ylabel):

    colors    = len(data_x)
    color_map = plt.get_cmap('Spectral')

    fig = plt.figure(1, figsize=(10, 8))
    ax  = fig.add_subplot(111)

    ax.set_color_cycle([color_map(1. * i / colors) for i in range(colors)])

    for i in range(len(data_x)):
        ax.plot(data_x[i], data_y[i], '-o', label = labels[i])

    legend = plt.legend(loc = 9, bbox_to_anchor = [0.5, -0.1], ncol = 4, shadow = True,
                        title = "", fancybox = True)
    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.tight_layout()

    fig.savefig("{0}.eps".format(plot_name), format = 'eps', dpi = 1000,
                bbox_extra_artists=(legend,), bbox_inches = 'tight')

    plt.clf()

def plot_bar(data,
             xlabel,
             ylabel,
             index_range,
             width,
             tick_labels,
             file_title,
             title,
             ymax):

    indexes = np.arange(index_range)
    fig     = plt.figure(1, figsize=(10, 8))
    ax      = fig.add_subplot(111)

    rects   = ax.bar(indexes + width, data, width, color = 'black')

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_xticks(indexes + (1 * width))
    ax.set_ylabel(ylabel)
    ax.set_xticklabels(tick_labels)

    ax.set_ylim([0, ymax + (.1 * ymax)])
    ax.axhline(y=1., color='r')

    autolabel(rects, ax)

    plt.tight_layout()

    fig.savefig("{0}.eps".format(file_title), format = 'eps', dpi = 2000)

    plt.clf()

if __name__ == '__main__':
    config_matplotlib()

    applications      = ["dfadd_5400_2",
                         "dfdiv_5400_5",
                         "dfmul_5400_3",
                         "dfsin_5400_3",
                         "gsm_5400_1",
                         "jpeg_5400_1",
                         "mips_5400_5",
                         "motion_5400_3",
                         "sha_5400_3",
                         "adpcm_5400_1",
                         "aes_5400_3",
                         "blowfish_5400_2"]

    base_applications = ["dfadd_5400_",
                         "dfdiv_5400_",
                         "dfmul_5400_",
                         "dfsin_5400_",
                         "gsm_5400_",
                         "jpeg_5400_",
                         "mips_5400_",
                         "motion_5400_",
                         "sha_5400_",
                         "adpcm_5400_",
                         "aes_5400_",
                         "blowfish_5400_"]

    metrics           = [
                             { 'name': 'Normalized Sum of Metrics',
                               'source_file': 'best_log.txt',
                               'dest_file': 'nsam'},
                             { 'name': 'Logic Utilization',
                               'source_file': 'best_lu_log.txt',
                               'dest_file': 'lu'},
                             { 'name': 'Virtual Pins',
                               'source_file': 'best_pins_log.txt',
                               'dest_file': 'pins'},
                             { 'name': 'RAM Blocks',
                               'source_file': 'best_ram_log.txt',
                               'dest_file': 'ram'},
                             { 'name': 'Registers',
                               'source_file': 'best_regs_log.txt',
                               'dest_file': 'regs'},
                             { 'name': 'Block Memory Bits',
                               'source_file': 'best_block_log.txt',
                               'dest_file': 'block'},
                             { 'name': 'Cycles',
                               'source_file': 'best_cycles_log.txt',
                               'dest_file': 'cycles'},
                             { 'name': 'DSP Blocks',
                               'source_file': 'best_dps_log.txt',
                               'dest_file': 'dsp'},
                             { 'name': 'FMax',
                               'source_file': 'best_fmax_log.txt',
                               'dest_file': 'fmax'},
                        ]

    # Generate figure of all metrics for each application
    for application in applications:
        print application

        name          = "{0} Metrics during 1.5h of Tuning (Cyclone V, Random Start)".format(application.split("_")[0])
        dest_filename = "random_" + application.split("_")[0] + "_all_5400_chstone_CycloneV"

        data_x = []
        data_y = []
        labels = []

        # For each metric, generate the normalized value
        for metric in metrics:
            if metric['name'] != "Normalized Sum of Metrics":
                print metric['name']

                best_filename = metric['source_file']
                data_file     = open("{0}/{1}".format(application, best_filename), "r")
                data          = data_file.readlines()
                data_file.close()

                x = []
                y = []

                for line in data:
                    x.append(line.split()[0])
                    y.append(line.split()[1])

                if not np.isclose(float(y[0]), 0.0):
                    starting_y = float(y[0])
                else:
                    starting_y = 1.

                for i in range(len(y)):
                    if np.isclose(float(y[i]), 0.0):
                        y[i] = 1.

                    y[i] = float(y[i]) / starting_y

                data_x.append(x)
                data_y.append(y)
                labels.append(metric['dest_file'])

        # Compare all normalized metrics for each application
        plot_sct_cmp(data_x,
                     data_y,
                     labels,
                     dest_filename,
                     name,
                     "Time (s)",
                     "Relative Improvement")

    # For each metric, plot how it performed in each application
    # using the absolute values
    for metric in metrics:
        best_filename = metric['source_file']

        print metric['name']

        for application in applications:
            print application
            name          = metric['name'] + " during 1.5h of Tuning (Cyclone V, Random Start, {0})".format(application.split("_")[0])
            dest_filename = "random_" + application.split("_")[0] + "_" + metric['dest_file'] + "_5400_chstone_CycloneV"
            data_file     = open("{0}/{1}".format(application, best_filename), "r")
            data          = data_file.readlines()

            data_file.close()

            data_x = []
            data_y = []

            for line in data:
                data_x.append(line.split()[0])
                data_y.append(line.split()[1])

            # Plot absolute value evolution for each pair (application, metric)
            plot_sct(data_x,
                     data_y,
                     dest_filename,
                     name,
                     "Time (s)",
                     metric['name'])

        # For the normalized sum of all metrics,
        # plot the summary of relative improvements
        # for all applications in a single figure
        if metric['name'] == 'Normalized Sum of Metrics':
            dest_filename = "random_" + metric['dest_file'] + "_5400_chstone_CycloneV"
            name          = metric['name'] + " after 1.5h of Tuning (Cyclone V, Random Start)"
            speedups = []

            for application in applications:
                data_file = open("{0}/{1}".format(application, best_filename), "r")
                data      = data_file.readlines()

                data_file.close()

                best      = float(data[-1].split()[1])

                if best != float('inf'):
                    speedups.append((application.split("_")[0], best))
                else:
                    speedups.append((application.split("_")[0], 0))

            ymax = max([s[1] for s in speedups])

            # Plot summary of relative improvements
            plot_bar([s[1] for s in speedups],
                     "CHStone Applications",
                     "Improvement vs. LegUp's Default",
                     len(speedups),
                     .45,
                     [s[0] for s in speedups],
                     dest_filename,
                     name,
                     ymax)
