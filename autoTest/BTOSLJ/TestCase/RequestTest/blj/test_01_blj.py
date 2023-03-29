# -*- coding:utf-8 -*-
import os
import time
import allure
import pytest
from BTOSLJ.PageObject.blj.workhour import Blj


@allure.story('一、内贸进口流程')
@allure.title('1.新增船期')
def test_workhuor(host):
    b = Blj(host)
    b.test_type()
    b.test_params_01()
    b.test_params_02()
    b.test_no_params()