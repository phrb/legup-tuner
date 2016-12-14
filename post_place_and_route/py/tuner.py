import adddeps  # add opentuner to path in dev mode

from enum import Enum
import legup_parameters
import argparse

import subprocess
import time
from multiprocessing.pool import ThreadPool

import opentuner
from opentuner.api import TuningRunManager
from opentuner.search.manipulator import ConfigurationManipulator
from opentuner.measurement.interface import DefaultMeasurementInterface
from opentuner.search.manipulator import EnumParameter, BooleanParameter
from opentuner.measurement import MeasurementInterface
from opentuner import IntegerParameter
from opentuner.resultsdb.models import Result

import time

import sys
import os

from shutil import copy, rmtree

import json

from uuid import uuid4

def log_intermediate(current_time, manager):
    current_best = manager.get_best_result()

    if current_best != None:
        best_log.write("{0} {1}\n".format(current_time, current_best.time))
        best_cycles_log.write("{0} {1}\n".format(current_time, current_best.cycles))
        best_fmax_log.write("{0} {1}\n".format(current_time, current_best.fmax))

        best_lu_log.write("{0} {1}\n".format(current_time, current_best.LU))
        best_pins_log.write("{0} {1}\n".format(current_time, current_best.pins))

        best_regs_log.write("{0} {1}\n".format(current_time, current_best.regs))
        best_block_log.write("{0} {1}\n".format(current_time, current_best.block))

        best_ram_log.write("{0} {1}\n".format(current_time, current_best.ram))
        best_dsp_log.write("{0} {1}\n".format(current_time, current_best.dsp))

        best_config_log.write("{0},\n".format(json.dumps(current_best.configuration.data)))
        print current_time, current_best.time

def save_final_configuration(configuration):
    best_config_log.write("]")
    best_config_log.close()

    best_log.close()
    best_cycles_log.close()
    best_fmax_log.close()

def get_wallclock_time(cfg):
    unique_id        = uuid4()

    unique_host_path = "{0}/{1}".format(host_path, unique_id)

    os.mkdir(unique_host_path)

    copy(script_name, "{0}/{1}".format(unique_host_path, script_name))

    filename = legup_parameters.generate_file(cfg, unique_host_path)

    docker_cmd  = "sudo docker run --rm"
    docker_cmd += " -w {0}".format(container_path)

    docker_cmd += " -v {0}:".format(unique_host_path)
    docker_cmd += "{0} -t -i {1}".format(container_path, image_name)

    docker_cmd += " /bin/bash -c \"./{0} {1} {2}\"".format(script_name,
                                                           unique_id,
                                                           verilog_file)

    try:
        output = subprocess.check_output(docker_cmd, shell = True)
        output = output.split()

        print output

        factor = 1000.
        cycles = float(output[0])
        fmax   = float(output[1])

        # Skip output[2,3,4]

        lu     = float(output[5])
        pins   = float(output[6])
        regs   = float(output[7])
        block  = float(output[8])
        ram    = float(output[9])
        dsp    = float(output[10])

        # TODO Improve weights
        value = (cycles * (factor / fmax)) + lu + pins + regs + block + ram + dsp

        result = { 'cycles': cycles,
                   'fmax': fmax,
                   'lu': lu,
                   'pins': pins,
                   'regs': regs,
                   'block': block,
                   'ram': ram,
                   'dsp': dsp,
                   'value': value,
                 }

        rmtree(unique_host_path, ignore_errors = True)
        return result
    except:
        # TODO: Discover all parameters that
        #       break compilation
        result = { 'cycles': penalty,
                   'fmax': penalty,
                   'lu': penalty,
                   'pins': penalty,
                   'regs': penalty,
                   'block': penalty,
                   'ram': penalty,
                   'dsp': penalty,
                   'value': penalty,
                 }

        rmtree(unique_host_path, ignore_errors = True)
        return result

