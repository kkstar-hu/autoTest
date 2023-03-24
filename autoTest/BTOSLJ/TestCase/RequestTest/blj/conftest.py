# -*- coding:utf-8 -*-
import os
import allure
from selenium import webdriver
import pytest
from BTOSLJ.PageObject.login import Login

host = None

@pytest.fixture(scope="session")
def host():
    global host
    host = "10.116.8.16:8520"
    yield host
    return host