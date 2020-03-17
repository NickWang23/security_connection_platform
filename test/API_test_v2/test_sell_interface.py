# !/usr/bin/env python
# -*-coding: utf-8-*-

# @ProjectName : security_connection_platform(SCP)
# @FileName : test_sell_interface.py
# @Time : 2020/3/17 9:09
# @Author : Nick


import pytest
import allure
from scp_python_adaptor.testdata_handle_kit import excutive_test
from scp_python_adaptor import testdata_handle_kit
from scp_python_adaptor.basicdata_set import basic_data
from scp_python_adaptor.testdata_handle_kit import sell_data


class SellDataset:
    """完成和销售接口相关的所有测试前准备工作：
    新思路：在每次读取一个玩法的数据时才更新sessionid，这样的话可以把初始化的工作放到每次测试进行之前，避免测试刚开始时做太多可能
    后续用不到的数据读取

    """
    def __init__(self, term_code, file, d3=False, dball=False):
        self.sell_profix = 'http://10.10.22.236:8941/secret/common/lottBet?partnerId=00101&hashType=md5&hash='
        self.sell_content = {"RunCode": "",
                             "UserId": basic_data.userid,
                             "AccessType": 2,
                             "PlayEname": "",
                             "SellTermCode": "",
                             "LoginSession": "",
                             "Money": "",
                             "DrawWay": 1,
                             "TicketCode": "",
                             "CheckCode": ""}
        self.session = testdata_handle_kit.sessionid()
        if d3:
            self.d3data = sell_data(file, term_code, session = self.session)
        if dball:
            self.dball = sell_data(file, term_code, session = self.session)


def get_ids(item):
    return item[1]


d3_src_file = r'D:\python_develop\jiling_aqjr\datadir\D3注码.txt'
d3_term_num = "2020017"
d3data = SellDataset(d3_term_num, d3_src_file, d3=True).d3data


@allure.feature("销售接口-3D玩法")
class Test3DSell:
    """
    3d玩法的测试用例，使用了parametrize来进行参数化，没有使用fixture，目的是为了减少玩法数据在conftest使用fixture初始化时，有一个
    出现问题导致，其他都失败
    """
    @allure.story("单式测试用例")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.title('3D_danshi_case')
    @pytest.mark.parametrize("danshi", d3data["danshi"], ids = get_ids)
    def test_3d_danshi(self, danshi):
        """
        用parametrize来完成参数化
        """
        # 可以用danshi_data['ReqContent']来查看每个元素的ReqContent内容
        sell_result = excutive_test(basic_data.sell_profix_url, "sell", danshi[0])
        # print("1:", d3_danshi[0]['ReqContent']['SellTermCode'])
        assert '100000' == sell_result["BackCode"]

    @allure.story("复式测试用例")
    @allure.title('3D_fushi_case')
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.parametrize("d3_fushi", d3data["fushi"], ids = get_ids)
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
    @pytest.mark.parametrize("d3_dantuo", d3data["dantuo"], ids = get_ids)
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
    @pytest.mark.parametrize("d3_yichang", d3data["yichang"], ids = get_ids)
    def test_d3_sell_exception(self, d3_yichang):
        """
        3D注码异常测试，采用于双色球不同的方式，判断输出内容是否相同，不判断返回码
        """
        sell_result = excutive_test(basic_data.sell_profix_url, "sell", d3_yichang[0])
        assert '100000' != sell_result["BackCode"]
