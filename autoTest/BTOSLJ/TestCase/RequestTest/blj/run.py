# -*- coding:utf-8 -*-
import os
import pytest
import urllib3

from Commons import allurechange

if __name__ == '__main__':
    pytest.main(['-sv','--alluredir', 'Report/result', "--clean-alluredir"])


    #urllib3.disable_warnings()
    os.system('allure generate Report/result -o Report/html --clean')
    allurechange.set_windos_title('罗泾BTOS3.0接口自动化测试')
    report_title = allurechange.get_json_data("罗泾BTOS3.0接口测试报告")
    allurechange.write_json_data(report_title)