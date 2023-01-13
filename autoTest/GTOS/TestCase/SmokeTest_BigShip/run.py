import os
import pytest
import urllib3

from Commons import allurechange

if __name__ == '__main__':
    pytest.main(['-sv','../SmokeTest/02_DischargingProcess/tesDischargingProcess.py',
                        '../SmokeTest/03_PackingProcess/testPackingProcess.py',
                        '../SmokeTest/07_DirectLoadingProcess/testDirectLoadingProcess.py',
                 '--alluredir', '../../report/result', "--clean-alluredir"])

    # pytest.main(['-sv','../SmokeTest/07_DirectLoadingProcess/testDirectLoadingProcess.py',
    #              '--alluredir', '../../report/result', "--clean-alluredir"])
    urllib3.disable_warnings()
    os.system('allure generate ../../report/result -o ../../report/html --clean')
    allurechange.set_windos_title('阳逻港GTOS自动化测试')
    report_title = allurechange.get_json_data("阳逻港GTOS测试报告")
    allurechange.write_json_data(report_title)

