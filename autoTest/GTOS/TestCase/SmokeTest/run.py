import os
import pytest
import urllib3
import os
import sys
sys.path.append(os.path.join(os.getcwd(), "../../../"))

from Commons import allurechange

if __name__ == '__main__':
    pytest.main(['-sv','--alluredir', '../../report/result', "--clean-alluredir"])

    '''
    pytest.main(['-sv', '../SmokeTest/01_DataProcess/test_DataProcess.py',
                 '../SmokeTest/02_DischargingProcess/test_DischargingProcess.py',
                 '../SmokeTest/03_PackingProcess/test_PackingProcess.py',
                 '../SmokeTest/04_EnterBoxProcess/test_EnterBoxProcess.py',
                 '../SmokeTest/05_PutBoxIntoShipProcess/test_LadeShipProcess.py',
                 '../SmokeTest/06_DirectLiftingProcess/test_DirectLiftingProcess.py',
                 '../SmokeTest/07_DirectLoadingProcess/test_DirectLoadingProcess.py',
                 '../SmokeTest/08_OverShip/test_OverShip.py',
                 '--alluredir', '../../report/result', "--clean-alluredir"])
    '''
    #urllib3.disable_warnings()
    os.system('allure generate ../../report/result -o ../../report/html --clean')
    allurechange.set_windos_title('阳逻港GTOS自动化测试')
    report_title = allurechange.get_json_data("阳逻港GTOS测试报告")
    allurechange.write_json_data(report_title)

