# -*- coding:utf-8 -*-
import os
import time

import allure
import pytest
from BTOSLJ.Config.config import mydata
from BTOSLJ.Controls.BTOS_menu import BtosMenu
from Commons.yamlread import read_yaml
from BTOSLJ.PageObject.ShipSchedule.ShipDateManage import ShipDate



@allure.story('一、内贸进口流程')
@allure.title('1.新增船期')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '01_ShipSchedule', 'ShipSchedule.yaml')))
def test_Add_ShipSchedule(driver, input : dict):
    print("******************************************Smoke Test Start***********************************************")
    menu = BtosMenu(driver)
    menu.select_level2_menu("船期管理","船期管理")

    schedule = ShipDate(driver)
    schedule.add_schedule(input)
    schedule.check_schedule(input)
    schedule.confirm_arrive(input)
    schedule.divide_region(input)


@allure.story('一、内贸进口流程')
@allure.title('2.新增靠泊计划')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), '01_ShipSchedule', 'BerthPlan.yaml')))
def test_Add_BerthPlan(driver, input : dict):
    schedule = ShipDate(driver)
    schedule.add_berth_plan(input)

