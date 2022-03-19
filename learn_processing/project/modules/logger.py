#!/usr/local/bin/python3

import logging


def new_logger():
    '''创建一个日志实例
    '''
    # 日志路径
    log_path = "./test.log"
    logging.basicConfig()
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(log_path)
    logger.addHandler(handler)
    return logger
