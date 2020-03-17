# !/usr/bin/env python
# -*-coding: utf-8-*-

# @ProjectName : jiling_aqjr
# @FileName : test_sell_interface_v01.py
# @Time : 2020/1/9 9:36
# @Author : Nick
"""
2020-03-11
测试数据准备的一个问题：
在测试数据中必须全部包含现在的各个玩法的每种数据，如果少了一种程序会报错，例如3D现在定义有：danshi、fushi、dantuo、yichang4种类型
那在3D数据构造的时候就要全部包括这4中类型，不然会报错。这个是结构性问题，暂时不改了
"""


import pytest
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


@allure.feature("销售接口-3D玩法")
class Test3DSell:
    @allure.story("单式测试用例")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title('3D_danshi_case')
    def test_3d_danshi(self, d3_danshi):
        """
        用fixture来完成测试数据准备，测试3D单式
        执行胆拖投注的测试，因为在自定义的fixture:danshi_data里面使用了request内建fixture，
        """
        # 可以用danshi_data['ReqContent']来查看每个元素的ReqContent内容
        sell_result = excutive_test(basic_data.sell_profix_url, "sell", d3_danshi[0])
        # print("1:", d3_danshi[0]['ReqContent']['SellTermCode'])
        assert '100000' == sell_result["BackCode"]

    @allure.story("复式测试用例")
    @allure.title('3D_fushi_case')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_fushi_sell(self, d3_fushi):
        """
        用参数化方式来测试,3D复式投注
        """
        sell_result = excutive_test(basic_data.sell_profix_url, "sell", d3_fushi[0])
        assert '100000' == sell_result["BackCode"]

    @pytest.mark.core_case
    @allure.story("胆拖测试用例")
    @allure.title('3D_dantuo_case')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_dantuo_sell(self, d3_dantuo):
        """
        测试3D胆拖
        """
        sell_result = excutive_test(basic_data.sell_profix_url, "sell", d3_dantuo[0])
        assert '100000' == sell_result["BackCode"]

    @pytest.mark.exception_case
    @allure.story("异常测试用例")
    @allure.title('3D_yichang_case')
    @allure.severity(allure.severity_level.BLOCKER)
    def test_d3_sell_exception(self, d3_yichang):
        """
        3D注码异常测试，采用于双色球不同的方式，判断输出内容是否相同，不判断返回码
        """
        sell_result = excutive_test(basic_data.sell_profix_url, "sell", d3_yichang[0])
        assert '100000' != sell_result["BackCode"]


@allure.feature("销售接口-双色球")
class TestB001Sell:
    @allure.story("单式测试用例")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title('B001_danshi_case')
    def test_b001_dashi(self, b001_danshi):
        """
        用fixture来完成测试数据准备，测试B001单式
        执行胆拖投注的测试，因为在自定义的fixture:danshi_data里面使用了request内建fixture，
        """
        # 可以用danshi_data['ReqContent']来查看每个元素的ReqContent内容
        sell_result = excutive_test(basic_data.sell_profix_url, "sell", b001_danshi[0])
        assert '100000' == sell_result["BackCode"]

    @allure.story("复式测试用例")
    @allure.title('B001_fushi_case')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_fushi_sell(self, b001_fushi):
        """
        用参数化方式来测试,B001复式投注
        """
        sell_result = excutive_test(basic_data.sell_profix_url, "sell", b001_fushi[0])
        assert '100000' == sell_result["BackCode"]

    @pytest.mark.core_case
    @allure.story("胆拖测试用例")
    @allure.title('B001_dantuo_case')
    @allure.severity(allure.severity_level.CRITICAL)
    def test_dantuo_sell(self, b001_dantuo):
        """
        测试3D胆拖
        """
        sell_result = excutive_test(basic_data.sell_profix_url, "sell", b001_dantuo[0])
        assert '100000' == sell_result["BackCode"]

    @pytest.mark.exception_case
    @allure.story("异常测试用例")
    @allure.title('B001_yichang_case')
    @allure.severity(allure.severity_level.BLOCKER)
    def test_b001_sell_exception(self, b001_yichang):
        """
        B001注码异常测试，采用于双色球不同的方式，判断输出内容是否相同，不判断返回码
        """
        sell_result = excutive_test(basic_data.sell_profix_url, "sell", b001_yichang[0])
        assert '100000' != sell_result["BackCode"]
