#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
--------------------------------------------------------
# @Contact      :   277383645@qq.com
# @License      :   GPL 
# @Project      :   Security_interface_platform.py    
# @File         :   test_sell_function.py    
--------------------------------------------------------
@Modify Time      @Author    @Version    
------------      -------    --------  
2021/3/16 14:21   Nick wong      1.0  
------------------------------------------------------------------------------------
# @Description  :
1.测试双色球、3D、七乐彩和K8的销售、查询和兑奖
2.测试函数只负责测试结果的验证，数据准备和请求处理过程全部在fixture中完成，达到封装和聚焦重点的目的
3.用allure生成测试报告，使用它的动态层次结构生成函数和测试数据的结合的办法产生测试报告需要的数据
-------------------------------------------------------------------------------------
"""

import pytest
import allure


@pytest.mark.run(order=1)
@pytest.mark.smoke
def test_sell_api(per_sell_case):
    """
    1.销售接口测试用例：完成测试结果验证和测试报告生成
    2.常规玩法使用数据库中的caseid动态添加allure标签，
    3.根据玩法名（playEname）allure.dynamic.feature("销售接口_" + per_record['playEname'])、
      投注方式（allure.dynamic.story(per_record['playEname'] + '_' + per_record['playType'] + '_case')）动态
      生成报告中的层级结构
    4.per_record的数据是从数据库查询出来的原始数据，长周期玩法和K8的数据不同要分开处理
    :param per_sell_case: 处理销售接口测试数据和请求过程的fixture
    :return:
    """
    per_record, recv, sell_term_code = per_sell_case
    # 长周期的报告生成
    if "playEname" in per_record:
        allure.dynamic.feature("销售接口_" + per_record['playEname'])
        allure.dynamic.story(per_record['playEname'] + '_' + per_record['playType'] + '_case')
        allure.dynamic.severity(allure.severity_level.CRITICAL)
        allure.dynamic.description("用例信息：" + "期号：" + sell_term_code + "金额：" +
                                   str(per_record['money']) + "    测试点：" + per_record['description'])
    # K8的报告生成
    if 'play_ename' in per_record:
        allure.dynamic.feature("销售接口_" + per_record['play_ename'])
        allure.dynamic.story(per_record['play_ename'] + '_' + per_record['bet_code'] + '_case')
        allure.dynamic.severity(allure.severity_level.CRITICAL)
        allure.dynamic.description("用例信息：" + "期号：" + sell_term_code + "金额：" +
                                   str(per_record['bet_money']) + "    测试点：" + per_record['comment'])

    assert '100000' == recv['BackCode']


@pytest.mark.run(order=2)
@pytest.mark.smoke
def test_query_api(per_query_test):
    """
    # 下面的函数测试了，可以将数据库的备注动态的输入到allure的报告中，可以使用数据库中的caseid
    测试了动态添加allure标签，不用再去处理
    :param per_query_test:
    :return:
    """
    sell_term_code, ticket_code, playEname, runcode, recv = per_query_test
    print(sell_term_code, ticket_code, playEname)

    allure.dynamic.feature("查询接口_" + playEname)
    allure.dynamic.story(playEname + '_' + sell_term_code + '_case')
    allure.dynamic.severity(allure.severity_level.CRITICAL)
    allure.dynamic.description("查询用例详情：{}, 期号：{}, 流水号：{},票号：{}".format(playEname, sell_term_code, runcode, ticket_code))
    assert '100000' == recv['BackCode']


# @pytest.mark.run(order=3)
# @pytest.mark.smoke
# def test_encash_api(encash_test_case):
#     """
#     # 下面的函数测试了，可以将数据库的备注动态的输入到allure的报告中，可以使用数据库中的caseid
#     测试了动态添加allure标签，不用再去处理
#     :param query_test_case:
#     :return:
#     """
#     playEname, sell_term_code, ticket_code, recv = encash_test_case
#
#     allure.dynamic.feature("兑奖接口_" + playEname)
#     allure.dynamic.story(playEname + '_' + sell_term_code + '_case')
#     allure.dynamic.severity(allure.severity_level.CRITICAL)
#     allure.dynamic.description("兑奖用例详情：玩法{}, 期号：{}, 票号：{} ".format(playEname, sell_term_code, ticket_code))
#     assert '100000' == recv['BackCode']
