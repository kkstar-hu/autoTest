import os
import sys

import allure
from selenium import webdriver
import pytest
from GTOSXM.Config import config
from GTOSXM.PageObject.login import Login

sys.path.append(os.path.join(os.getcwd(), "../"))
sys.path.append(os.path.join(os.getcwd(), "../../../"))

driver = None


@pytest.fixture(scope="session")
def driver():
    global driver
    driver = webdriver.Chrome()
    login = Login(driver)
    login.geturl(config.host)
    login.login(config.username, config.password, f"用户{config.username}登录成功", "海润", config.showname)
    yield driver
    driver.quit()
    return driver


# @pytest.hookimpl(tryfirst=True, hookwrapper=True)
# def pytest_runtest_makereport(item, call):
#     '''
#     hook pytest失败
#     :param item:
#     :param call:
#     :return:
#     '''
#     # execute all other hooks to obtain the report object
#     outcome = yield
#     rep = outcome.get_result()
#     # we only look at actual failing test calls, not setup/teardown
#     if rep.when == "call" and rep.failed:
#         mode = "a" if os.path.exists("../failures") else "w"
#         with open("../failures", mode) as f:
#                 # let's also access a fixture for the fun of it
#             if "tmpdir" in item.fixturenames:
#                     extra = " (%s)" % item.funcargs["tmpdir"]
#             else:
#                     extra = ""
#             f.write(rep.nodeid + extra + "\n")
#             with allure.step('添加失败截图...'):
#                 allure.attach(driver.get_screenshot_as_png(), "失败截图", allure.attachment_type.PNG)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call, ):
    """
    获取每个用例的钩子函数
    :param item:
    :param call:
    :return:
    """
    outcome = yield
    rep = outcome.get_result()
    # 以下为实现异常截图的代码：
    # rep.when可选参数有call、setup、teardown，
    # call表示为用例执行环节、setup、teardown为环境初始化和清理环节
    # 这里只针对用例执行且失败的用例进行异常截图
    if rep.when == "call" and rep.failed:
        mode = "a" if os.path.exists("failures") else "w"
        with open("failures", mode) as f:
            if "tmpdir" in item.fixturenames:
                extra = " (%s) " % item.funcargs["tmpdir"]
            else:
                extra = ""
            f.write(rep.nodeid + extra + "\n")
        item.name = item.name.encode("utf-8").decode("unicode-escape")

        # file_name = '{}.png'.format(str(round(time.time() * 1000)))
        # path = os.path.join(PRPORE_SCREEN_DIR, file_name)
        #
        # driver.save_screenshot(path)

        if hasattr(driver, "get_screenshot_as_png"):
            with allure.step("添加失败截图"):
                # get_screenshot_as_png实现截图并生成二进制数据
                # allure.attach直接将截图二进制数据附加到allure报告中
                allure.attach(driver.get_screenshot_as_png(), "失败截图", allure.attachment_type.PNG)
