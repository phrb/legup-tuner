#! /usr/bin/python

from scipy import stats

import re
import os
import matplotlib as mpl

mpl.use('agg')

import matplotlib.pyplot as plt
import numpy as np

def config_matplotlib():
    plt.rc('text', usetex = True)
    plt.rc('font', family = 'serif')

    font = {'family' : 'serif',
            'size'   : 16}

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
             data_error_y,
             plot_name,
             title,
             xlabel,
             ylabel):
    fig = plt.figure(1, figsize=(9, 6))
    ax  = fig.add_subplot(111)

    ax.scatter(data_x, data_y)
    ax.errorbar(data_x, data_y, yerr = data_error_y, linestyle="None")

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.tight_layout()

    fig.savefig("{0}.eps".format(plot_name), format = 'eps', dpi = 1000)

    plt.clf()

def plot_sct_cmp(data1_x,
                 data1_y,
                 data1_error_y,
                 data2_x,
                 data2_y,
                 data2_error_y,
                 plot_name,
                 title,
                 xlabel,
                 ylabel):
    fig = plt.figure(1, figsize=(9, 6))
    ax  = fig.add_subplot(111)

    ax.scatter(data1_x, data1_y)
    ax.errorbar(data1_x, data1_y, yerr = data1_error_y, linestyle="None")

    ax.scatter(data2_x, data2_y)
    ax.errorbar(data2_x, data2_y, yerr = data2_error_y, linestyle="None")

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.tight_layout()

    fig.savefig("{0}.eps".format(plot_name), format = 'eps', dpi = 1000)

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
    ax.set_xticks(indexes + (1.5 * width))
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

    applications     = ["sha_7200_2",
                        "dfadd_7200_2",
                        "dfmul_7200_1",
                        "dfdiv_7200_1",
                        "motion_7200_1"]
    speedups         = []
    best_filename    = "best_log.txt"

    for application in applications:
        data_file = open("{0}/{1}".format(application, best_filename), "r")
        data      = data_file.readlines()

        data_file.close()

        best      = float(data[-1].split()[1])
        default   = float(data[0].split()[1])

        speedups.append((application.split("_")[0], default / best))

    print speedups
    ymax = max([s[1] for s in speedups])

    plot_bar([s[1] for s in speedups],
             "CHStone Applications",
             "Speedup vs. LegUp's Default",
             len(speedups),
             .45,
             [s[0] for s in speedups],
             "wct_speedups_chstone_7200_hls",
             "Wall-clock Time Speedup after Tuning for 2h (Cyclone V DE1-SoC)",
             ymax)

    path             = "huang_et_al"
    applications     = ["wct_sha.txt",
                        "wct_dfadd.txt",
                        "wct_dfmul.txt",
                        "wct_dfdiv.txt",
                        "wct_motion.txt"]
    speedups         = []

    for application in applications:
        data_file = open("{0}/{1}".format(path, application), "r")
        speedup   = float(data_file.readline())

        data_file.close()

        speedups.append((application.replace(".", "_").split("_")[1], speedup))

    print speedups

    new_max = max([s[1] for s in speedups])
    if new_max > ymax:
        ymax = new_max

    plot_bar([s[1] for s in speedups],
             "CHStone Applications",
             "Speedup vs. LLVM's -O3",
             len(speedups),
             .45,
             [s[0] for s in speedups],
             "wct_speedups_chstone_IN3_llvm",
             "Wall-clock Time Speedup after IN3 (Cyclone II)",
             ymax)

    applications     = ["sha_1800_1",
                        "dfadd_1800_1",
                        "dfmul_1800_1",
                        "dfdiv_1800_1",
                        "motion_1800_1",
                        "adpcm_1800_1"]
    speedups         = []
    best_filename    = "best_log.txt"

    for application in applications:
        data_file = open("{0}/{1}".format(application, best_filename), "r")
        data      = data_file.readlines()

        data_file.close()

        best      = float(data[-1].split()[1])
        default   = float(data[0].split()[1])

        speedups.append((application.split("_")[0], default / best))

    print speedups
    ymax = max([s[1] for s in speedups])

    plot_bar([s[1] for s in speedups],
             "CHStone Applications",
             "Speedup vs. LegUp's Default",
             len(speedups),
             .45,
             [s[0] for s in speedups],
             "clk_speedups_chstone_1800_hls",
             "Clock Cycles Speedup after Tuning for 30min (Cyclone V DE1-SoC)",
             ymax)

    path             = "huang_et_al"
    applications     = ["clk_sha.txt",
                        "clk_dfadd.txt",
                        "clk_dfmul.txt",
                        "clk_dfdiv.txt",
                        "clk_motion.txt"]
    speedups         = []

    for application in applications:
        data_file = open("{0}/{1}".format(path, application), "r")
        speedup   = float(data_file.readline())

        data_file.close()

        speedups.append((application.replace(".", "_").split("_")[1], speedup))

    print speedups
    new_max = max([s[1] for s in speedups])
    if new_max > ymax:
        ymax = new_max

    plot_bar([s[1] for s in speedups],
             "CHStone Applications",
             "Speedup vs. LLVM's -O3",
             len(speedups),
             .45,
             [s[0] for s in speedups],
             "clk_speedups_chstone_IN3_llvm",
             "Clock Cycles Speedup after IN3 (Cyclone II)",
             ymax)
