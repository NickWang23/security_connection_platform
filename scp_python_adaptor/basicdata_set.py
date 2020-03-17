# !/usr/bin/env python
# -*-coding: utf-8-*-

# @ProjectName : jiling_aqjr_proj
# @FileName : basicdata_set.py
# @Time : 2019/11/7 10:12
# @Author : Nick

"""
目的：使用单例模式管理配置文件的读取，确保配置文件信息调用时，因为只初始化一次，还可以加快运行性能，保证程序在多处地方获取的配置信息一致
"""

import random
import time
import collections
import configparser
import os.path
from scp_python_adaptor import log_setting_gdca

"""
python中实现单例模式最简单的两种方法：
一、通过模块调用
在python3中，首次导入模块文件时，会在程序目录下的__pycache__目录中生成pyc文件，
再导入时，将直接加载pyc文件。因此，只需把相关的函数和数据定义在一个模块中，就可以获得一个单例对象了。 

# 读取配置文件中关于java和jar的配置项
config = configparser.ConfigParser()
config.read('config.ini')

# 本机java虚拟机路径及运行参数
jvm_path = config.get('Java', "Java_path")
jar_path = config.get('Java', "jar_path")

# 接口URL前缀
sell_profix_url = config.get('Url_set', 'sell_profix')
time_sync_profix_url = config.get('Url_set', 'time_sync_profix')
encash_profix_url = config.get('Url_set', 'encash_profix')
bet_query_url = config.get('Url_set', 'bet_query_profix')
account_query_url = config.get('Url_set', 'account_query_profix')
login_profix_url = config.get('Url_set', 'login_profix')


# 登录、投注、兑奖3个接口使用
gdca_key = config.get('Key', 'gdca_key')
# 3个查询接口使用（时间同步、自购投注查询、站点余额）
old_key = config.get('Key', 'old_key')


# 投注商ID,用命名元组管理多个渠道商
channel = collections.namedtuple("Channel", 'First,Second,Three')
channel_id = channel._make([config.get('Channel', 'first'), config.get('Channel', 'second'), config.get('Channel', 'third')])

# 自助终端的编号
userid = config.get('Basic_infor', 'userid')
# 渠道ID
partner_id = config.get('Basic_infor', 'partner_id')
# 版本
version = config.get('Basic_infor', 'version')

def serial_num_gen():
    # 生成15位随机列号
    return str(random.randrange(1, 9999)) + str(random.randrange(1, 9999)) + str(random.randrange(1, 9999))

def current_time():
    # 生成当前时间时间戳
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

二、使用__new__方法

    __new__：创建实例对象时调用的构造方法
    __init__ ：实例初始化方法，用于设置实例的相关属性

当实例化一个对象时，先调用__new__方法（未定义时调用object.__new__）实例化对象，然后调用__init__方法进行对象初始化。
所以，可以声明一个私有类变量__instance。当__instance不为None时，表示系统中已有实例，直接返回该实例；若__instance为None时，
表示系统中还没有该类的实例，则创建新实例并返回。

"""


class Dataset(object):
    __instance = None

    def __init__(self):
        # 读取配置文件中关于java和jar的配置项
        config = configparser.ConfigParser()
        config.read(os.getcwd()+'\scp_python_adaptor\config.ini')

        # 初始化日志调用
        self.log_level = config.get('Default', "loglevel")
        self.log_dir = config.get('Default', "logfile")
        self.logger = log_setting_gdca.log_setting()

        # 初始化销售过程中产生的文件存放的目录
        result_dir = config.get('Default', "resultdir")
        if not os.path.exists(result_dir):
            os.mkdir(r'%s' % result_dir)
        self.result_dir = result_dir + '\\'

        # 初始化销售过程中产生的文件存放的目录
        datadir = config.get('Default', "datadir")
        if not os.path.exists(datadir):
            os.mkdir(r'%s' % datadir)
        self.datadir = datadir + '\\'

        # 接口URL前缀
        self.sell_profix_url = config.get('Url_set', 'sell_profix')
        self.time_sync_profix_url = config.get('Url_set', 'time_sync_profix')
        self.encash_profix_url = config.get('Url_set', 'encash_profix')
        self.bet_query_url = config.get('Url_set', 'bet_query_profix')
        self.account_query_url = config.get('Url_set', 'account_query_profix')
        self.login_profix_url = config.get('Url_set', 'login_profix')

        # 登录、投注、兑奖3个接口使用
        self.gdca_key = config.get('Key', 'gdca_key')
        # 3个查询接口使用（时间同步、自购投注查询、站点余额）
        self.old_key = config.get('Key', 'old_key')

        # 投注商ID,用命名元组管理多个渠道商
        channel = collections.namedtuple("Channel", 'First,Second,Three')
        self.channel_id = channel._make(
            [config.get('Channel', 'first'), config.get('Channel', 'second'), config.get('Channel', 'third')])

        # 自助终端的编号
        self.userid = config.get('Basic_infor', 'userid')
        # 渠道ID
        self.partner_id = config.get('Basic_infor', 'partner_id')
        # 版本
        self.version = config.get('Basic_infor', 'version')
        # 登录密码
        self.login_pass = config.get('Basic_infor', 'loginpass')
        # 登录类型
        self.login_type = config.get('Basic_infor', 'logintype')
        # MAC地址
        self.mac_address = config.get('Basic_infor', 'macaddress')

    @staticmethod
    def serial_num_gen():
        # 生成15位随机列号
        return str(random.randrange(1, 9999)) + str(random.randrange(1, 9999)) + str(random.randrange(1, 9999))

    @staticmethod
    def current_time():
        # 生成当前时间时间戳
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance


basic_data = Dataset()

# 单例模式验证
# basic_data1 = Dataset()
# print(id(basic_data), id(basic_data1))
