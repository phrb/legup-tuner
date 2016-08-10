import json
from enum import Enum

parameters = {
#    "set_parameter CASE_FSM" : [bool, [], True],
    "set_parameter CLOCK_PERIOD" : [int, [10, 30], ["set_parameter SDC_NO_CHAINING"], 10],
#    "set_parameter GROUP_RAMS" : [bool, [], False],
#    "set_parameter GROUP_RAMS_SIMPLE_OFFSET" : [bool, [], False],
#    "set_parameter LOCAL_RAMS" : [bool, [], False],
    "set_parameter MB_MINIMIZE_HW" : [bool, [], False],
    "set_combine_basicblock" : [int, [0, 2], [], 0],
#    "set_parameter CASEX" : [bool, ["set_parameter CASE_FSM"], False],
    "set_parameter DISABLE_REG_SHARING" : [bool, [], False],
    "set_parameter DONT_CHAIN_GET_ELEM_PTR" : [bool, [], False],
    "set_parameter DUAL_PORT_BINDING" : [bool, [], True],
    "set_parameter ENABLE_PATTERN_SHARING" : [bool, [], False],
    "set_parameter EXPLICIT_LPM_MULTS" : [bool, [], False],
    "set_parameter INCREMENTAL_SDC" : [bool, [], False],
    "set_parameter MB_MAX_BACK_PASSES" : [int, [-1, 100000], ["set_parameter MB_MINIMIZE_HW"], -1],
    "set_parameter MODULO_SCHEDULER" : [Enum, ["SDC_BACKTRACKING", "SDC_GREEDY", "ITERATIVE"], [], "SDC_BACKTRACKING"],
    "set_parameter MULTIPLIER_NO_CHAIN" : [bool, [], False],
    "set_parameter MULTIPUMPING" : [bool, [], False],
    "set_parameter NO_LOOP_PIPELINING" : [bool, [], False],
    "set_parameter NO_ROMS" : [bool, [], False],
    "set_parameter PATTERN_SHARE_ADD" : [bool, ["set_parameter ENABLE_PATTERN_SHARING"], True],
    "set_parameter PATTERN_SHARE_BITOPS" : [bool, ["set_parameter ENABLE_PATTERN_SHARING"], True],
    "set_parameter PATTERN_SHARE_SHIFT" : [bool, ["set_parameter ENABLE_PATTERN_SHARING"], True],
    "set_parameter PATTERN_SHARE_SUB" : [bool, ["set_parameter ENABLE_PATTERN_SHARING"], True],
    "set_parameter PIPELINE_ALL" : [bool, [], False],
    "set_parameter PIPELINE_RESOURCE_SHARING": [bool, [], True],
    "set_parameter PS_BIT_DIFF_THRESHOLD" : [int, [2, 16], ["set_parameter ENABLE_PATTERN_SHARING"], 10],
    "set_parameter PS_MAX_SIZE" : [int, [2, 16], ["set_parameter ENABLE_PATTERN_SHARING"], 10],
    "set_parameter PS_MIN_SIZE" : [int, [2, 16], ["set_parameter ENABLE_PATTERN_SHARING"], 1],
    "set_parameter PS_MIN_WIDTH" : [int, [2, 16], ["set_parameter ENABLE_PATTERN_SHARING"], 2],
#    "set_parameter RESTRICT_TO_MAXDSP" : [bool, [], False],
    "set_parameter SDC_MULTIPUMP" : [bool, ["set_parameter MULTIPUMPING"], False],
    "set_parameter SDC_NO_CHAINING" : [bool, [], False],
    "set_parameter SDC_PRIORITY" : [bool, [], True],
    "set_resource_constraint mem_dual_port" : [int, [1, 8], [], 2],
    "set_resource_constraint shared_mem_dual_port" : [int, [1, 8], [], 1],
    "set_resource_constraint signed_divide_8" : [int, [1, 8], [], 1],
    "set_resource_constraint signed_divide_16" : [int, [1, 8], [], 1],
    "set_resource_constraint signed_divide_32" : [int, [1, 8], [], 1],
    "set_resource_constraint signed_divide_64" : [int, [1, 8], [], 1],
    "set_resource_constraint signed_multiply_8" : [int, [1, 8], [], 1],
    "set_resource_constraint signed_multiply_16" : [int, [1, 8], [], 1],
    "set_resource_constraint signed_multiply_32" : [int, [1, 8], [], 1],
    "set_resource_constraint signed_multiply_64" : [int, [1, 8], [], 1],
    "set_resource_constraint signed_modulus_8" : [int, [1, 8], [], 1],
    "set_resource_constraint signed_modulus_16" : [int, [1, 8], [], 1],
    "set_resource_constraint signed_modulus_32" : [int, [1, 8], [], 1],
    "set_resource_constraint signed_modulus_64" : [int, [1, 8], [], 1],
    "set_resource_constraint signed_add_8" : [int, [1, 8], [], 1],
    "set_resource_constraint signed_add_16" : [int, [1, 8], [], 1],
    "set_resource_constraint signed_add_32" : [int, [1, 8], [], 1],
    "set_resource_constraint signed_add_64" : [int, [1, 8], [], 1],
    "set_resource_constraint unsigned_divide_8" : [int, [1, 8], [], 1],
    "set_resource_constraint unsigned_divide_16" : [int, [1, 8], [], 1],
    "set_resource_constraint unsigned_divide_32" : [int, [1, 8], [], 1],
    "set_resource_constraint unsigned_divide_64" : [int, [1, 8], [], 1],
    "set_resource_constraint unsigned_multiply_8" : [int, [1, 8], [], 1],
    "set_resource_constraint unsigned_multiply_16" : [int, [1, 8], [], 1],
    "set_resource_constraint unsigned_multiply_32" : [int, [1, 8], [], 1],
    "set_resource_constraint unsigned_multiply_64" : [int, [1, 8], [], 1],
    "set_resource_constraint unsigned_modulus_8" : [int, [1, 8], [], 1],
    "set_resource_constraint unsigned_modulus_16" : [int, [1, 8], [], 1],
    "set_resource_constraint unsigned_modulus_32" : [int, [1, 8], [], 1],
    "set_resource_constraint unsigned_modulus_64" : [int, [1, 8], [], 1],
    "set_resource_constraint unsigned_add_8" : [int, [1, 8], [], 1],
    "set_resource_constraint unsigned_add_16" : [int, [1, 8], [], 1],
    "set_resource_constraint unsigned_add_32" : [int, [1, 8], [], 1],
    "set_resource_constraint unsigned_add_64" : [int, [1, 8], [], 1],
    "set_resource_constraint altfp_add_8" : [int, [1, 8], [], 1],
    "set_resource_constraint altfp_add_16" : [int, [1, 8], [], 1],
    "set_resource_constraint altfp_add_32" : [int, [1, 8], [], 1],
    "set_resource_constraint altfp_add_64" : [int, [1, 8], [], 1],
    "set_resource_constraint altfp_subtract_8" : [int, [1, 8], [], 1],
    "set_resource_constraint altfp_subtract_16" : [int, [1, 8], [], 1],
    "set_resource_constraint altfp_subtract_32" : [int, [1, 8], [], 1],
    "set_resource_constraint altfp_subtract_64" : [int, [1, 8], [], 1],
    "set_resource_constraint altfp_multiply_8" : [int, [1, 8], [], 1],
    "set_resource_constraint altfp_multiply_16" : [int, [1, 8], [], 1],
    "set_resource_constraint altfp_multiply_32" : [int, [1, 8], [], 1],
    "set_resource_constraint altfp_multiply_64" : [int, [1, 8], [], 1],
    "set_resource_constraint altfp_divide_8" : [int, [1, 8], [], 1],
    "set_resource_constraint altfp_divide_16" : [int, [1, 8], [], 1],
    "set_resource_constraint altfp_divide_32" : [int, [1, 8], [], 1],
    "set_resource_constraint altfp_divide_64" : [int, [1, 8], [], 1],
    "set_operation_latency altfp_add_8" : [int, [0, 8], [], 14],
    "set_operation_latency altfp_add_16" : [int, [0, 8], [], 14],
    "set_operation_latency altfp_add_32" : [int, [0, 8], [], 14],
    "set_operation_latency altfp_add_64" : [int, [0, 8], [], 14],
    "set_operation_latency altfp_subtract_8" : [int, [0, 8], [], 14],
    "set_operation_latency altfp_subtract_16" : [int, [0, 8], [], 14],
    "set_operation_latency altfp_subtract_32" : [int, [0, 8], [], 14],
    "set_operation_latency altfp_subtract_64" : [int, [0, 8], [], 14],
    "set_operation_latency altfp_multiply_8" : [int, [0, 8], [], 11],
    "set_operation_latency altfp_multiply_16" : [int, [0, 8], [], 11],
    "set_operation_latency altfp_multiply_32" : [int, [0, 8], [], 11],
    "set_operation_latency altfp_multiply_64" : [int, [0, 8], [], 11],
    "set_operation_latency altfp_divide_8" : [int, [0, 8], [], 33],
    "set_operation_latency altfp_divide_16" : [int, [0, 8], [], 33],
    "set_operation_latency altfp_divide_32" : [int, [0, 8], [], 33],
    "set_operation_latency altfp_divide_64" : [int, [0, 8], [], 64],
    "set_operation_latency altfp_truncate_8" : [int, [0, 8], [], 3],
    "set_operation_latency altfp_truncate_16" : [int, [0, 8], [], 3],
    "set_operation_latency altfp_truncate_32" : [int, [0, 8], [], 3],
    "set_operation_latency altfp_truncate_64" : [int, [0, 8], [], 3],
    "set_operation_latency altfp_extend_8" : [int, [0, 8], [], 2],
    "set_operation_latency altfp_extend_16" : [int, [0, 8], [], 2],
    "set_operation_latency altfp_extend_32" : [int, [0, 8], [], 2],
    "set_operation_latency altfp_extend_64" : [int, [0, 8], [], 2],
    "set_operation_latency altfp_fptosi" : [int, [0, 8], [], 6],
    "set_operation_latency altfp_sitofp" : [int, [0, 8], [], 6],
    "set_operation_latency signed_comp_o" : [int, [0, 8], [], 1],
    "set_operation_latency signed_comp_u" : [int, [0, 8], [], 1],
    "set_operation_latency reg" : [int, [0, 8], [], 2],
    "set_operation_latency mem_dual_port" : [int, [0, 8], [], 2],
    "set_operation_latency local_mem_dual_port" : [int, [0, 8], [], 1],
    "set_operation_latency signed_divide_8" : [int, [0, 8], [], 1],
    "set_operation_latency signed_divide_16" : [int, [0, 8], [], 1],
    "set_operation_latency signed_divide_32" : [int, [0, 8], [], 1],
    "set_operation_latency signed_divide_64" : [int, [0, 8], [], 1],
    "set_operation_latency signed_multiply_8" : [int, [0, 8], [], 1],
    "set_operation_latency signed_multiply_16" : [int, [0, 8], [], 1],
    "set_operation_latency signed_multiply_32" : [int, [0, 8], [], 1],
    "set_operation_latency signed_multiply_64" : [int, [0, 8], [], 1],
    "set_operation_latency signed_modulus_8" : [int, [0, 8], [], 1],
    "set_operation_latency signed_modulus_16" : [int, [0, 8], [], 1],
    "set_operation_latency signed_modulus_32" : [int, [0, 8], [], 1],
    "set_operation_latency signed_modulus_64" : [int, [0, 8], [], 1],
    "set_operation_latency signed_add_8" : [int, [0, 8], [], 1],
    "set_operation_latency signed_add_16" : [int, [0, 8], [], 1],
    "set_operation_latency signed_add_32" : [int, [0, 8], [], 1],
    "set_operation_latency signed_add_64" : [int, [0, 8], [], 1],
    "set_operation_latency unsigned_divide_8" : [int, [0, 8], [], 1],
    "set_operation_latency unsigned_divide_16" : [int, [0, 8], [], 1],
    "set_operation_latency unsigned_divide_32" : [int, [0, 8], [], 1],
    "set_operation_latency unsigned_divide_64" : [int, [0, 8], [], 1],
    "set_operation_latency unsigned_multiply_8" : [int, [0, 8], [], 1],
    "set_operation_latency unsigned_multiply_16" : [int, [0, 8], [], 1],
    "set_operation_latency unsigned_multiply_32" : [int, [0, 8], [], 1],
    "set_operation_latency unsigned_multiply_64" : [int, [0, 8], [], 1],
    "set_operation_latency unsigned_modulus_8" : [int, [0, 8], [], 1],
    "set_operation_latency unsigned_modulus_16" : [int, [0, 8], [], 1],
    "set_operation_latency unsigned_modulus_32" : [int, [0, 8], [], 1],
    "set_operation_latency unsigned_modulus_64" : [int, [0, 8], [], 1],
    "set_operation_latency unsigned_add_8" : [int, [0, 8], [], 1],
    "set_operation_latency unsigned_add_16" : [int, [0, 8], [], 1],
    "set_operation_latency unsigned_add_32" : [int, [0, 8], [], 1],
    "set_operation_latency unsigned_add_64" : [int, [0, 8], [], 1],
}

