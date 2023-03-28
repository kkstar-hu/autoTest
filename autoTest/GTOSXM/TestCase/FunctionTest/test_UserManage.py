import os.path

import allure
import pytest

from Commons.Controls.tag import Tag
from Commons.yamlread import read_yaml
from GTOSXM.PageObject.User_Manage.user_add import User_Manage
from GTOSXM.PageObject.gtos_menu import GtosMenu


@allure.story('1.系统管理')
@allure.title('3、用户管理')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'user_manage','user_data.yaml')))
def testUserManage01UserAdd(driver, input):
    """添加用户"""
    print("******************************************Test Add User***********************************************")
    #菜单跳转
    menu = GtosMenu(driver)
    menu.select_level_Menu("系统管理,用户管理")
    #新增用户
    userManager = User_Manage(driver)
    userManager.Add_User(input)
    #关闭用户管理Tag
    Tag(driver).closeTagGtos('用户管理')
