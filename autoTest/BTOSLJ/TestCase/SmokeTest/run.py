# -*- coding:utf-8 -*-
import os
import pytest
import urllib3

from Commons import allurechange

if __name__ == '__main__':
    #pytest.main(['-sv','--alluredir', '../report/result', "--clean-alluredir"])


    pytest.main(['-sv', '01_ShipSchedule/test_AddShipSchedule.py',
                 '--alluredir', '../../Report/result', "--clean-alluredir"])

    #urllib3.disable_warnings()
    os.system('allure generate ../../Report/result -o ../../Report/html --clean')
    allurechange.set_windos_title('罗泾BTOS3.0自动化测试')
    report_title = allurechange.get_json_data("罗泾BTOS3.0测试报告")
    allurechange.write_json_data(report_title)

