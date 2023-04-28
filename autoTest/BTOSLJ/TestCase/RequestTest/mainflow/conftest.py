# -*- coding:utf-8 -*-
import os
import allure
import pytest

host = None

@pytest.fixture(scope="session")
def host():
    global host
    host = "10.166.0.131:20000"
    yield host
    return host


