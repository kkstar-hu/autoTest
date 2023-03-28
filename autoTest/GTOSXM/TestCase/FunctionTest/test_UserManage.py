import os.path

import allure
import pytest

from Commons.Controls.tag import Tag
from Commons.yamlread import read_yaml
from GTOSXM.PageObject.User_Manage.user_add import User_Manage
from GTOSXM.PageObject.gtos_menu import GtosMenu


@allure.story('1.系统管理')
@allure.title('用户管理')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'user_manage','user_data.yaml')))
def testUserAdd(driver, input):
    """添加用户"""
    print("******************************************Test Add User***********************************************")
    menu = GtosMenu(driver)  #菜单跳转
    menu.select_level_Menu("系统管理,用户管理")
    userManager = User_Manage(driver)
    userManager.Add_User(input)  #新增用户
    Tag(driver).closeTagGtos('用户管理')  #关闭用户管理Tag

@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'user_manage','user_data.yaml')))
def testNewUserinformation(driver, input):
    menu = GtosMenu(driver)
    menu.select_level_Menu("系统管理,用户管理")
    userManager = User_Manage(driver)
    userManager.New_User_Select(input)  #查询用户
    Tag(driver).closeTagGtos('用户管理')  #关闭用户管理Tag


