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

import sys

class LegUpParametersTuner(MeasurementInterface):
    def get_wallclock_time(self, config_file):
        penalty = 999999999

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
        return opentuner.resultsdb.models.Result(time = cost)

    def save_final_config(self, configuration):
        self.manipulator().save_to_file(configuration.data,
                                        'final_config.json')

if __name__ == '__main__':
    argparser        = opentuner.default_argparser()
    application      = "sha"
    application_path = "legup_src/legup-4.0/examples/chstone/{0}".format(application)
    container_path   = "/root/legup_src/legup-4.0/examples/chstone/{0}/tuner".format(application)
    host_path        = "/home/phrb/code/legup-tuner"
    image_name       = "legup_ubuntu"
    script_name      = "measure.sh"
    legup_parameters.generate_seed()
    LegUpParametersTuner.main(argparser.parse_args())
