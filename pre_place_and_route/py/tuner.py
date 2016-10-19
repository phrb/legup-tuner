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

from shutil import copytree, rmtree

import json

from uuid import uuid4

def log_intermediate(current_time, manager):
    current_best = manager.get_best_result()

    if current_best != None:
        best_log.write("{0} {1}\n".format(current_time, current_best.time))
        best_config_log.write("{0},\n".format(json.dumps(current_best.configuration.data)))
        print current_time, current_best.time

def save_final_configuration(configuration):
    best_config_log.write("]")
    best_config_log.close()

    best_log.close()

    legup_parameters.generate_file(configuration, "./")

def get_wallclock_time(cfg):
    unique_id        = uuid4()

    unique_path = "{0}_{1}".format(application, unique_id)

    copytree(application, unique_path)

    os.remove("{0}/config.tcl".format(unique_path))

    filename = legup_parameters.generate_file(cfg, unique_path)

    cmd = "./{0} {1}".format(script_name, unique_path)

    try:
        output = subprocess.check_output(cmd, shell = True)
        output = output.split()

        cycles = float(output[0])

        rmtree(unique_path, ignore_errors = True)
        return cycles
    except:
        rmtree(unique_path, ignore_errors = True)
        return penalty

def tuning_loop():
    report_delay = 200
    last_time    = time.time()
    start_time   = last_time
    parser       = argparse.ArgumentParser(parents = opentuner.argparsers())

    parser.add_argument("--processes",
                        type = int,
                        help = "Number of Python threads available.")
    parser.add_argument("--no-wait",
                        action = "store_true",
                        help   = "Do not wait for requested results to generate more requests.")

    args         = parser.parse_args()
    pool         = ThreadPool(args.processes)
    manipulator  = ConfigurationManipulator()

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
                    manager.report_result(dr, Result(time = result))

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
    application      = "../motion"
    script_name      = "measure.sh"

    penalty          = float('inf')

    best_log         = open("best_log.txt", "w+")
    best_config_log  = open("best_log.json", "w+")
    best_config_log.write("[\n")
    #legup_parameters.generate_seed()
    tuning_loop()
