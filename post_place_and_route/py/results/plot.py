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
                ha = 'center', va = 'bottom', rotation = '90')

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

def plot_bar(data1,
             data2,
             xlabel,
             ylabel,
             index_range,
             width,
             tick_labels,
             file_title,
             title,
             ymax,
             line):

    indexes = np.arange(index_range)
    fig     = plt.figure(1, figsize=(18, 8))
    ax      = fig.add_subplot(111)

    rects1   = ax.bar(indexes, data1, width, color = 'black')
    rects2   = ax.bar(indexes + width, data2, width, color = 'gray')

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_xticks(indexes + (.5 * width))
    ax.set_ylabel(ylabel)
    ax.set_xticklabels(tick_labels, rotation = '30')

    ax.set_ylim([0, ymax + (.1 * ymax)])

    if line:
        ax.axhline(y=1., color='r')

    ax.legend((rects1[0], rects2[0]), ('Default Start', 'Random Start'))

    autolabel(rects1, ax)
    autolabel(rects2, ax)

    plt.tight_layout()

    fig.savefig("{0}.eps".format(file_title), format = 'eps', dpi = 2000)

    plt.clf()

if __name__ == '__main__':
    config_matplotlib()

    applications   =  { 'random_cycloneV'  : ["dfadd_5400_2",
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
                                              "blowfish_5400_2"],
                        'default_cycloneV' : ["dfadd_5400_5",
                                              "dfdiv_5400_4",
                                              "dfmul_5400_5",
                                              "dfsin_5400_2",
                                              "gsm_5400_1",
                                              "jpeg_5400_1",
                                              "mips_5400_2",
                                              "motion_5400_1",
                                              "sha_5400_1",
                                              "adpcm_5400_1",
                                              "aes_5400_5",
                                              "blowfish_5400_2"],
                        'default_stratixV' : ["dfadd_5400_4",
                                              "dfdiv_5400_5",
                                              "dfmul_5400_1",
                                              "dfsin_5400_2",
                                              "gsm_5400_1",
                                              "jpeg_5400_1",
                                              "mips_5400_1",
                                              "motion_5400_2",
                                              "sha_5400_1",
                                              "adpcm_5400_5",
                                              "aes_5400_4",
                                              "blowfish_5400_3"]
                      }

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

    # For each metric, plot how it performed in each application
    # using the absolute values
    for metric in metrics:
        best_filename = metric['source_file']
        # For all metrics, plot the summary of absolute improvements for all
        # applications in a single figure.
        # For the Normalized Sum, plot the relative improvements
        dest_filename = "rel_comp_" + metric['dest_file'] + "_5400_chstone_CycloneV"
        name          = "Relative Improvement for " + metric['name'] + ", after 1.5h of Tuning (Cyclone V)"
        default_speedups = []
        random_speedups = []

        current_board = 'default_cycloneV'
        random_board = 'random_cycloneV'
        current_apps = applications[current_board]

        for i in range(len(current_apps)):
            application = current_apps[i]

            default_data_file = open("{0}/{1}/{2}".format(current_board,
                                                  application,
                                                  best_filename),
                                                  "r")
            default_data      = default_data_file.readlines()

            random_data_file = open("{0}/{1}/{2}".format(random_board,
                                                  application,
                                                  best_filename),
                                                  "r")
            random_data      = random_data_file.readlines()

            random_data_file.close()
            default_data_file.close()

            default_best     = float(default_data[-1].split()[1])
            random_best      = float(random_data[-1].split()[1])

            # Relative improvement already computed
            if metric['name'] == 'Normalized Sum of Metrics':
                if default_best != float('inf'):
                    default_speedups.append((application.split("_")[0], default_best))
                else:
                    default_speedups.append((application.split("_")[0], 0))

                if random_best != float('inf'):
                    random_speedups.append((application.split("_")[0], random_best))
                else:
                    random_speedups.append((application.split("_")[0], 0))
            else:
                # Compute relative improvements
                index = 0
                default_start = float(default_data[index].split()[1])
                index += 1

                while default_start == float('inf') and index < len(default_data):
                    default_start = float(default_data[index].split()[1])
                    index += 1

                index = 0
                random_start  = float(default_data[0].split()[1])
                index += 1

                while random_start == float('inf') and index < len(random_data):
                    random_start = float(random_data[index].split()[1])
                    index += 1

                if default_best != float('inf') and default_start != float(0) and default_start != float('inf'):
                    default_speedups.append((application.split("_")[0], default_best / default_start))
                else:
                    default_speedups.append((application.split("_")[0], 0))

                if random_best != float('inf') and default_start != float(0) and random_start != float('inf'):
                    random_speedups.append((application.split("_")[0], random_best / random_start))
                else:
                    random_speedups.append((application.split("_")[0], 0))

        default_ymax = max([s[1] for s in default_speedups])
        random_ymax = max([s[1] for s in random_speedups])

        print(default_ymax, random_ymax)

        ymax = max(default_ymax, random_ymax)

        # Plot summary of relative improvements
        plot_bar([s[1] for s in default_speedups],
                 [s[1] for s in random_speedups],
                 "CHStone Applications",
                 "Improvement vs. Starting Point",
                 len(default_speedups),
                 .225,
                 [s[0] for s in default_speedups],
                 dest_filename,
                 name,
                 ymax,
                 True)

    # For each metric, plot how it performed in each application
    # using the absolute values
    for metric in metrics:
        # Plot absolute values
        if metric['name'] != 'Normalized Sum of Metrics':
            best_filename = metric['source_file']
            # For all metrics, plot the summary of absolute final values for all
            # applications in a single figure.
            dest_filename = "abs_comp_" + metric['dest_file'] + "_5400_chstone_CycloneV"
            name          = "Final Values for " + metric['name'] + ", after 1.5h of Tuning (Cyclone V)"
            default_speedups = []
            random_speedups = []

            current_board = 'default_cycloneV'
            random_board = 'random_cycloneV'
            current_apps = applications[current_board]

            for i in range(len(current_apps)):
                application = current_apps[i]

                default_data_file = open("{0}/{1}/{2}".format(current_board,
                                                      application,
                                                      best_filename),
                                                      "r")
                default_data      = default_data_file.readlines()

                random_data_file = open("{0}/{1}/{2}".format(random_board,
                                                      application,
                                                      best_filename),
                                                      "r")
                random_data      = random_data_file.readlines()

                random_data_file.close()
                default_data_file.close()

                default_best     = float(default_data[-1].split()[1])
                random_best      = float(random_data[-1].split()[1])

                if default_best != float('inf'):
                    default_speedups.append((application.split("_")[0], default_best))
                else:
                    default_speedups.append((application.split("_")[0], 0))

                if random_best != float('inf'):
                    random_speedups.append((application.split("_")[0], random_best))
                else:
                    random_speedups.append((application.split("_")[0], 0))

        default_ymax = max([s[1] for s in default_speedups])
        random_ymax = max([s[1] for s in random_speedups])

        print(default_ymax, random_ymax)

        ymax = max(default_ymax, random_ymax)

        # Plot summary of relative improvements
        plot_bar([s[1] for s in default_speedups],
                 [s[1] for s in random_speedups],
                 "CHStone Applications",
                 "Improvement vs. Starting Point",
                 len(default_speedups),
                 .225,
                 [s[0] for s in default_speedups],
                 dest_filename,
                 name,
                 ymax,
                 False)
