import os
import sys

import pytest
sys.path.append(os.path.join(os.getcwd(), "../../../"))
from Commons import allurechange


if __name__ == '__main__':
    pytest.main(['test_07_bulkcargointostorage.py','-sv','--alluredir', '../../report/result', "--clean-alluredir"])


    '''
    pytest.main([
                 #'test_01_goin_box_process.py',
                 #'test_02_changeStoreProcess.py',
                 #'test_03_changeBox.py',
                 #'test_04_checkplan.py',
                 #'test_05_lockbox.py',
                 # test_06_outplan.py'
                 #'test_07_bulkcargointostorage.py',
                 # test_08_bulkcargooutstorage.py',
                 # test_09_packingplan.py',
                 # test_10_splitboxplan.py',
                 '-sv','--alluredir', '../../report/result', "--clean-alluredir"])
    '''

    os.system('allure generate ../../report/result -o ../../report/html --clean')
    allurechange.set_windos_title('集疏运UI自动化测试')
    report_title = allurechange.get_json_data("集疏运测试报告")
    allurechange.write_json_data(report_title)