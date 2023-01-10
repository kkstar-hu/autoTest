from selenium import webdriver

import pytest
from NZYMS.Config import config
from NZYMS.PageObject.login import Login

@pytest.fixture(scope="session")
def driver():
    driver=webdriver.Chrome()
    login = Login(driver)
    login.geturl(config.host)
    login.login(config.username, config.password, config.showname)
    return driver