def tuning_loop():
    report_delay = 30
    last_time    = time.time()
    start_time   = last_time
    iterations   = 5
    parser       = argparse.ArgumentParser(parents = opentuner.argparsers())

    parser.add_argument("--processes",
                        type = int,
                        help = "Number of Python threads available.")
    parser.add_argument("--no-wait",
                        action = "store_true",
                        help   = "Do not wait for requested results to generate more requests.")
    parser.add_argument("--application",
                        type = str,
                        help = "Application name.")
    parser.add_argument("--verilog-file",
                        type = str,
                        help = "Verilog file for the application.")

    args         = parser.parse_args()
    pool         = ThreadPool(args.processes)
    manipulator  = ConfigurationManipulator()

    global application
    global verilog_file
    global application_path
    global container_path
    global host_path
    global image_name
    global script_name

    application      = args.application
    verilog_file     = args.verilog_file
    application_path = "/root/legup_src/legup-4.0/examples/chstone/{0}".format(application)
    container_path   = "/root/legup_src/legup-4.0/examples/chstone/{0}/tuner".format(application)
    host_path        = "/home/bruelp/legup-tuner/post_place_and_route/py"
    image_name       = "legup_quartus"
    script_name      = "measure.sh"

    for name in legup_parameters.parameters:
        parameter_type = legup_parameters.parameter_type(name)
        values = legup_parameters.parameter_values(name)
        if parameter_type == int:
            manipulator.add_parameter(IntegerParameter(name, values[0], values[1]))
        elif parameter_type == bool:
            manipulator.add_parameter(BooleanParameter(name))
        elif parameter_type == Enum:
            manipulator.add_parameter(EnumParameter(name, values))
        else:
            print("ERROR: No such parameter type \"{0}\"".format(name))

    interface = DefaultMeasurementInterface(args            = args,
                                            manipulator     = manipulator,
                                            project_name    = 'HLS-FPGAs',
                                            program_name    = 'legup-tuner',
                                            program_version = '0.0.1')

    manager = TuningRunManager(interface, args)

    current_time      = time.time()
    computing_results = []
    computed_results  = []
    desired_results   = manager.get_desired_results()

    while current_time - start_time < args.stop_after:
        if args.no_wait:
            if len(desired_results) != 0 or len(computing_results) != 0:
                for desired_result in desired_results:
                    computing_results.append([desired_result,
                                              pool.apply_async(get_wallclock_time,
                                                              (desired_result.configuration.data, ))])

                for result in computing_results:
                    if result[1].ready() and result[0] not in computed_results:
                        cost = result[1].get()
                        manager.report_result(result[0], Result(time = cost))
                        computed_results.append(result)

                for result in computed_results:
                    if result in computing_results:
                        computing_results.remove(result)

                computed_results = []
        else:
            if len(desired_results) != 0:
                cfgs    = [dr.configuration.data for dr in desired_results]
                results = pool.map_async(get_wallclock_time, cfgs).get(timeout = None)

                for dr, result in zip(desired_results, results):
                    manager.report_result(dr,
                                          Result(time = result['value'],
                                                 cycles = result['cycles'],
                                                 fmax = result['fmax'],
                                                 LU = result['lu'],
                                                 pins = result['pins'],
                                                 regs = result['regs'],
                                                 block = result['block'],
                                                 ram = result['ram'],
                                                 dsp = result['dsp']))

        desired_results = manager.get_desired_results()

        current_time = time.time()

        if (current_time - last_time) >= report_delay:
            log_intermediate(current_time - start_time, manager)
            last_time = current_time

    current_time = time.time()
    log_intermediate(current_time - start_time, manager)

    save_final_configuration(manager.get_best_configuration())
    manager.finish()

if __name__ == '__main__':
    application      = ""
    verilog_file     = ""
    application_path = ""
    container_path   = ""
    host_path        = ""
    image_name       = ""
    script_name      = ""

    penalty          = float('inf')

    best_log         = open("best_log.txt", "w+")
    best_cycles_log  = open("best_cycles_log.txt", "w+")
    best_fmax_log    = open("best_fmax_log.txt", "w+")

    best_lu_log      = open("best_lu_log.txt", "w+")
    best_pins_log    = open("best_pins_log.txt", "w+")

    best_regs_log    = open("best_regs_log.txt", "w+")
    best_block_log   = open("best_block_log.txt", "w+")

    best_ram_log     = open("best_ram_log.txt", "w+")
    best_dsp_log     = open("best_dps_log.txt", "w+")

    best_config_log  = open("best_log.json", "w+")
    best_config_log.write("[\n")
    #legup_parameters.generate_seed()
    tuning_loop()
