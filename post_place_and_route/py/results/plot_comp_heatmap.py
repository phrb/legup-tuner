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

    print(data.shape)

    fig     = plt.figure(1, figsize=(18, 10))
    ax      = fig.add_subplot(111)

    for y in range(data.shape[0]):
        for x in range(data.shape[1]):
            if data[y, x] == 0.5:
                cell_color = 'black'
                data[y, x] = 1.0

                plt.text(x + 0.5, y + 0.5, '--',
                        horizontalalignment='center',
                        verticalalignment='center',
                        color=cell_color,
                        usetex=True,
                        fontsize=44,
                        weight='black'
                        )

            else:
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
                        weight='black'
                        )

    heatmap = plt.pcolor(data, cmap = plt.cm.RdBu_r, vmin = 0.5, vmax = 1.5, edgecolors='gray')
    #plt.colorbar()

    xlabels = ["\\textit{FMax}", "\\textit{DSP}", "\\textit{Cycles}",
               "\\textit{Blocks}", "\\textit{Regs}", "\\textit{BRAM}",
               "\\textit{Pins}", "\\textit{LUTs}"]
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

    applications   =  ["dfadd_5400_",
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
                       "blowfish_5400_"
                      ]

    metrics           = [
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

    boards = ["random_stratixV", "default_stratixV"]

    heatmaps = {}

    for board in boards:
        print(board)
        heatmaps[board] = {}
        heatmap = heatmaps[board]

        for metric in metrics:
            print(metric)
            heatmap[metric['name']] = []

            best_filename = metric['source_file']
            speedups = []
            error = []

            for i in range(len(applications)):
                print(applications[i])
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

                    if best != float('inf'):
                        all_best.append(best)

                if len(all_best) >= 1:
                    heatmap[metric['name']].append((application.split("_")[0], numpy.mean(all_best)))
                    #speedups.append((application.split("_")[0], numpy.mean(all_best)))
                    #error.append((application.split("_")[0], numpy.std(all_best)))
                else:
                    heatmap[metric['name']].append((application.split("_")[0], float('inf')))
                    #speedups.append((application.split("_")[0], 1))
                    #error.append((application.split("_")[0], 1))

            #ymax = max([s[1] for s in speedups])

            #print(ymax)

    heatmap_data = []
    heatmap_apps = []
    heatmap_metr = []

    heatmap = heatmaps['random_stratixV']

    #print(heatmap.keys())

    for name in heatmap.keys():
        app_values = []
        #heatmap_apps.append(name)
        heatmap_metr.append(name)

        #print(heatmap[name])
        for random_value, default_value in zip(heatmaps['random_stratixV'][name], heatmaps['default_stratixV'][name]):
            if random_value[1] == float('inf') and default_value != float('inf'):
                app_values.append(0.5)
            elif random_value[1] != float('inf') and default_value == float('inf'):
                app_values.append(1.5)
            elif name == "FMax" and (random_value[1] < default_value[1]):
                #app_values.append(0.5)
                app_values.append(random_value[1] / default_value[1])
            elif name == "FMax" and (random_value[1] > default_value[1]):
                #app_values.append(1.5)
                app_values.append(random_value[1] / default_value[1])
            elif random_value[1] > default_value[1]:
                #app_values.append(0.5)
                app_values.append(default_value[1] / random_value[1])
            elif random_value[1] < default_value[1]:
                #app_values.append(1.5)
                app_values.append(default_value[1] / random_value[1])
            elif not random_value[1] == default_value[1] and math.isnan(random_value[1] / default_value[1]):
                app_values.append(0.5)
            else:
                app_values.append(1.0)

            if "\\textit{" + random_value[0] + "}" not in heatmap_apps:
                heatmap_apps.append("\\textit{" + random_value[0] + "}")

        heatmap_data.append(app_values)

    print(heatmap_data)
    plot_heatmap(numpy.transpose(heatmap_data),
                 heatmap_apps,
                 heatmap_metr,
                 "CHStone Applications",
                 "Quartus Metrics",
                 "heatmap_comp_stratixV",
                 "")
