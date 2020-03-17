# !/usr/bin/env python
# -*-coding: utf-8-*-

# @ProjectName : jiling_aqjr
# @FileName : conftest.py.py
# @Time : 2019/12/31 17:24
# @Author : Nick
"""
2020-03-11
测试数据准备的一个问题：
在测试数据中必须全部包含现在的各个玩法的每种数据，如果少了一种程序会报错，例如3D现在定义有：danshi、fushi、dantuo、yichang4种类型
那在3D数据构造的时候就要全部包括这4中类型，不然会报错。这个是结构性问题，暂时不改了
注意事项：
    所有的原始数据文件都放在datadir目录下，目录是固定的
    查询和兑奖使用同一个文件：encash_and_query.txt；此文件在投注销售时会自动生成
"""

from scp_python_adaptor.testdata_handle_kit import *


d3_src_file = r'D:\python_develop\jiling_aqjr\datadir\D3注码.txt'
d3_term_num = "202017"
dball_src_file = r'D:\python_develop\jiling_aqjr\datadir\B001_test.txt'
dball_term_num = "2020012"
betquery_encash_file = 'D:\python_develop\jiling_aqjr\datadir\encash_and_query.txt'


def login_sessionid():
    return get_session()


unique_login_id = login_sessionid()
d3_data_set = sell_data(d3_src_file, d3_term_num, unique_login_id)
dball_data_set = sell_data(dball_src_file, dball_term_num, unique_login_id)
betquery_set = betquery_encash_data(betquery_encash_file, 'bet_query', unique_login_id)
encash_set = betquery_encash_data(betquery_encash_file, 'encash', unique_login_id)


def get_ids(item):
    return item[1]


def pytest_generate_tests(metafunc):
    """
    使用这个hook函数来完成fixture的参数化，一次完成多个fixture的参数化，在用例中使用时，只需输入fixture名字，如d3_danshi
    """
    if "d3_danshi" in metafunc.fixturenames:
        metafunc.parametrize("d3_danshi", d3_data_set['danshi'], ids = get_ids)
    if "d3_fushi" in metafunc.fixturenames:
        metafunc.parametrize("d3_fushi", d3_data_set['fushi'], ids = get_ids)
    if "d3_dantuo" in metafunc.fixturenames:
        metafunc.parametrize("d3_dantuo", d3_data_set['dantuo'], ids = get_ids)
    if "d3_yichang" in metafunc.fixturenames:
        metafunc.parametrize("d3_yichang", d3_data_set['yichang'], ids = get_ids)
    if "b001_danshi" in metafunc.fixturenames:
        metafunc.parametrize("b001_danshi", dball_data_set['danshi'], ids = get_ids)
    if "b001_fushi" in metafunc.fixturenames:
        metafunc.parametrize("b001_fushi", dball_data_set['fushi'], ids = get_ids)
    if "b001_dantuo" in metafunc.fixturenames:
        metafunc.parametrize("b001_dantuo", dball_data_set['dantuo'], ids = get_ids)
    if "b001_yichang" in metafunc.fixturenames:
        metafunc.parametrize("b001_yichang", dball_data_set['yichang'], ids = get_ids)
    if "bet_query" in metafunc.fixturenames:
        metafunc.parametrize("bet_query", betquery_set, ids = get_ids)
    if "encash" in metafunc.fixturenames:
        metafunc.parametrize("encash", encash_set, ids = get_ids)
