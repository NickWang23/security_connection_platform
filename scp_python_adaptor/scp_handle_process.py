# -*-coding: utf-8-*-

import json
import hashlib
import requests
import collections
from scp_python_adaptor import sm4decode
from scp_python_adaptor.basicdata_set import basic_data


def md5(dt):
    """进行md5加密"""
    h1 = hashlib.md5()
    h1.update(dt)
    return h1.hexdigest().upper()


def getcheckcode(instring):
    """获取MD5校验码"""
    ret = 0
    for i in range(len(instring)):
        ret = ret+ord(instring[i])
    ret = ret % 100000
    outstring = str(ret)
    for i in range(5-len(outstring)):
        outstring = "0" + outstring
    return outstring


class ContentSet:

    @staticmethod
    def time_stamp_gen():
        # 生成服务器时间时间戳
        time_req = {
            "PartnerId": basic_data.partner_id,
            "TimeStamp": basic_data.current_time(),
            "SerialNum": basic_data.serial_num_gen(),
            "Version": basic_data.version,
            "Token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "ReqContent": {
            }
        }
        return DataHandleToolkit.excutive_test(basic_data.time_sync_profix_url, 'time', time_req)

    @staticmethod
    def login():
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

    def __init__(self):
        self.general_out_content = {"PartnerId": basic_data.partner_id,
                                    "TimeStamp": ContentSet.time_stamp_gen(),
                                    "SerialNum": basic_data.serial_num_gen(),
                                    "Version": basic_data.version,
                                    "Token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                                    "ReqContent": ""}
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

        self.encash_content = {
                "UserId": basic_data.userid,
                "RunCode": "",
                "TicketCode": "",
                "CheckCode": "",
                "LoginSession": ""}

        self.account_query_content = {
            "ChannelId": ""
        }

        self.bet_query_content = {
            "RunCode": ""
        }


# @allure.step
class DataHandleToolkit:
    @staticmethod
    def req_set_url(profix_url=None, hash_content=None):
        # basic_data.logger.debug("0 进入URL地址组装函数")
        return profix_url + str(hash_content)

    @staticmethod
    def req_set_md5(raw_data, key=''):
        # 使用separators参数去掉dumps生成的字符串中逗号和冒号后面的空格
        json_string = json.dumps(raw_data, separators=(',', ':'))
        # sm4加密
        md5_bytes = sm4decode.sm4encrype(key, json_string)
        # md5加密
        md5_hash = md5(md5_bytes)
        return md5_bytes, md5_hash

    @staticmethod
    def decode_recv_data(recv_data, key=''):
        # 解密返回数据，得到String类型的数据
        java_byte_array = sm4decode.sm4decrypt(key, recv_data.content)

        return json.loads(java_byte_array)

    @classmethod
    def excutive_test(cls, profix_url, interface_type, content):
        if interface_type in ["login", "sell", "encash"]:
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
                return recv_post["RespContent"]['SysDateTime']
        basic_data.logger.info('接口返回成功，recv_post %s' % recv_post)
        return recv_post

    @staticmethod
    def per_record_handle(file=None, tag= None, term_code = None):
        """
        从文件中读取所有的销售注码，然后把每行存储在一个命名元组（namedtuple）中
        :param file: 数据源文件
        :param tag: 两个取值’sell和 'encash'
        :param term_code:
        :return:
        """
        # 从数据文件中读取投注数据，注意最后一个字段comment中的注释不要用逗号，防止在解析时被认成分隔符
        sell_record = collections.namedtuple("Sellrecord", "record_id, game_name,bet_type, bet_code, money, case_type, comment")
        query_encash_record = collections.namedtuple("Encashrecord", "UserId,RunCode,TicketCode")
        content = ContentSet()
        # 兑奖或销售前先做一次登录，获取loginsession
        login_session = ContentSet.login()
        content.sell_content.update(LoginSession=login_session)
        content.encash_content.update(LoginSession = login_session)
        # unicode-escape编码集，他是将unicode内存编码值直接存储
        if file:
            with open(file, 'r', encoding='unicode_escape') as f:
                if tag == 'sell':
                    with open(basic_data.datadir + "bet_success_data.txt", 'w+', encoding = 'utf-8') as sucess, \
                            open(basic_data.result_dir + "bet_detail_record.txt", 'w+', encoding = 'utf-8') as record_file:
                        for record in f:
                            # print("split", record.split(','))
                            # 直接使用namedtuple的_make方法将解析后的文件行数据转换成namedtuple实例，并存储在records列表中
                            # 组合生成每条记录
                            record_info = sell_record._make(record.strip().split(','))
                            content.sell_content.update(SellTermCode=term_code, Money=record_info.money,
                                                        PlayEname=record_info.game_name, TicketCode=record_info.bet_code,
                                                        RunCode= basic_data.serial_num_gen())
                            checkcode = getcheckcode(content.sell_content['RunCode'] +
                                                         content.general_out_content["PartnerId"] +
                                                         content.sell_content["UserId"] +
                                                         content.sell_content["TicketCode"] +
                                                         content.sell_content["Money"] +
                                                         content.sell_content["LoginSession"]
                                                         )
                            content.sell_content.update(CheckCode=checkcode)
                            content.general_out_content.update(ReqContent = content.sell_content)
                            # 修复小坑：在存储嵌套字典的时候要注意浅拷贝的问题，需要使用深拷贝方法
                            # records.append(copy.deepcopy(content.general_out_content))
                            basic_data.logger.info("销售请求开始")
                            # record = copy.deepcopy(item)
                            # print("item", item)
                            sell_result = DataHandleToolkit.excutive_test(basic_data.sell_profix_url, "sell",
                                                                                           content.general_out_content)
                            basic_data.logger.info("销售成功")
                            # print("sell_result", sell_result)
                            if "RespContent" in sell_result:
                                sucess.write(content.general_out_content["ReqContent"]["UserId"] + ',' +
                                             content.general_out_content["ReqContent"]["RunCode"] + ',' +
                                             sell_result["RespContent"]["TicketCode"] + '\n')
                                record_file.write(str(sell_result) + '\n')
                                basic_data.logger.debug("bet_success_data文件写入成功")
                            else:
                                record_file.write("error record: runcode: %s,Money: %s,SellTerm: %s,betcode: %s\n" %
                                                  (content.general_out_content['ReqContent']['RunCode'],
                                                   content.general_out_content['ReqContent']['Money'],
                                                   content.general_out_content['ReqContent']['SellTermCode'],
                                                   content.general_out_content['ReqContent']['TicketCode']))
                                record_file.write("sell_result: %s\n" % sell_result)
                                basic_data.logger.debug("bet_detail_record文件写入成功")
                    return sell_result
                if tag == 'encash':
                    with open(basic_data.result_dir + "encash_detail_record.txt", 'w+') as encash_detail_file:
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
                            # # 修复小坑：在存储嵌套字典的时候要注意浅拷贝的问题，需要使用深拷贝方法
                            # records.append(copy.deepcopy(content.general_out_content))
                            basic_data.logger.info("兑奖请求开始")
                            encash_result = DataHandleToolkit.excutive_test(basic_data.encash_profix_url, "encash",
                                                                            content.general_out_content)
                            basic_data.logger.info("兑奖请求成功返回： %s" % encash_result)

                            # print("encash_result", encash_result)
                            if "RespContent" in encash_result:
                                encash_detail_file.write(str(encash_result) + '\n')
                            else:
                                encash_detail_file.write("error record: runcode: %s,,betcode: %s\n" %
                                                         (content.general_out_content['ReqContent']['RunCode'],
                                                          content.general_out_content['ReqContent']['TicketCode']))
                                encash_detail_file.write("encash_result: %s\n" % encash_result)
                                basic_data.logger.info("兑奖请求错误信息成功记录")
                    return encash_result
                if tag == 'bet_query':
                    with open(basic_data.result_dir + "bet_query_record.txt", "w+") as result:
                        for record in f:
                            basic_data.logger.info("自助终端投注查询开始")
                            record_info = query_encash_record._make(record.strip().split(','))
                            content.bet_query_content.update(RunCode = record_info.RunCode)
                            content.general_out_content.update(ReqContent = content.bet_query_content)
                            bet_query_result = DataHandleToolkit.excutive_test(basic_data.bet_query_url, "bet_query",
                                                                               content.general_out_content)
                            basic_data.logger.info("自主终端投注查询成功返回： %s" % bet_query_result)
                            # print("bet_query_result", bet_query_result)
                            if "RespContent" in bet_query_result:
                                result.write(str(bet_query_result) + '\n')
                            else:
                                result.write("error record: runcode: %s\n" % record['ReqContent']['RunCode'])
                                result.write("bet_query_result: %s\n" % bet_query_result)
                                basic_data.logger.info("自主终端投注查询错误信息成功记录")
                    return bet_query_result
        if tag == 'account_query':
            basic_data.logger.info("渠道商账户金额查询开始")
            content.account_query_content.update(ChannelId = basic_data.channel_id.First)
            content.general_out_content.update(ReqContent = content.account_query_content)
            account_query_result = DataHandleToolkit.excutive_test(basic_data.account_query_url,
                                                                   "account_query", content.general_out_content)
            # print("account_query_result", account_query_result)
            basic_data.logger.info("渠道商账户金额查询成功 %s" % account_query_result)
            return account_query_result
