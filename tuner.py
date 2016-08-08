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
        best_config_log.write("{0},\n".format(json.dumps(current_best.configuration.data)))
        print current_time, current_best.time

def save_final_configuration(configuration):
    best_config_log.write("]")
    best_config_log.close()

    best_log.close()

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

    docker_cmd += " /bin/bash -c \"./{0}\"".format(script_name)

    output = subprocess.check_output(docker_cmd, shell = True)
    output = output.split()

    rmtree(unique_host_path, ignore_errors = True)

    try:
        cycles            = float(output[0])
        cycles_per_second = float(output[1])
        factor            = 1000.
        return cycles * (factor / cycles_per_second)
    except ValueError:
        # TODO: Discover all parameters that
        #       break compilation
        return penalty

def tuning_loop():
    report_delay = 30
    last_time    = time.time()
    start_time   = last_time
    iterations   = 5
    parser       = argparse.ArgumentParser(parents=opentuner.argparsers())
    args         = parser.parse_args()
    pool         = ThreadPool(16)
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

    for x in xrange(iterations):
        desired_results = manager.get_desired_results()
        desired_cfgs    = [result.configuration.data for result in desired_results]

        if len(desired_results) == 0:
            continue

        results = []

        for desired_cfg in desired_cfgs:
            results.append(pool.apply_async(get_wallclock_time, desired_cfg))

        ready_results = []
        for dr, result in zip(desired_results, results):
            if result.ready() and dr not in ready_results:
                cost = result.get()
                manager.report_result(dr, Result(time = cost))
                ready_results.append(dr)
                print("reported result. time = {0}".format(cost))

        current_time = time.time()

        if (current_time - last_time) >= report_delay:
            log_intermediate(current_time - start_time, manager)
            last_time = current_time

    current_time = time.time()
    log_intermediate(current_time - start_time, manager)

    save_final_configuration(manager.get_best_configuration())
    manager.finish()

if __name__ == '__main__':
    application      = "dfadd"
    application_path = "legup_src/legup-4.0/examples/chstone/{0}".format(application)
    container_path   = "/root/legup_src/legup-4.0/examples/chstone/{0}/tuner".format(application)
    host_path        = "/home/phrb/code/legup-tuner"
    image_name       = "legup_ubuntu"
    script_name      = "measure.sh"

    penalty          = float('inf')

    best_log         = open("best_log.txt", "w+")
    best_config_log  = open("best_log.json", "w+")
    best_config_log.write("[\n")
    #legup_parameters.generate_seed()
    tuning_loop()
