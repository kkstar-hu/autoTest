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
                 '../SmokeTest_BigShip/test_Big01_DataProcess.py',
                 '../SmokeTest_BigShip/test_Big02_DischargingProcess.py',
                 '../SmokeTest_BigShip/test_Big03_PackingProcess.py',
                 '../SmokeTest_BigShip/test_Big04_EnterBoxProcess.py',
                 '../SmokeTest_BigShip/test_Big05_LadeShipProcess.py',
                 '../SmokeTest_BigShip/test_Big06_DirectLiftingProcess.py',
                 '../SmokeTest_BigShip/test_Big07_DirectLoadingProcess.py',
                 # '../SmokeTest_BigShip/test_Big08_OverShip.py',
                 '--alluredir', '../../report/result', "--clean-alluredir"])


    os.system('allure generate ../../report/result -o ../../report/html --clean')
    allurechange.set_windos_title('阳逻港GTOS自动化测试')
    report_title = allurechange.get_json_data("阳逻港GTOS测试报告")
    allurechange.write_json_data(report_title)

