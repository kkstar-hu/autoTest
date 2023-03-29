# -*- coding:utf-8 -*-
import os
import time
import allure
import pytest
from BTOSLJ.PageObject.blj.workhour import WorkHour
from BTOSLJ.PageObject.blj.ioa_by_goodstype import IoaByGoodsTypeDay, IoaByGoodsTypeMonth
from Commons.jsonread import read_json



@allure.story('一、内贸进口流程')
@allure.title('1.新增船期')
def test_workhuor(host):
    schema = read_json(os.path.join(os.getcwd(), 'workhour.json'))
    b = WorkHour(host)
    b.test_type(schema)
    b.test_params_01(schema)
    b.test_params_02(schema)
    b.test_no_params(schema)

def test_ioa_by_goodstype_day(host):
    schema = read_json(os.path.join(os.getcwd(), 'ioa_by_goodstype_day.json'))
    b = IoaByGoodsTypeDay(host)
    b.test_type(schema)

def test_ioa_by_goodstype_month(host):
    schema = read_json(os.path.join(os.getcwd(), 'ioa_by_goodstype_month.json'))
    b = IoaByGoodsTypeMonth(host)
    b.test_type(schema)