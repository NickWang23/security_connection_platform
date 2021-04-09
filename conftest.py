"""
--------------------------------------------------------
# @Contact      :   277383645@qq.com
# @License      :   GPL
# @Project      :   Security_interface_platform.py
# @File         :   conftest.py
--------------------------------------------------------
@Modify Time      @Author    @Version
------------      -------    --------
2021/4/9 8:31   Nick wong      1.0
--------------------------------------------------------
# @Description  :    实现测试框架中使用到的fixture和hook函数
--------------------------------------------------------
"""

import init_config
import datetime
from setting_initial_env import Toolkit
from init_config import basic_data
import pytest


def pytest_sessionstart():
    """
    测试session开始运行时，记录开始时间
    :return:
    """
    global start
    start = datetime.datetime.now()
    print("*"*35, "testing session start", "*"*36)


def pytest_sessionfinish():
    """
    测试session运行结束时，计算运行完所有测试消耗的时间
    :return:
    """
    end = datetime.datetime.now()
    # 从测试开始运行到结束的时间跨度
    print("*"*30, "session duration:", str(end - start), "*"*30)


def case_id(item):
    """
    每个销售测试用例的id构造函数
    :param item: 从数据库中得到的每条原始销售数据
    :return: 构造完成的销售测试用例id
    """
    if 'play_ename' in item:
        return item['play_ename'] + '_' + item['bet_code'] + '_' + item['comment']
    return item['id']


def bet_query_case_id(item):
    """
    每个查询测试用例的id构造函数
    :param item:
    :return:
    """
    return item['PlayEname'] + '_' + item['SellTermCode'] + '_' + item['Runcode']


# 单例模式：运行一次测试只有一个session_id,而不是每个测试用例都去进行登录获取session_id,因此调用同一个对象获取相同的sessionId
session = Toolkit.session_id()

