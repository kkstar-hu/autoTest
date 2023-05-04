# -*- coding:utf-8 -*-
import os
import allure
from selenium import webdriver
import pytest
from BTOSLJ.PageObject.login import Login

server_host = None
db_host = None

@pytest.fixture(scope="session")
def server_host():
    global server_host
    server_host = "10.166.0.131:20000"
    yield server_host
    return server_host


@pytest.fixture(scope="session")
def db_host():
    global db_host
    db_host = "10.166.0.137"
    yield db_host
    return db_host

