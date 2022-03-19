#!/usr/local/bin/python3
# -*- coding:utf-8 -*-
import sys

sys.path.append("E:\source_code\crawler\learn_processing\project\libs")
from s import sum11
import logger

if __name__ == '__main__':

    print("fsaf")
    lL = logger.new_logger()
    lL.info(111)
    sum11()

    try:
        print('try...')
        r = 10 / 0
        print('result:', r)
    except ZeroDivisionError as e:
        print('except:', e)
        logging.exception(e)
    finally:
        print('finally...')
        print('END')
