import os

from Commons.yamlread import read_yaml

a = read_yaml((os.path.join('../Interface_Test/interface.yaml')))['url'] + read_yaml((os.path.join('../Interface_Test/interface.yaml')))['配载']
print(a)