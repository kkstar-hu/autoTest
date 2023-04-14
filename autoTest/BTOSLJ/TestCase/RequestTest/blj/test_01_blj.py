# -*- coding:utf-8 -*-
import os
import allure
import pytest
from BTOSLJ.PageObject.blj.workhour import WorkHour
from BTOSLJ.PageObject.blj.ioa_by_goodstype import InterfaceRes
from Commons.jsonread import read_json


@allure.story('罗泾报表一期')
@allure.title('1.昼夜工时表')
def test_workhuor(host):
    schema = read_json(os.path.join(os.getcwd(), 'workhour.json'))
    b = WorkHour(host)
    b.test_type(schema)
    b.test_params_01(schema)
    b.test_params_02(schema)
    b.test_no_params(schema)

@allure.title('2.分货类进出存日报表')
def test_ioa_by_goodstype_day(host):
    schema = read_json(os.path.join(os.getcwd(), 'ioa_by_goodstype_day.json'))
    b = InterfaceRes(host)
    b.test_ioabygoodstype_day(schema)

