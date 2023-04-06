import os
import pytest
import os
import sys
sys.path.append(os.path.join(os.getcwd(), "../../../"))

from Commons import allurechange

if __name__ == '__main__':
    # pytest.main(['-sv','--alluredir', '../../report/result', "--clean-alluredir"])

    pytest.main(['-sv',
                 # '../smoke_test/test_01_DataProcess.py',
                 '../smoke_test/test_02_DischargingProcess.py',
                 '../smoke_test/test_03_PackingProcess.py',
                 '../smoke_test/test_04_EnterBoxProcess.py',
                 '../smoke_test/test_05_LadeShipProcess.py',
                 '../smoke_test/test_06_DirectLiftingProcess.py',
                 '../smoke_test/test_07_DirectLoadingProcess.py',
                 # '../smoke_test/test_08_OverShip.py',
                 '--alluredir', '../../report/result', "--clean-alluredir"])



    os.system('allure generate ../../report/result -o ../../report/html --clean')
    allurechange.set_windos_title('阳逻港GTOS自动化测试')
    report_title = allurechange.get_json_data("阳逻港GTOS测试报告")
    allurechange.write_json_data(report_title)

