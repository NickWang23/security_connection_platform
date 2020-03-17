# !/usr/bin/env python
# -*-coding: utf-8-*-

# @ProjectName : security_connection_platform(SCP)
# @FileName : testdata_handle_kit.py
# @Time : 2020/3/6 16:14
# @Author : Nick


import copy
import allure
from scp_python_adaptor.scp_handle_process import *
from scp_python_adaptor.scp_handle_process import ContentSet
from scp_python_adaptor.basicdata_set import basic_data
from scp_python_adaptor.scp_handle_process import DataHandleToolkit


def get_session():
    return ContentSet.login()


def sessionid():
    server_time_stamp = ContentSet.time_stamp_gen()
    req_content = {
        "PartnerId": basic_data.partner_id,
        "TimeStamp": server_time_stamp,
        "SerialNum": basic_data.serial_num_gen(),
        "Version": basic_data.version,
        "Token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
        "ReqContent": {
            "Userid": "2290110100003",
            "LoginPass": "123456",
            "LoginType": "1",
            "MacAddress": "ABCDEFG123456"
        }
    }
    basic_data.logger.info("登录开始")
    return DataHandleToolkit.excutive_test(basic_data.login_profix_url, 'login', req_content)


@allure.step("prepare source data")
def sell_data(file, term_code, session = None, business_type= 'sell'):
    """
        从文件中读取所有的销售注码，然后把所有数据按按照销售类型分类存储
        在示例文件中的投注类型为投注类型['danshi', 'fushi', 'dantuo', 'yichang']
        注：只能调用此函数来进行数据准备，多次调用会导致loginsession不一致报错
        :param file: 数据源文件
        :param business_type: 两个取值’sell'和 'encash'
        :param term_code:期号
        :param session:登录的loginsession，在一个会话里时必须使用一个session
        :return: 列表:每个元素包含一个由单条销售数据+用于pytest参数化执行时的用例id组成的列表
    """
    # 从数据文件中读取投注数据，注意最后一个字段comment中的注释不要用逗号，防止在解析时被认成分隔符
    sell_record = collections.namedtuple("Sellrecord", "record_id, game_name,case_type, bet_code, money,"
                                                       "case_result, comment")
    content = ContentSet()
    # 兑奖或销售前先做一次登录，获取loginsession
    login_session = session
    content.sell_content.update(LoginSession = login_session)
    # 将原始数据文件中的投注类型放在case_type中，可以实现自动的投注类型归纳整理，不用手动指定投注类型
    # 如果对数据文件中的投注类型不清楚时，可以打印case_type
    case_type = set()
    data_set = {}
    # unicode-escape编码集，他是将unicode内存编码值直接存储
    if file:
        with open(file, 'r', encoding = 'unicode_escape') as f:
            if business_type == 'sell':
                for record in f:
                    # print("split", record.split(','))
                    # 直接使用namedtuple的_make方法将解析后的文件行数据转换成namedtuple实例，并存储在records列表中
                    # 组合生成每条记录
                    record_info = sell_record._make(record.strip().split(','))
                    if record_info.case_type not in case_type:
                        case_type.add(record_info.case_type)
                        data_set[record_info.case_type] = []
                    # print("record_info", record_info)
                    content.sell_content.update(SellTermCode = term_code, Money = record_info.money,
                                                PlayEname = record_info.game_name,
                                                TicketCode = record_info.bet_code,
                                                RunCode = basic_data.serial_num_gen())
                    checkcode = getcheckcode(content.sell_content['RunCode'] + content.general_out_content["PartnerId"]
                                             + content.sell_content["UserId"]
                                             + content.sell_content["TicketCode"]
                                             + content.sell_content["Money"]
                                             + content.sell_content["LoginSession"])
                    content.sell_content.update(CheckCode = checkcode)
                    content.general_out_content.update(ReqContent = content.sell_content)
                    if record_info.case_type in data_set:
                        data_set[record_info.case_type].append((copy.deepcopy(content.general_out_content),
                                                               '{}_{}_{}_{}'.format(business_type,
                                                                                    record_info.game_name,
                                                                                    record_info.case_type,
                                                                                    record_info.record_id)))
    return data_set


