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