# !/usr/bin/env python
# -*-coding: utf-8-*-

# @ProjectName : security_connection_platform(SCP)
# @FileName : test_pytest_log.py
# @Time : 2020/3/13 9:07
# @Author : Nick

import logging
import pytest


@pytest.fixture()
def log():
    logging.info("No logger object difinition")
    yield
    logging.log(logging.DEBUG, "finishi is all right")


def testlog(log):
    assert 1 == 1


