#! /usr/bin/python

import json

parameters = {}

with open("seed.json") as json_data:
    data = json.load(json_data)

    for key in data.keys():
        if len(key.split()) > 1:
            param_type = key.split()[0]
            param = key.split()[1]

            if param_type not in parameters.keys():
                parameters[param_type] = []

            if param.split("_")[-1] in ["8", "16", "32", "64"]:
                if "_".join(param.split("_")[:-1]) not in parameters[param_type]:
                    parameters[param_type].append("_".join(param.split("_")[:-1]))
            else:
                parameters[param_type].append(param)
        else:
            if "set_parameter" not in parameters.keys():
                parameters["set_parameter"] = []

            parameters["set_parameter"].append(key.upper())

print("\\begin{table}[htpb]")
print("\\centering")
print("\\begin{tabular}{@{}p{0.14\columnwidth}p{0.72\columnwidth}@{}}")
print("\\toprule")
print("Type & \\multicolumn{1}{c}{Parameters} \\\\ \\midrule")

ending = "\\\\"

for param_type in parameters.keys():
    title = ""

    if param_type == "set_parameter":
        title = "Boolean or Multi-Valued"
    elif param_type == "set_operation_latency":
        title = "Operation Latency"
    elif param_type == "set_resource_constraint":
        title = "Resource Constraint"

    line = title + " & \\tiny{"

    for param in parameters[param_type]:
        line += "\\texttt{" + param.replace("_", "\\_") + "}"
        if param != parameters[param_type][-1]:
            line += ", "

    line += "} "

    if param_type == "set_parameter":
        ending = "\\\\ \\bottomrule"

    line += ending

    print(line)

print("\\addlinespace{}")
print("\\end{tabular}")
print("\\caption{Subset of All Autotuned LegUP HLS Parameters}")
print("\\label{tab:params}")
print("\\end{table}")
