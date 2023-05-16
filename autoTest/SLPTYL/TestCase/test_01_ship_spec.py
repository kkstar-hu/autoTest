import os
import allure
import pytest
from pytest_check import check
from Commons.operateJson import read_json
import Commons.yamlread as yamlread
from SLPTYL.PageObject.standardData.interface_req import InterfaceReq

@allure.story('一、标准化数据')
@allure.title('1.新增船舶')
def test_add_vessel(server_host):
    schema=yamlread.get_api_info('新增船舶规范报文',os.path.abspath(os.path.dirname(os.getcwd()))+'/Data/standardData.yaml')
    with allure.step("接口请求"):
        req = InterfaceReq(server_host)
        req.req_add_ship_spec(schema)
    with allure.step("数据库请求"):#TODO
        pass






