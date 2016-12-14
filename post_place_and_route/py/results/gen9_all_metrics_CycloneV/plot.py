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

    applications     = ["dfadd_5400_1",
                        "dfdiv_5400_1",
                        "dfmul_5400_1",
                        "dfsin_5400_1",
                        "gsm_5400_1",
                        "jpeg_5400_1",
                        "mips_5400_1",
                        "motion_5400_1",
                        "sha_5400_1",
                        "adpcm_5400_1",
                        "aes_5400_1",
                        "blowfish_5400_1"]

    metrics          = [
                            { 'name': 'Sum of All Metrics',
                              'source_file': 'best_log.txt',
                              'dest_file': 'sam'},
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

    for metric in metrics:
        best_filename = metric['source_file']

        print metric['name']

        for application in applications:
            print application
            name          = metric['name'] + " during 1.5h of Tuning (Cyclone V, {0})".format(application.split("_")[0])
            dest_filename = application.split("_")[0] + "_" + metric['dest_file'] + "_5400_chstone_CycloneV"
            data_file = open("{0}/{1}".format(application, best_filename), "r")
            data      = data_file.readlines()

            data_file.close()

            data_x = []
            data_y = []

            for line in data:
                data_x.append(line.split()[0])
                data_y.append(line.split()[1])

            plot_sct(data_x,
                     data_y,
                     dest_filename,
                     name,
                     "Time (s)",
                     metric['name'])

        if metric['name'] == 'Sum of All Metrics':
            dest_filename = metric['dest_file'] + "_5400_chstone_CycloneV"
            name          = metric['name'] + " after 1.5h of Tuning (Cyclone V)"
            speedups = []

            for application in applications:
                data_file = open("{0}/{1}".format(application, best_filename), "r")
                data      = data_file.readlines()

                data_file.close()

                best      = float(data[-1].split()[1])
                default   = float(data[0].split()[1])

                if math.isnan(default / best) or default / best == float('inf'):
                    speedups.append((application.split("_")[0], 0))
                else:
                    speedups.append((application.split("_")[0], default / best))

            ymax = max([s[1] for s in speedups])

            plot_bar([s[1] for s in speedups],
                     "CHStone Applications",
                     "Improvement vs. LegUp's Default",
                     len(speedups),
                     .45,
                     [s[0] for s in speedups],
                     dest_filename,
                     name,
                     ymax)
