# -*- coding:utf-8 -*-
import os
import pytest
import urllib3
import platform

from Commons import allurechange

if __name__ == '__main__':
    #pytest.main(['-sv','--alluredir', 'Report/result'])
    pytest.main(['-sv','--alluredir', 'Report/result', "--clean-alluredir"])

    #urllib3.disable_warnings()
    environment = {
        "device-name": platform.node(),
        "operating-system": platform.platform(),
        "python version": platform.python_version(),
        "server host": "10.116.8.16:8520",
        "database host": "10.116.8.20"
    }
    allurechange.set_environment(environment)
    #os.system('allure generate Report/result -o Report/html')
    os.system('allure generate Report/result -o Report/html --clean')
    allurechange.set_windos_title('罗泾BTOS3.0接口自动化测试')
    report_title = allurechange.get_json_data("罗泾BTOS3.0接口测试报告")
    allurechange.write_json_data(report_title)
