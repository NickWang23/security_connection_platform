#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
--------------------------------------------------------
# @Contact      :   277383645@qq.com
# @License      :   GPL
# @Project      :   Security_interface_platform.py
# @File         :   init_config.py
--------------------------------------------------------
@Modify Time      @Author    @Version
------------      -------    --------
2021/3/10 14:05   Nick wong      1.0
--------------------------------------------------------
# @Description  :    读取配置文件的值初始化基本设置
--------------------------------------------------------
"""
import configparser
import random
import time
import pathlib
import pymysql


def db_connection():
    """
        读取pytest.ini中关于数据库的配置项db并连接数据库
        :return: 返回一个数据库连接对象
    """
    try:
        # 设置pytest.ini的路径
        # 坑：pathlib.Path的中的相对路径和你的运行路径密切相关：这里可以正确运行的条件是：
        #    你运行pytest时的目录是项目的最顶层根目录,否则不会识别到pytest.ini文件
        pytest_path = pathlib.Path('pytest.ini')
        # print('pytest_path:', str(pytest_path))
        # get db config
        db_config = configparser.ConfigParser()
        db_config.read(str(pytest_path))
        # print(db_config.sections())
        db_host = db_config['DB']['host']
        db_user = db_config.get('DB', 'user')
        db_pwd = db_config.get('DB', 'password')
        db = db_config.get('DB', 'db')
        db_charset = db_config.get('DB', 'charset')
        connection = pymysql.connect(host=db_host, user=db_user, password=db_pwd, db=db,
                                     charset=db_charset,
                                     cursorclass=pymysql.cursors.DictCursor)
        # print('DB:', type(connection))
        return connection
    except Exception as e:
        print("读取配置文件或连接数据库错误：", e)


def get_db_data(sql, count='all'):
    """
    从数据库查询数据，并返回指定的记录条数
    :param sql: SQL查询语句
    :param count: 指定要返回记录的条数，默认返回所有查询结果。
    :return: 返回一个数据集列表，每个列表元素代表一条记录
    """
    try:
        connection = db_connection()
        with connection.cursor() as cursor:
            # 注意采坑：这里的SQL语句要和mysql语法要完全一样
            cursor.execute(sql)
            # 选择返回的数据数量，暂时为了测试只选择4条
        if count == 'all':
            result = cursor.fetchall()
            # print(result)
        else:
            result = cursor.fetchmany(int(count))
        connection.close()
        return result
    except Exception as e:
        print("读取配置文件或连接数据库错误：", e)


class DataSet(object):
    """
    读取配置文件中的配置项，并以单例模式的方式返回
    """
    __instance = None
    
    def __init__(self):
        # 读取配置文件中关于java和jar的配置项
        config = configparser.ConfigParser()
        pytest_path = pathlib.Path('pytest.ini')
        config.read(str(pytest_path))
        # print(config.sections())
        
        # 接口URL前缀
        self.sell_profix_url = config.get('Url_set', 'sell_profix')
        self.time_sync_profix_url = config.get('Url_set', 'time_sync_profix')
        self.encash_profix_url = config.get('Url_set', 'encash_profix')
        self.bet_query_url = config.get('Url_set', 'bet_query_profix')
        self.account_query_url = config.get('Url_set', 'account_query_profix')
        self.login_profix_url = config.get('Url_set', 'login_profix')
        
        # 登录、投注、兑奖3个接口使用
        self.gm_key = config.get('Key', 'gm_key')
        # 3个查询接口使用（时间同步、自购投注查询、站点余额）
        self.old_key = config.get('Key', 'old_key')
        
        # 终端信息读取
        # 自助终端的编号
        self.user_id = config.get('terminal_info', 'user_id')
        # MAC地址
        self.mac_address = config.get('terminal_info', 'mac_address')
        # 渠道ID
        self.partner_id = config.get('terminal_info', 'partner_id')
        # 版本
        self.version = config.get('Basic_info', 'version')
        # 登录密码
        self.login_pass = config.get('terminal_info', 'login_pwd')
        # 登录类型
        self.login_type = config.get('Basic_info', 'logintype')
        
        # 取新期
        new_terms = get_db_data("SELECT play_ename,MAX(term_code) FROM hot_term  GROUP BY play_ename;", count='all')
        for item in new_terms:
            if item['play_ename'] == 'B001':
                self.ball_term_code = item['MAX(term_code)']
            if item['play_ename'] == 'ZCKL8':
                self.k8_term_code = item['MAX(term_code)']
            if item['play_ename'] == 'QL730':
                self.QL730_term_code = item['MAX(term_code)']
            if item['play_ename'] == 'S3':
                self.d3_term_code = item['MAX(term_code)']
    
    @classmethod
    def serial_num_gen(cls):
        # 生成15位随机列号
        return str(random.randrange(1, 9999)) + str(random.randrange(1, 9999)) + str(random.randrange(1, 9999))
    
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


basic_data = DataSet()

# print(basic_data.d3_term_code)
