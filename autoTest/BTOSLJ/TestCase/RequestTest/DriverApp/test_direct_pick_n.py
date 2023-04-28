# -*- coding:utf-8 -*-
import os
import allure
import pytest
from pytest_check import check
from BTOSLJ.PageObject.blj.workhour import WorkHour
from BTOSLJ.PageObject.blj.interface_res import InterfaceRes
from Commons.jsonread import read_json
from BTOSLJ.PageObject.blj.db_operate import DataRes