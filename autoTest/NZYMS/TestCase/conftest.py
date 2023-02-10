import os
import sys
from Base.basepage import BasePage
from selenium import webdriver
import pytest


sys.path.append(os.path.join(os.getcwd(), "../"))
sys.path.append(os.path.join(os.getcwd(), "../../../"))
from NZYMS.Config import config
from NZYMS.PageObject.login import Login


@pytest.fixture(scope="session")
def driver():
    driver=webdriver.Chrome()
    login = Login(driver)
    login.geturl(config.host)
    login.login(config.username, config.password, config.showname)
    BasePage(driver).refresh()
    return driver


