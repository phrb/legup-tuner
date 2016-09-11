import JSON

@everywhere begin
    using StochasticSearch

    function generate_file(config::Configuration, path::AbstractString)
        filename = "$path/config.tcl"

        text     = "source ../config.tcl\n"
        text     = string(text, "set_parameter LOCAL_RAMS 1\n")
        text     = string(text, "set_parameter GROUP_RAMS 1\n")
        text     = string(text, "set_parameter GROUP_RAMS_SIMPLE_OFFSET 1\n")
        text     = string(text, "set_parameter CASE_FSM 1\n")

        file     = open("$filename", "w+")

        for parameter in values(config.parameters)
            value::AbstractString
            name::AbstractString = parameter.name
            if typeof(parameter) == BoolParameter
                if parameter.value
                    value = "1"
                else
                    value = "0"
                end
            else
                value = string(parameter.value)
            end
            text = string(text, "$name $value\n")
        end

        write(file, text)
        close(file)
        return filename
    end

    function get_wallclock_time(config::Configuration, parameters::Dict{Symbol, Any})
        application      = "dfadd"
        verilog_file     = "dfadd.v"
        application_path = "legup_src/legup-4.0/examples/chstone/$application"
        container_path   = "/root/legup_src/legup-4.0/examples/chstone/$application/tuner"
        host_path        = "/home/phrb/code/legup-tuner/post_place_and_route/jl"
        image_name       = "legup_ubuntu"
        script_name      = "measure.sh"

        penalty          = Inf

        unique_id        = Base.Random.uuid4()

        unique_host_path = "$host_path/$unique_id"

        mkdir(unique_host_path)

        cp(script_name, "$unique_host_path/$script_name")

        filename = generate_file(config, unique_host_path)

        docker_cmd = `docker run --rm -w $container_path
                      -v $unique_host_path:$container_path -i $image_name
                      /bin/bash -c 'chmod +x '$script_name' && './$script_name' '$unique_id' '$verilog_file''`

        try begin
            output = split(readall(docker_cmd))

            cycles            = parse(Float64, output[1])
            cycles_per_second = parse(Float64, output[2])
            factor            = 1000.

            rm(unique_host_path, recursive = true)

            return cycles * (factor / cycles_per_second)
        end
        catch
            rm(unique_host_path, recursive = true)
            return penalty
        end
    end
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

best_log = open("best_log.txt", "w+")

parameters    = load_parameters()
configuration = Configuration(parameters, "legup_parameters")

tuning_run = Run(cost               = get_wallclock_time,
                 starting_point     = configuration,
                 methods            = [[:simulated_annealing 1];
                                       [:iterative_first_improvement 1];
                                       [:randomized_first_improvement 1];],
                 stopping_criterion  = elapsed_time_criterion,
                 duration            = 5400,
                 reporting_criterion = elapsed_time_reporting_criterion,
                 report_after        = 250)

search_task = @task optimize(tuning_run)

result = consume(search_task)
print("$(result.current_time) $(result.cost_minimum)\n")
write(best_log, "$(result.current_time) $(result.cost_minimum)\n")

while result.is_final == false
    result = consume(search_task)
    print("$(result.current_time) $(result.cost_minimum)\n")
    write(best_log, "$(result.current_time) $(result.cost_minimum)\n")
end
