
import json

def read_json(name):
    with open(name,'r', encoding='utf-8') as f:
        b = json.loads(f.read())
        return b


