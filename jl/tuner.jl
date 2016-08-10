import JSON

@everywhere begin
    using StochasticSearch
end

json_parameters = JSON.parsefile("legup_parameters.json"; dicttype=Dict)

parameters = []

print(typeof(json_parameters))

print(json_parameters["legup_parameters"])

for parameter in json_parameters.second
    print(parameter)
end
