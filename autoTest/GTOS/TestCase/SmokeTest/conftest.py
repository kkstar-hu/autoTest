import os
import sys

from selenium import webdriver

sys.path.append(os.path.join(os.getcwd(), "../"))
import pytest

from GTOS.Config import config
from GTOS.PageObject.login import Login


@pytest.fixture(scope="session")
def driver():
    driver=webdriver.Chrome()
    login = Login(driver)
    login.geturl(config.host)
    login.login(config.username, config.password, config.showname)
    return driver


