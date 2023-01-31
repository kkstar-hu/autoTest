from selenium import webdriver

import pytest

from GTOSXM.Config import config
from GTOSXM.PageObject.login import Login


@pytest.fixture(scope="session")
def driver():
    driver=webdriver.Chrome()
    login = Login(driver)
    login.geturl(config.host)
    login.login(config.username, config.password, config.showname,'海润')
    return driver