def parameter_type(name):
    return parameters[name][0]

def parameter_values(name):
    return [True, False] if parameters[name][0] == bool else parameters[name][1]

def generate_file(configuration, path):
    filename = "{0}/config.tcl".format(path)
    text     = "source ../config.tcl\n"
    text    += "set_parameter LOCAL_RAMS 1\n"
    text    += "set_parameter GROUP_RAMS 1\n"
    text    += "set_parameter GROUP_RAMS_SIMPLE_OFFSET 1\n"
    text    += "set_parameter CASE_FSM 1\n"
    file     = open("{0}".format(filename), "w+")
    for name in parameters:
        if parameter_type(name) == bool:
            value = "1" if configuration[name] else "0"
        else:
            value = str(configuration[name])

        text += "{0} {1}\n".format(name, value)
    file.write(text)
    file.close()
    return filename

def generate_seed():
    seed = {}
    for name in parameters:
        seed[name] = parameters[name][-1]

    file = open("seed.json", "w+")
    json.dump(seed, file)
    file.close()

def get_dependencies(name, index):
    deps = ""
    for dep in parameters[name][index]:
        deps += " {0}".format(dep)

    return str.strip(deps)

def get_values(name, index):
    return get_dependencies(name, index)

def export_to_json():
    file = open("legup_parameters.json", "w+")
    file.write("{\"legup_parameters\":[\n")

    last = parameters.keys()[-1]

    for name in parameters:
        file.write("    {{\n        \"name\":\"{0}\",\n".format(name))
        name_type = parameters[name][0]
        file.write("        \"type\":\"{0}\",\n".format(str(name_type).split("'")[1]))
        if name_type == bool:
            deps = get_dependencies(name, 1)
            file.write("        \"dependencies\":\"{0}\",\n".format(deps))
            file.write("        \"default\":\"{0}\"\n".format(parameters[name][2]))
        elif name_type == Enum:
            vals = get_values(name, 1)
            file.write("        \"values\":\"{0}\",\n".format(vals))
            deps = get_dependencies(name, 2)
            file.write("        \"dependencies\":\"{0}\",\n".format(deps))
            file.write("        \"default\":\"{0}\"\n".format(parameters[name][3]))
        else:
            file.write("        \"min\":\"{0}\",\n".format(parameters[name][1][0]))
            file.write("        \"max\":\"{0}\",\n".format(parameters[name][1][1]))
            deps = get_dependencies(name, 2)
            file.write("        \"dependencies\":\"{0}\",\n".format(deps))
            file.write("        \"default\":\"{0}\"\n".format(parameters[name][3]))

        if name != last:
            file.write("    },\n")
        else:
            file.write("    }\n")

    file.write("]}")

    file.close()

if __name__ == "__main__":
    export_to_json()
