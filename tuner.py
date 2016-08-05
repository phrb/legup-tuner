from enum import Enum
import legup_parameters
import argparse

import subprocess

import opentuner
from opentuner.search.manipulator import ConfigurationManipulator
from opentuner.search.manipulator import EnumParameter, BooleanParameter
from opentuner.measurement import MeasurementInterface
from opentuner import IntegerParameter
from opentuner import Result

from datetime import datetime

import sys
import json

class LegUpParametersTuner(MeasurementInterface):
    def log_intermediate(self, data, cost):
        global last_best, start_date

        now = datetime.now()

        full_log.write("{0} {1}\n".format((now - start_date).total_seconds(), cost))
        full_config_log.write("{0},\n".format(json.dumps(data)))

        if cost < last_best:
            last_best = cost
            best_log.write("{0} {1}\n".format((now - start_date).total_seconds(), cost))
            best_config_log.write("{0},\n".format(json.dumps(data)))
        else:
            best_log.write("{0} {1}\n".format((now - start_date).total_seconds(), last_best))
            best_config_log.write("{0},\n".format(json.dumps(data)))

    def get_wallclock_time(self, config_file):
        docker_cmd = "sudo docker run --rm"
        docker_cmd += " -w {0}".format(container_path)

        docker_cmd += " -v {0}:".format(host_path)
        docker_cmd += "{0} -t -i {1}".format(container_path, image_name)

        docker_cmd += " /bin/bash -c \"./{0}\"".format(script_name)

        output = subprocess.check_output(docker_cmd, shell = True)
        output = output.split()
        print(output)

        try:
            cycles = float(output[0])
            cycles_per_second = float(output[1])
            factor = 1000.
            return cycles * (factor / cycles_per_second)
        except ValueError:
            # TODO: Discover all parameters that
            #       break compilation
            print("PENALTY!")
            return penalty

    def manipulator(self):
        manipulator = ConfigurationManipulator()
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
        return manipulator

    def run(self, desired_result, input, limit):
        filename = legup_parameters.generate_file(desired_result.configuration.data)
        cost = self.get_wallclock_time(filename)

        if cost != penalty:
            self.log_intermediate(desired_result.configuration.data, cost)
        return opentuner.resultsdb.models.Result(time = cost)

    def save_final_config(self, configuration):
        self.manipulator().save_to_file(configuration.data,
                                        'final_config.json')
        full_config_log.write("]")
        full_config_log.close()

        best_config_log.write("]")
        best_config_log.close()

        full_log.close()
        best_log.close()

if __name__ == '__main__':
    argparser        = opentuner.default_argparser()
    application      = "dfadd"
    application_path = "legup_src/legup-4.0/examples/chstone/{0}".format(application)
    container_path   = "/root/legup_src/legup-4.0/examples/chstone/{0}/tuner".format(application)
    host_path        = "/home/phrb/code/legup-tuner"
    image_name       = "legup_ubuntu"
    script_name      = "measure.sh"

    penalty          = 999999999

    last_best        = float('inf')
    start_date       = datetime.now()

    full_log         = open("full_log.txt", "w+")
    full_config_log  = open("full_log.json", "w+")
    full_config_log.write("[\n")

    best_log         = open("best_log.txt", "w+")
    best_config_log  = open("best_log.json", "w+")
    best_config_log.write("[\n")
    #legup_parameters.generate_seed()
    LegUpParametersTuner.main(argparser.parse_args())