# 把销售、查询和兑奖接口中的公共部分抽取出来，定义成一个字典，避免代码重复
general_out_content = {"PartnerId": basic_data.partner_id,
                       "TimeStamp": Toolkit.time_stamp_gen(),
                       "SerialNum": basic_data.serial_num_gen(),
                       "Version": basic_data.version,
                       "Token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                       "ReqContent": ""}


@pytest.fixture()
def per_sell_case(request):
    """
    每条销售测试用例的数据处理fixture：完成数据的组装、请求的发送和响应数据的返回
    :param request: 代表每条销售测试用例
    :return:
    """

    # 销售测试用例请求数据的组装：因常规玩法和特殊玩法测试数据来源于不同的表，所以需要分别处理
    sell_content = {"RunCode": basic_data.serial_num_gen(),
                    "UserId": basic_data.user_id,
                    "AccessType": 2,
                    "PlayEname": "",
                    "SellTermCode": "",
                    "LoginSession": session['RespContent']['LoginSession'],
                    "Money": "",
                    "DrawWay": 1,
                    "TicketCode": "",
                    "CheckCode": ""}
    # 长周期数据和快乐8数据来自不同的表：快乐8玩法的玩法名、金额和投注号码
    if 'play_ename' in request.param:
        sell_content.update(PlayEname=request.param['play_ename'])
        sell_content.update(Money=str(request.param['bet_money']))
        sell_content.update(TicketCode=request.param['bet_code'])
        if sell_content['PlayEname'] == 'ZCKL8':
            sell_content.update(SellTermCode=basic_data.k8_term_code)
    # 长周期数据和快乐8数据来自不同的表：长周期玩法销售用例的玩法名、金额和投注号码
    if 'playEname' in request.param:
        sell_content.update(PlayEname=request.param['playEname'])
        sell_content.update(Money=request.param['money'])
        sell_content.update(TicketCode=request.param['code'])
        if sell_content['PlayEname'] == 'B001':
            sell_content.update(SellTermCode=basic_data.ball_term_code)
        if sell_content['PlayEname'] == 'S3':
            sell_content.update(SellTermCode=basic_data.d3_term_code)
        if sell_content['PlayEname'] == 'QL730':
            sell_content.update(SellTermCode=basic_data.QL730_term_code)

    # 计算验证码并更新请求数据中的对应值
    check_code = Toolkit.check_code(sell_content['RunCode'] + general_out_content['PartnerId'] + sell_content['UserId']
                                    + sell_content['TicketCode'] + str(sell_content['Money']) +
                                    sell_content['LoginSession'])
    sell_content.update(Checkcode=check_code)
    general_out_content.update(ReqContent=sell_content)

    # 发送销售请求并接收返回值
    recv = Toolkit.send_and_recv(basic_data.sell_profix_url + basic_data.partner_id + '&hashType=md5&hash=',
                                 'sell', general_out_content)
    # 返回数据库中得到的原始销售记录、服务器返回值和销售期号给销售测试函数
    return request.param, recv, sell_content['SellTermCode']


@pytest.fixture()
def per_query_test(request):
    """
    查询接口的每条测试用例数据准备fixture，作用和销售接口的fixture相同
    :param request:
    :return:
    """
    bet_query_content = {
        "RunCode": ""
    }
    sell_term_code = request.param['SellTermCode']
    ticket_code = request.param['TicketCode']
    play_ename = request.param['PlayEname']
    runcode = request.param['Runcode']
    
    bet_query_content.update(RunCode=runcode)
    general_out_content.update(ReqContent=bet_query_content)
    
    recv = Toolkit.send_and_recv(basic_data.bet_query_url + basic_data.partner_id + '&hashType=md5&hash=',
                                 'bet_query', general_out_content)
    return sell_term_code, ticket_code, play_ename, runcode, recv


@pytest.fixture()
def encash_test_case(request):
    """
    兑奖接口的每条测试用例数据准备fixture，作用和销售接口的fixture相同
    :param request:
    :return:
    """
    encash_content = {
        "UserId": basic_data.user_id,
        "RunCode": request.param['Runcode'],
        "TicketCode": request.param['TicketCode'],
        "CheckCode": "",
        "LoginSession": session}
    check_code = Toolkit.check_code(encash_content['UserId'] + encash_content["TicketCode"])
    
    encash_content.update(CheckCode=check_code)
    general_out_content.update(ReqContent=encash_content)
    
    sell_term_code = request.param['SellTermCode']
    playEname = request.param['PlayEname']
    ticket_code = request.param['TicketCode']
    recv = Toolkit.send_and_recv(basic_data.encash_profix_url + basic_data.partner_id + '&hashType=md5&hash=',
                                 'encash', general_out_content)
    
    return playEname, sell_term_code, ticket_code, recv


def pytest_addoption(parser):
    """
    通过不同的命令行选项来控制测试用例的数据范围
    :param parser:
    :return:
    """
    parser.addoption("--smoke", action='store_true', help='执行冒烟测试用例')
    parser.addoption("--long_games", action='store_true', help='执行常规玩法的测试用例')
    parser.addoption("--k8", action='store_true', help='执行特殊玩法的测试用例')


def pytest_generate_tests(metafunc):
    """
    解析命令行参数，根据不同的参数实现测试用例数据的灵活参数化
    特别注意： 在metafunc.config.getoption获取并解析命令行参数时，不能紧接着就调用metafunc.parametrize，必须
             在判断fixture是否存在后，再执行参数化操作
    :param metafunc: 测试用例收集阶段的一个pytest对象
    :return:
    """
    # print(metafunc.config.option)
    long_term_sell_data = None
    k8_sell_data = None
    
    if metafunc.config.getoption('long_games'):
        # 查出双色球、3d和七乐彩3个长周期玩法的所有销售用例
        sell_data = "SELECT id, playEname,playType,code,money,description FROM sell_bet_code " \
                    "WHERE (playEname = 'B001' or playEname = 'S3' or playEname = 'QL730')"
    if metafunc.config.getoption('k8'):
        # 查出快乐8的所有销售用例
        sell_data = "SELECT play_ename,bet_code,bet_money,comment FROM sell_bet_code_zckl8 WHERE play_ename = 'ZCKL8'"

    if metafunc.config.getoption('smoke'):
        long_term_sell_data = "SELECT id, playEname,playType,code,money,description FROM sell_bet_code where " \
                              "(playEname='B001' and (funPoint in ('10','20','30','40','50') or playType = 'danshi')) "\
                              "or (playEname = 's3'and (funPoint in ('00','01','02','10','11','12','14','15','1ToMore')))" \
                              "or ((playEname = 'QL730' and ( (funPoint in ('10','20') and money > 5000) or playType = 'danshi')))"
        k8_sell_data = "SELECT play_ename,bet_code,bet_money,comment " \
                       "FROM sell_bet_code_zckl8 WHERE play_ename = 'ZCKL8'"
        sell_data = init_config.get_db_data(long_term_sell_data, count=2) + init_config.get_db_data(k8_sell_data, count=1)

    if 'per_sell_case' in metafunc.fixturenames:
        # indirect为True时，parameterize的第一个参数就是fixture函数，会对第二参数中的每条记录进行处理
        metafunc.parametrize('per_sell_case', sell_data, ids=case_id, indirect=True)

    if 'per_query_test' in metafunc.fixturenames:
        test_case_query = "SELECT SellTermCode, TicketCode,PlayEname,Runcode FROM sell_result"
        query_data = init_config.get_db_data(test_case_query, count='all')
        metafunc.parametrize('per_query_test', query_data, ids=bet_query_case_id, indirect=True)

    if 'encash_test_case' in metafunc.fixturenames:
        test_case_encash = "SELECT SellTermCode, TicketCode,PlayEname,Runcode FROM sell_result"
        encash_data = init_config.get_db_data(test_case_encash)
        metafunc.parametrize('encash_test_case', encash_data, ids=bet_query_case_id, indirect=True)

