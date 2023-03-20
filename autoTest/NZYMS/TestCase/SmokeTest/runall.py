import os
import sys

import pytest
sys.path.append(os.path.join(os.getcwd(), "../../../"))
from Commons import allurechange


if __name__ == '__main__':
    pytest.main(['-sv','--alluredir', '../../report/result', "--clean-alluredir"])


    '''
    pytest.main([
                 #'../SmokeTest/01_goinboxprocess/test_01_goin_box_process.py',
                 #'../SmokeTest/02_changeStoreProcess/test_02_changeStoreProcess.py',
                # '../SmokeTest/03_changeBoxProcess/test_changeBox.py',
                 #'../SmokeTest/04_checkboxprocess/test_checkplan.py',
                #'../SmokeTest/06_bulkcargointostorage/test_bulkcargointostorage.py',
                # '../SmokeTest/07_bulkcargooutstorage/test_bulkcargooutstorage.py',
                # '../SmokeTest/08_packingboxprocess/test_packingplan.py',
                # '../SmokeTest/09_solitboxprocess/test_splitboxplan.py',
                 '../SmokeTest/10_outboxprocess/test_outplan.py',
                 '-sv','--alluredir', '../../report/result', "--clean-alluredir"])
    '''

    os.system('allure generate ../../report/result -o ../../report/html --clean')
    allurechange.set_windos_title('集疏运UI自动化测试')
    report_title = allurechange.get_json_data("集疏运测试报告")
    allurechange.write_json_data(report_title)