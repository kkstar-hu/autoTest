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
                 # '../empty_box_test/test_01_DischargingProcess.py',
                 '../empty_box_test/test_02_DataProcess.py',
                 '--alluredir', '../../report/result', "--clean-alluredir"])

    os.system('allure generate ../../report/result -o ../../report/html --clean')
    allurechange.set_windos_title('厦门GTOS自动化测试')
    report_title = allurechange.get_json_data("厦门GTOS测试报告")
    allurechange.write_json_data(report_title)
