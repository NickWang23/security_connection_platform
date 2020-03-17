"""
python中有自带的logging模块，只要按照API文档和一些教程操作，就可以搞定
学习资料参考：
API文档：logging模块
网址：https://www.cnblogs.com/Nicholas0707/p/9021672.html
"""

import logging
import configparser
import datetime
import os


# 先列出日志的对应等级，我觉得这个做法好，可以一目了然
logLevel = {
    1: logging.NOTSET,
    2: logging.DEBUG,
    3: logging.INFO,
    4: logging.WARNING,
    5: logging.ERROR,
    6: logging.CRITICAL
}


# 读取配置文件中关于日志的配置项
config = configparser.ConfigParser()
config.read(os.getcwd()+'\scp_python_adaptor\config.ini')
log_level = config.getint('Default', 'loglevel')
log_dir = config.get('Default', 'logfile')
# print(log_level,log_dir)


def log_setting():

    # 创建logger
    logger = logging.getLogger('root_log')
    # 设置日志等级
    logger.setLevel(logLevel[log_level])
    # print("2:",logLevel[log_level])

    # 这地方也要注意，先判断日志文件目录是否存在，再决定后续操作
    if not os.path.exists(log_dir):
        os.mkdir(r'%s' % log_dir)
    log_file = os.path.join(log_dir, datetime.datetime.now().strftime('%Y-%m-%d') + '.log')

    # 当不存在任何日志处理器（handler）时才创建，直接新建新的handler会引起重复输出日志问题
    if not logger.hasHandlers():
        # 创建文件handler,并设置将那个级别以上的日志输出到文件
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.INFO)

        # 创建流输出handler，也就是屏幕输出handler，并设置将ERROR级别即以上的日志输出到屏幕
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)

        # 设置输出格式
        formatter = logging.Formatter(fmt="%(asctime)s %(filename)s %(funcName)s  %(lineno)s %(message)s ", datefmt='%Y/%m/%d %X')

        # 为logger添加日志处理器
        logger.addHandler(file_handler)
        logger.addHandler(ch)

        # 设置输出格式
        file_handler.setFormatter(formatter)
        ch.setFormatter(formatter)

    return logger