def betquery_encash_data(file, business_type= 'bet_query', session = None):
    """
    生成投注查询和兑奖的用例
    :param file:
    :param business_type: 两个取值"bet_query"和"encash"
    :param session:
    :return:
    """
    query_encash_record = collections.namedtuple("Encashrecord", "Playname,UserId,RunCode,TicketCode")
    content = ContentSet()
    encash_data_set = []
    query_data_set = []

    content.encash_content.update(LoginSession = session)

    if file:
        with open(file, 'r', encoding = 'unicode_escape') as f:
            if business_type == 'encash':
                for record in f:
                    record_info = query_encash_record._make(record.strip().split(','))
                    # print("record_info", record_info)
                    content.encash_content.update(UserId = record_info.UserId, RunCode = record_info.RunCode,
                                                  TicketCode = record_info.TicketCode)
                    checkcode = getcheckcode(content.encash_content['UserId'] +
                                                 content.encash_content["TicketCode"])
                    # print('checkcode:', checkcode)
                    content.encash_content.update(CheckCode = checkcode)
                    # # print("item:",  item)
                    content.general_out_content.update(ReqContent = content.encash_content)
                    encash_data_set.append((copy.deepcopy(content.general_out_content),
                                            '{}_{}'.format(record_info.Playname, record_info.TicketCode)))
                return encash_data_set
            if business_type == 'bet_query':
                for record in f:
                    record_info = query_encash_record._make(record.strip().split(','))
                    # print("record_info", record_info)
                    content.bet_query_content.update(RunCode = record_info.RunCode)
                    content.general_out_content.update(ReqContent = content.bet_query_content)
                    query_data_set.append((copy.deepcopy(content.general_out_content),
                                           '{}_{}'.format(record_info.Playname, record_info.TicketCode)))
                return query_data_set


def excutive_test(profix_url, interface_type, content):
        if interface_type in ["login", "sell", "encash"]:
            with open(basic_data.datadir + 'encash_and_query', 'a+', encoding = 'utf-8') as sucess:
                md5, md5_hash = DataHandleToolkit.req_set_md5(content, key=basic_data.gdca_key)
                # basic_data.logger.info('0 进入"login", "sell", "encash"接口处理过程')
                basic_data.logger.debug('Hash值返回成功，md5_hash: %s' % md5_hash)
                basic_data.logger.debug('md5加密后数据返回成功')
                test_url = DataHandleToolkit.req_set_url(profix_url, md5_hash)
                basic_data.logger.debug('URL组装成功，test_url: %s' % test_url)
                # print("url: ", test_url)
                recv = requests.post(test_url, data=md5)
                # print("recv.content", recv.content)
                recv_post = DataHandleToolkit.decode_recv_data(recv, key=basic_data.gdca_key)
                # basic_data.logger.info('返回值解密成功，recv_post: %s' % recv_post)
                # print("recv_post", recv_post)
                if interface_type == 'sell' and recv_post["BackCode"] == '100000':
                    sucess.write(content["ReqContent"]["PlayEname"] + ',' + content["ReqContent"]["UserId"] + ',' +
                                 content["ReqContent"]["RunCode"] + ',' +
                                 recv_post["RespContent"]["TicketCode"] + '\n')
                    basic_data.logger.debug("encash_and_query.txt文件写入成功")
                if interface_type == 'login' and "RespContent" in recv_post:
                    basic_data.logger.debug('Login接口返回成功，recv_post["RespContent"][“LoginSession”]: %s' %
                                            recv_post["RespContent"]['LoginSession'])
                    return recv_post["RespContent"]['LoginSession']

        elif interface_type in ["time", "bet_query", "account_query"]:
            # basic_data.logger.info('0 进入"time", "bet_query", "account_balance"接口处理过程')
            md5, md5_hash = DataHandleToolkit.req_set_md5(content, key=basic_data.old_key)
            basic_data.logger.debug('Hash值返回成功，md5_hash: %s' % md5_hash)
            basic_data.logger.debug('md5加密后数据返回成功')
            # print(md5)
            test_url = DataHandleToolkit.req_set_url(profix_url, md5_hash)
            basic_data.logger.debug('URL组装成功，test_url: %s' % test_url)
            # print("url: ", test_url)
            recv = requests.post(test_url, data=md5)
            # print("http code:", recv.status_code)
            recv_post = DataHandleToolkit.decode_recv_data(recv, key=basic_data.old_key)
            # basic_data.logger.info('返回值解密成功，recv_post: %s' % recv_post)
            # print(recv_post)
            if interface_type == 'time' and "RespContent" in recv_post:
                # print('SysDateTime', recv_post["RespContent"]['SysDateTime'])
                basic_data.logger.info('time接口返回成功，time: %s' % recv_post["RespContent"]['SysDateTime'])
                return recv_post["RespContent"]['SysDateTime']
        basic_data.logger.info('接口返回成功，recv_post %s' % recv_post)
        return recv_post
