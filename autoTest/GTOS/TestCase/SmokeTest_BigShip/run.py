import os
import pytest
import os
import sys
sys.path.append(os.path.join(os.getcwd(), "../../../"))
from Commons import allurechange
import warnings
warnings.filterwarnings("ignore")
if __name__ == '__main__':
    # pytest.main(['-sv','--alluredir', '../../report/result', "--clean-alluredir"])
    pytest.main(['-sv',
                 # '../SmokeTest_BigShip/01_DataProcess/test_DataProcess.py',
                 '../SmokeTest_BigShip/02_DischargingProcess/test_DischargingProcess.py',
                 '../SmokeTest_BigShip/03_PackingProcess/test_PackingProcess.py',
                 '../SmokeTest_BigShip/04_EnterBoxProcess/test_EnterBoxProcess.py',
                 '../SmokeTest_BigShip/05_PutBoxIntoShipProcess/test_LadeShipProcess.py',
                 # '../SmokeTest_BigShip/06_DirectLiftingProcess/test_DirectLiftingProcess.py',
                 # '../SmokeTest_BigShip/07_DirectLoadingProcess/test_DirectLoadingProcess.py',
                 # '../SmokeTest_BigShip/08_OverShip/test_OverShip.py',
                 '--alluredir', '../../report/result', "--clean-alluredir"])



    os.system('allure generate ../../report/result -o ../../report/html --clean')
    allurechange.set_windos_title('阳逻港GTOS自动化测试')
    report_title = allurechange.get_json_data("阳逻港GTOS测试报告")
    allurechange.write_json_data(report_title)

