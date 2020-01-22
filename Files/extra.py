import os
import json

COLOR_File = 'voice_assistant_status.txt'


def readJson(path, filename):
    with open(path + '/' + filename) as json_file:
        data = json.load(json_file)
    return data


def writeJson(path, filename, data):
    with open(path + '/' + filename, 'w') as outfile:
        json.dump(data, outfile, indent=4)


def get_path():
    return os.path.abspath(os.getcwd())


def change_status(color):
    with open(COLOR_File, 'w') as file:
        file.write(color)
        file.close()

change_status('red')