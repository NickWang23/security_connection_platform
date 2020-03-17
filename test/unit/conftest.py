# !/usr/bin/env python
# -*-coding: utf-8-*-

# @ProjectName : security_connection_platform(SCP)
# @FileName : conftest.py.py
# @Time : 2020/3/16 14:20
# @Author : Nick


def pytest_make_parametrize_id(config, val, argname):
    print('argname:', argname, 'val', val)
    return repr(val)
