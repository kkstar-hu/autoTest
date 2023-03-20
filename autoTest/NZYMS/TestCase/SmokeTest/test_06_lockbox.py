import os

import allure
import pytest as pytest
from Commons.Controls.tag import Tag
from Commons.menu import Menu
from Commons.yamlread import read_yaml
from NZYMS.PageObject.BoxManagement.lockbox import LockBox


#@pytest.mark.skip
@allure.title('高级锁箱管理中加高级锁、解高级锁、加普通锁、解普通锁')
@allure.story('5.锁箱流程')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'05_lockboxprocess','lockbox.yaml')))
def testlockbox(driver, input):
    menu=Menu(driver)
    menu.select_level_Menu("箱务管理,集装箱管理,高级锁箱管理")
    lockbox=LockBox(driver)
    lockbox.search(input)
    lockbox.checkboxInformation(input)
    lockbox.lockbox(input)
    lockbox.unlockbox(input)
    lockbox.superlockbox(input)
    lockbox.unlockbox(input)
    Tag(driver).closeTag("高级锁箱管理")
    driver.refresh()












if __name__ == '__main__':
    pytest.main(['-vs','--alluredir','../allure-result'])
    #os.system('allure generate ../allure-result -o ../reports')