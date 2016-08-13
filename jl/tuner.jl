import JSON

@everywhere begin
    using StochasticSearch
end

function load_parameters()
    json_parameters = JSON.parsefile("legup_parameters.json"; dicttype=Dict)

    parameters::Array{Parameter, 1}
    parameters = []

    for parameter in json_parameters["legup_parameters"]
        p_type = parameter["type"]
        if p_type == "int"
            push!(parameters, IntegerParameter(parse(Int, parameter["min"]),
                                               parse(Int, parameter["max"]),
                                               parse(Int, parameter["default"]),
                                               parameter["name"]))
        elseif p_type == "bool"
            value = false
            if parameter["default"] == "True"
                value = true
            end
            push!(parameters, BoolParameter(value,
                                            parameter["name"]))
        elseif p_type == "Enum"
            values = []
            for val in split(parameter["values"])
                push!(values, StringParameter(val, val))
            end
            push!(parameters, EnumParameter(values,
                                            findfirst(split(parameter["values"]),
                                                      parameter["default"]),
                                            parameter["name"]))
        else
            println("ERROR: No such type")
            exit()
        end
    end
    return parameters
end

parameters    = load_parameters()
configuration = Configuration(parameters, "legup_parameters")
