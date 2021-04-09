#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
--------------------------------------------------------
# @Contact      :   277383645@qq.com
# @License      :   GPL 
# @Project      :   Security_interface_platform.py    
# @File         :   test_time_sync_login.py
--------------------------------------------------------
@Modify Time      @Author    @Version    
------------      -------    --------  
2021/3/10 14:05   Nick wong      1.0  
--------------------------------------------------------
# @Description  :
收获：
1. pytest的日志设置会自动完成logging模块，对于log对象的设置，
   并劫持日志对象，你只需要和正常使用日志一样就可使用，非常方便
2. pytest的 pytest.ini文件中不能用中文做注释，会报编码错误
--------------------------------------------------------
"""

from init_config import basic_data
from setting_initial_env import Toolkit
import logging
import sys
import io
# 改变标准输出的默认编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='ISO-8859-1')


def test_time_sync():
    time_sync_json = {
                "PartnerId": basic_data.partner_id,
                "TimeStamp": basic_data.current_time(),
                "SerialNum": basic_data.serial_num_gen(),
                "Version": basic_data.version,
                "Token": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
                "ReqContent": {}
    }
    rcv_time = Toolkit.send_and_recv(basic_data.time_sync_profix_url + basic_data.partner_id + '&hashType=md5&hash=', "time",
                                     time_sync_json)
    # print(rcv_time['RespContent']['SysDateTime'])
    logging.info("test_time_sync获取到服务器返回")
    assert rcv_time != 0


def test_login():
    rcv_login = Toolkit.session_id()
    # print(rcv_login['RespContent']['LoginSession'])
    logging.info("test_login获取到服务器返回")
    assert rcv_login != 0
