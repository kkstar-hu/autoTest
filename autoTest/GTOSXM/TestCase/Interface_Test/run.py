import json
import os

from Base.baseinterface import RequestHandler
from Commons.operateJson import read_json
from Commons.yamlread import read_yaml

# a = read_yaml('interface.yaml')
# print(a)
# b = read_yaml(r'D:\ATA\autoTest\GTOS\TestCase\smoke_test\01_DataProcess\immediata_plan.yaml')
# print(type(b))
# print(b[0]['船舶代码'])
body = read_json(r'D:\ATA\autoTest\GTOS\TestCase\Interface_Test\JSOn\cangdan.json')
print(body)
# print(type(body['goodsList']))
# req = RequestHandler()
# c = req.visit('post',url = a['url'], json = b,)
# print(c.json())