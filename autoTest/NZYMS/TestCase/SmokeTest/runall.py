import os
import sys

import pytest
sys.path.append(os.path.join(os.getcwd(), "../../../"))
from Commons import allurechange


if __name__ == '__main__':
    pytest.main(['-sv','--alluredir', '../../report/result', "--clean-alluredir"])


    '''
    pytest.main([
                 #'../SmokeTest/test_01_goin_box_process.py',
                 #'../SmokeTest/test_02_changeStoreProcess.py',
                # '../SmokeTest/test_changeBox.py',
                 #'../SmokeTest/test_checkplan.py',
                #'../SmokeTest/test_bulkcargointostorage.py',
                # '../SmokeTest/test_bulkcargooutstorage.py',
                # '../SmokeTest/test_packingplan.py',
                # '../SmokeTest/test_splitboxplan.py',
                 '../SmokeTest/test_outplan.py',
                 '-sv','--alluredir', '../report/result', "--clean-alluredir"])
    '''

    os.system('allure generate ../../report/result -o ../../report/html --clean')
    allurechange.set_windos_title('集疏运UI自动化测试')
    report_title = allurechange.get_json_data("集疏运测试报告")
    allurechange.write_json_data(report_title)