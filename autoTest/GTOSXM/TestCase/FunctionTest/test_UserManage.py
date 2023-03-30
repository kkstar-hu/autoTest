import os.path

import allure
import pytest
from Commons.Controls.tag import Tag
from Commons.yamlread import read_yaml
from GTOSXM.PageObject.User_Manage.user_manage import User_Manage
from GTOSXM.PageObject.gtos_menu import GtosMenu
from GTOSXM.PageObject.login import Login


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
    userManager.testUserSearch(input)  # 查询用户
    Tag(driver).closeTagGtos('用户管理')  #关闭用户管理Tag

@allure.story('1.系统管理')
@allure.title('用户管理')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'user_manage','user_data.yaml')))
def testUserSearch(driver, input):
    """查询用户"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("系统管理,用户管理")
    userManager = User_Manage(driver)
    userManager.User_Search(input)  #查询用户
    userManager.User_Check(input)  #校验用户信息
    userManager.Check_Role(input)  #校验用户角色
    Tag(driver).closeTagGtos('用户管理')  #关闭用户管理Tag

@allure.story('1.系统管理')
@allure.title('用户管理')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'user_manage','user_update_data.yaml')))
def testUserUpdate(driver, input):
    """更新用户"""
    menu = GtosMenu(driver)
    menu.select_level_Menu("系统管理,用户管理")
    userManager = User_Manage(driver)
    userManager.Update_User(input)  #更新用户
    userManager.User_Check(input)  #校验用户信息
    userManager.Check_Role(input)  #检查角色信息
    Tag(driver).closeTagGtos('用户管理')  # 关闭用户管理Tag

@allure.story('1.系统管理')
@allure.title('用户管理')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(),'user_manage','user_forbidden_data.yaml')))
def testUserForbidden(driver, input):
    """禁用用户"""
    # menu = GtosMenu(driver)
    # menu.select_level_Menu("系统管理,用户管理")
    userManager = User_Manage(driver)
    # userManager.User_Search(input)  #定位到要禁用的用户
    # userManager.Forbidden_User(input)
    # userManager.User_Check(input)  #校验禁用后的用户信息
    userManager.Logout_User()  #退出当前用户
    # forbidden_driver = Login(driver)  #以被禁用的用户身份登录
    # forbidden_driver.login(input["用户账号"], input["密码"], input["归属码头"], input["码头中文名称"])
    userManager.Login_As_Forbidden_User(input)  #以被禁用的用户身份登录