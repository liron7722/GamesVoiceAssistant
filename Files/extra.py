import os
import json


def readJson(path, filename):
    with open(path + '/' + filename) as json_file:
        data = json.load(json_file)
    return data


def writeJson(path, filename, data):
    with open(path + '/' + filename, 'w') as outfile:
        json.dump(data, outfile, indent=4)


def get_path():
    return os.path.abspath(os.getcwd())
