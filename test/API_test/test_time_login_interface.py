# !/usr/bin/env python
# -*-coding: utf-8-*-

# @ProjectName : security_connection_platform(SCP)
# @FileName : test_time_login_interface.py
# @Time : 2020/3/11 15:52
# @Author : Nick

from scp_python_adaptor.scp_handle_process import ContentSet
import allure

"""
这个文件里的测试用例只是检查了正常输入后的结果，没有模拟登录参数的异常和多代销商登录的情况
注意：登录接口测试，最好不要和其他的测试一起开展，可能会引起session异常报错
"""


@allure.feature("测试时间同步接口")
@allure.severity(allure.severity_level.NORMAL)
@allure.title('time_sync_case')
def test_time_sync():
    assert 14 == len(ContentSet.time_stamp_gen())


@allure.feature("测试登录接口")
@allure.severity(allure.severity_level.NORMAL)
@allure.title('login_case')
def test_login():
    # print(len(ContentSet.login()))
    assert 32 == len(ContentSet.login())





