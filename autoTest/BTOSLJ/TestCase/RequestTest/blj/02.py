import os

from Commons.jsonread import load_json

a = load_json(os.path.join(os.getcwd(), 'workhour.json'))
print(a)