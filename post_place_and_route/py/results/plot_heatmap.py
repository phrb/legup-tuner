#! /usr/bin/python

import re
import os
import matplotlib as mpl

import math
import numpy

mpl.use('agg')

import matplotlib.pyplot as plt
import numpy as np

def config_matplotlib():
    plt.rc('text', usetex = True)
    plt.rc('font', family = 'serif')

    font = {'family' : 'serif',
            'size'   : 28}

    mpl.rc('font', **font)

def plot_heatmap(data,
                 ylabels,
                 xlabels,
                 ylabel,
                 xlabel,
                 file_title,
                 title):

    #print(data.shape)

    fig     = plt.figure(1, figsize=(18, 10))
    ax      = fig.add_subplot(111)

#    aux = data[-1]
#
#    data[-1] = data[-2]
#
#    data[-2] = aux

    heatmap = plt.pcolor(data, cmap = plt.cm.RdBu_r, vmin = 0.5, vmax = 1.5, edgecolors='gray')
    #plt.colorbar()

    for y in range(data.shape[0]):
        for x in range(data.shape[1]):
            if data[y, x] <= 0.65 or data[y, x] >= 1.45:
                cell_color = 'white'
            else:
                cell_color = 'black'

            plt.text(x + 0.5, y + 0.5, '%.2f' % data[y, x],
                    horizontalalignment='center',
                    verticalalignment='center',
                    color=cell_color,
                    usetex=True,
                    fontsize=44,
                    fontweight='bold'
                    )

    xlabels = ["\\textit{FMax}", "\\textit{DSP}", "\\textit{Cycles}",
               "\\textit{Blocks}", "\\textit{Regs}", "\\textit{BRAM}",
               "\\textit{Pins}", "\\textit{LUTs}", "\\textbf{WNS}"]
    xlabels.reverse()

    ax.set_yticks(np.arange(len(ylabels)) + 0.5, minor = False)
    ax.set_xticks(np.arange(len(xlabels)) + 0.5, minor = False)

    ax.set_title(title)
    #ax.set_xlabel(xlabel)
    ax.set_xticklabels(xlabels, minor=False)
    #ax.set_ylabel(ylabel)
    ax.set_yticklabels(ylabels, minor=False)

    #plt.xticks(rotation = 45)
    #plt.yticks(rotation = 45)

    plt.tight_layout()

    fig.savefig("{0}.eps".format(file_title), format = 'eps', dpi = 2000, bbox_inches = 'tight')

    plt.clf()

if __name__ == '__main__':
    config_matplotlib()

    runs = 10

    applications   =  [
                       "blowfish_5400_",
                       "dfadd_5400_",
                       "dfdiv_5400_",
                       "dfmul_5400_",
                       "dfsin_5400_",
                       "gsm_5400_",
                       #"jpeg_5400_",
                       "mips_5400_",
                       "motion_5400_",
                       "sha_5400_",
                       "adpcm_5400_",
                       "aes_5400_",
                      ]

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

    boards = ["random_stratixV", "default_stratixV", "default_stratixV_area", "default_stratixV_perf", "default_stratixV_perflat"]

    for board in boards:
        #print(board)
        heatmap = {}

        for metric in metrics:
            #print(metric)
            heatmap[metric['name']] = []

            best_filename = metric['source_file']
            speedups = []
            error = []

            for i in range(len(applications)):
                #print(applications[i])
                application = applications[i]

                all_best = []

                for j in range(1, runs + 1):
                    if os.path.isfile("{0}/{1}{2}/{3}".format(board,
                                                              application,
                                                              j,
                                                              best_filename)):

                        data_file = open("{0}/{1}{2}/{3}".format(board,
                                                                 application,
                                                                 j,
                                                                 best_filename),
                                                                 "r")
                        data = data_file.readlines()
                        data_file.close()
                        best = float(data[-1].split()[1])

                        # Relative improvement already computed
                        if metric['name'] == 'Normalized Sum of Metrics':
                            if best != float('inf'):
                                all_best.append(best)
                        else:
                            # Compute relative improvements
                            index = 0
                            start = float(data[index].split()[1])
                            index += 1

                            while start == float('inf') and index < len(data):
                                start = float(data[index].split()[1])
                                index += 1

                            if metric['name'] == 'FMax' and best != float(0) and best != float('inf'):
                                #print(start/best, best/start)
                                all_best.append(start / best)
                            elif start != float(0) and start != float('inf'):
                                all_best.append(best / start)

                if len(all_best) > 0:
                    heatmap[metric['name']].append((application.split("_")[0], numpy.mean(all_best)))
                else:
                    heatmap[metric['name']].append((application.split("_")[0], 1))

        heatmap_data = []
        heatmap_apps = []
        heatmap_metr = []

        for name in heatmap.keys():
            app_values = []
            heatmap_metr.append(name)

            for value in heatmap[name]:
                app_values.append(value[1])
                if "\\textit{" + value[0] + "}" not in heatmap_apps:
                    heatmap_apps.append("\\textit{" + value[0] + "}")

            heatmap_data.append(app_values)

            if name == "Normalized Sum of Metrics":
                print(board)
                print((1 - numpy.mean(app_values)) * 100)
                print((1 - min(app_values)) * 100)

        plot_heatmap(numpy.transpose(heatmap_data),
                     heatmap_apps,
                     heatmap_metr,
                     "CHStone Applications",
                     "Quartus Metrics",
                     "heatmap_" + board,
                     "")
