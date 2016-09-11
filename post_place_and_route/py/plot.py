#! /usr/bin/python

from scipy import stats

import os
import matplotlib as mpl

mpl.use('agg')

import matplotlib.pyplot as plt
import numpy as np

def config_matplotlib():
    plt.rc('text', usetex = True)
    plt.rc('font', family = 'serif')

    font = {'family' : 'serif',
            'size'   : 18}

    mpl.rc('font', **font)

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
             title):

    indexes = np.arange(width, index_range)
    fig     = plt.figure(1, figsize=(9, 6))
    ax      = fig.add_subplot(111)

    ax.bar(indexes, data, width, color = 'black')

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_xticks(indexes + (width / 2))
    ax.set_ylabel(ylabel)
    ax.set_xticklabels(tick_labels, rotation = 30)

    plt.tight_layout()

    fig.savefig("{0}.eps".format(file_title), format = 'eps', dpi = 2000)

    plt.clf()

if __name__ == '__main__':
    config_matplotlib()

    applications     = ["sha_7200_2",
                        "dfadd_7200_2"]
    speedups         = []
    default_filename = "default.txt"
    best_filename    = "best_log.txt"

    for application in applications:
        best_file = open("{0}/{1}".format(application, best_filename), "r")
        best      = float(best_file.readlines()[-1].split()[1])

        default_file = open("{0}/{1}".format(application, default_filename), "r")
        default      = float(default_file.readline())
        speedups.append((application.split("_")[0], 1 - (best / default)))

    print speedups

    plot_bar([s[1] for s in speedups],
             "testx",
             "testy",
             len(speedups),
             .5,
             [s[0] for s in speedups],
             "testf",
             "testt")

