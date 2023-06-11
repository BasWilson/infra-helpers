from functools import reduce
import os
import yaml

from infra_helpers.paths import GetInfraPath

yaml.Dumper.ignore_aliases = lambda *args: True


def StoreState(state):
    with open("{}/state/state.yaml".format(GetInfraPath()), "w") as yaml_file:
        yaml.dump(state, yaml_file, default_flow_style=False)


def GetState():
    state = None
    try:
        with open("{}/state/state.yaml".format(GetInfraPath()), "r") as stream:
            state = yaml.safe_load(stream)
    except:
        state = {}
    return state


def GetValueFromState(state, resourceId, key):
    return state[resourceId][key]


def deep_get(dictionary, keys, default=None):
    return reduce(
        lambda d, key: d.get(key, default) if isinstance(d, dict) else default,
        keys.split("."),
        dictionary,
    )


def extract_variables_from_string(string):
    variable = string[string.find("${") + 2 : string.find("}")]
    if variable != None:
        foundValue = deep_get(GetState(), variable, os.getenv(variable))

        if foundValue == None:
            return string

        return foundValue


def GetResourceValue(resource, key, default=None):
    if key in resource:
        strValue = str(resource[key])
        if strValue.find("${") != -1 and strValue.find("}") != -1:
            if isinstance(resource[key], list):
                return [extract_variables_from_string(item) for item in resource[key]]
            elif isinstance(resource[key], dict):
                return {
                    k: extract_variables_from_string(v)
                    for k, v in resource[key].items()
                }
            else:
                return extract_variables_from_string(resource[key])

        # no variables found, return the value
        return resource[key]
    else:
        return default
