import os
import json


def loadJSON(filepath):
    if os.path.exists(filepath) == False:
        raise Exception('File at {} does not exist'.format(filepath))
    with open(filepath) as data:
        return json.load(data)
