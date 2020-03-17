# !/usr/bin/env python
# -*-coding: utf-8-*-
# @ProjectName : security_connection_platform(SCP)
# @FileName : test_bet_query.py
# @Time : 2020/3/11 15:43
# @Author : Nick

"""
在conftest.conf文件中的完成数据收集，使用hook函数pytest_generate_tests实现bet_query的参数化
注意：运行前检查，数据文件encash_and_query.txt是否存在
"""

import allure
from scp_python_adaptor.basicdata_set import basic_data
from scp_python_adaptor.testdata_handle_kit import excutive_test


@allure.feature("自助终端投注查询接口")
class TestBetQuery:

    @allure.story("不分玩法和投注方式的查询测试用例")
    @allure.severity(allure.severity_level.NORMAL)
    @allure.title('bet_query_case')
    def test_bet_query(self, bet_query):
        recv_query = excutive_test(basic_data.bet_query_url, 'bet_query', bet_query[0])
        assert '100000' == recv_query["BackCode"]
