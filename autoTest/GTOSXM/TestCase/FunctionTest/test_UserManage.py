import os.path
import allure
import pytest

from Base.basepage import BasePage
from Commons.Controls.tag import Tag
from Commons.yamlread import read_yaml
from GTOSXM.Config import config
from GTOSXM.PageObject.User_Manage.user_manage import User_Manage
from GTOSXM.PageObject.gtos_menu import GtosMenu
from GTOSXM.PageObject.login import Login

@allure.story('1.系统管理')
@allure.title('用户管理')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), 'user_manage', 'user_data.yaml')))
def testUserAdd(driver, input):
    """添加用户"""
    print("******************************************Test Add User***********************************************")
    # 菜单跳转
    menu = GtosMenu(driver)
    menu.select_level_Menu("系统管理,用户管理")
    userManager = User_Manage(driver)
    # 新增用户
    userManager.Add_User(input)
    # userManager.User_Search(input)  # 查询用户

@allure.story('1.系统管理')
@allure.title('用户管理')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), 'user_manage', 'user_search_data.yaml')))
def testUserSearch(driver, input):
    """查询用户"""
    # 菜单跳转
    # menu = GtosMenu(driver)
    # menu.select_level_Menu("系统管理,用户管理")
    userManager = User_Manage(driver)
    # 查询用户
    userManager.User_Search(input)
    userManager.User_Check(input)  # 校验用户信息
    userManager.Check_Role(input)  # 校验用户角色

@allure.story('1.系统管理')
@allure.title('用户管理')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), 'user_manage', 'user_update_data.yaml')))
def testUserUpdate(driver, input):
    """更新用户"""
    # 菜单跳转
    # menu = GtosMenu(driver)
    # menu.select_level_Menu("系统管理,用户管理")
    userManager = User_Manage(driver)
    # 更新用户
    userManager.Update_User(input)
    userManager.User_Check(input)  # 校验用户信息
    userManager.Check_Role(input)  # 检查角色信息
    Tag(driver).closeTagGtos('用户管理')  # 关闭用户管理Tag
    userManager.Logout_User()

@allure.story('1.系统管理')
@allure.title('用户管理')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), 'user_manage', 'user_forbidden_data.yaml')))
def testUserForbidden(driver, input):
    """禁用用户"""
    # 登录(单个测试时注释本段)
    # driver.refresh()
    login = Login(driver)
    login.login(config.username, config.password, "用户admin登录成功", "海润", config.showname)
    # 菜单跳转
    menu = GtosMenu(driver)
    menu.select_level_Menu("系统管理,用户管理")
    userManager = User_Manage(driver)
    userManager.User_Search(input)  # 定位到要禁用的用户
    # 禁用用户
    userManager.Forbidden_User(input)
    userManager.User_Check(input)  # 校验禁用后的用户信息
    userManager.Logout_User()  # 退出当前用户
    # 以被禁用的用户身份登录
    forbidden_driver = Login(driver)
    forbidden_driver.login(input["用户账号"], input["密码"], "账户已被禁用。账户:testAddUser6", input["码头中文名称"], config.showname)

@allure.story('1.系统管理')
@allure.title('用户管理')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), 'user_manage', 'user_resume_data.yaml')))
def testUserResume(driver, input):
    """恢复用户"""
    # 以未被禁用的用户身份登录(单个测试时注释本段）
    page = BasePage(driver)
    page.refresh()
    login = Login(driver)
    login.login(config.username, config.password, "用户admin登录成功", "海润", config.showname)
    # 菜单跳转
    menu = GtosMenu(driver)
    menu.select_level_Menu("系统管理,用户管理")
    userManager = User_Manage(driver)
    userManager.User_Search(input)  # 定位到要恢复的用户
    # 恢复用户
    userManager.Resume_User(input)
    userManager.User_Check(input)  # 校验恢复后的用户信息
    userManager.Logout_User()  # 退出当前用户
    # 验证恢复后登录成功
    resume_driver = Login(driver)
    resume_driver.login(input["用户账号"], input["密码"], "用户testAddUser6登录成功", input["码头中文名称"], config.showname)
    userManager.Logout_User()

@allure.story('1.系统管理')
@allure.title('用户管理')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), 'user_manage', 'user_reset_password_data.yaml')))
def testResetPassword(driver, input):
    """重置密码"""
    # 登录(单个测试时注释本段)
    page = BasePage(driver)
    page.refresh()
    login = Login(driver)
    login.login(config.username, config.password, "用户admin登录成功", "海润", config.showname)
    # 菜单跳转
    menu = GtosMenu(driver)
    menu.select_level_Menu("系统管理,用户管理")
    userManager = User_Manage(driver)
    userManager.User_Search(input)  # 定位到要重置密码的用户
    # 重置密码
    userManager.Reset_Password(input)
    userManager.Logout_User()  # 退出当前用户
    # 验证旧的密码不能登录
    old_password_driver = Login(driver)  # 以旧的密码登录
    old_password_driver.login(input["用户账号"], input["密码"], "认证中心调用失败。错误信息:用户名或密码错误, 9次后账号将被锁", input["码头中文名称"], input["归属码头"])
    # 验证重置后的密码可以登录
    driver.refresh()
    new_password_driver = Login(driver)
    new_password_driver.login(input["用户账号"], input["重置密码"], "密码已过期", input["码头中文名称"], input["归属码头"])
    userManager.Logout_User()

@allure.story('1.系统管理')
@allure.title('用户管理')
@pytest.mark.parametrize("input", read_yaml(os.path.join(os.getcwd(), 'user_manage', 'user_deblocking_data.yaml')))
def testUserDeblocking(driver, input):
    """解锁用户"""
    # 登录(单个测试时注释本段)
    page = BasePage(driver)
    page.refresh()
    login = Login(driver)
    login.login(config.username, config.password, "用户admin登录成功", "海润", config.showname)
    # 循环输入错误密码使用户被锁
    userManager = User_Manage(driver)
    userManager.Logout_User()
    userManager.Loop_Util_Lock_User(input)
    # 以未被锁用户的身份进入进行解锁
    userManager.Use_Unlock_User_Login()
    userManager = User_Manage(driver)
    userManager.User_Search(input)  # 定位到要解锁的用户
    userManager.Deblocking_User(input)  # 解锁用户
    userManager.Logout_User()
    userManager.Check_User_Delocking(input)  # 验证解锁后能成功登录


