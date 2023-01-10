import pytest
from Base.basepage import BasePage
import pytest_check as check

from GTOS.Controls.Gtos_table import Gtos_table
from GTOS.Controls.text import Gtos_text
from GTOS.PageObject.gtos_menu import GtosMenu




def testAddGoInPlan_BoxNumber(driver):
    menu = GtosMenu(driver)
    menu.select_level_Menu("系统管理,用户管理V1")

    test=Gtos_text(driver)
    b=test.get_attribute_info("xpath","//form[@class='el-form']//label[contains(text(),'用户状态')]//following-sibling::div//input",'innerText')
    check.equal(b, "正常")
    #table=Gtos_table(driver)
    #a=table.get_value("用户账号")
    #check.equal(table.get_value("用户账号"), "CTEST01")


if __name__ == '__main__':
    pytest.main(['-v'])
