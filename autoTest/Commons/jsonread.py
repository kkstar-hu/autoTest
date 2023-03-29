import json


def read_json(name):
    with open(name,'r') as f:
        b = json.loads(f.read())
        return b

