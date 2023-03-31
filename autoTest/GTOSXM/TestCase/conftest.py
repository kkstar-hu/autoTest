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
    driver=webdriver.Chrome()
    login = Login(driver)
    login.geturl(config.host)
    login.login(config.username, config.password, config.showname,"海润")
    yield driver
    driver.quit()
    return driver

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    '''
    hook pytest失败
    :param item:
    :param call:
    :return:
    '''
    # execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()
    # we only look at actual failing test calls, not setup/teardown
    if rep.when == "call" and rep.failed:
        mode = "a" if os.path.exists("../failures") else "w"
        with open("../failures", mode) as f:
                # let's also access a fixture for the fun of it
            if "tmpdir" in item.fixturenames:
                    extra = " (%s)" % item.funcargs["tmpdir"]
            else:
                    extra = ""
            f.write(rep.nodeid + extra + "\n")
            with allure.step('添加失败截图...'):
                allure.attach(driver.get_screenshot_as_png(), "失败截图", allure.attachment_type.PNG)

