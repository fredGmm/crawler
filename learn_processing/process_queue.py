#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from multiprocessing import Process,Queue
import time, random
from multiprocessing import Pool
import subprocess

def write(queue):
    print('start write process, pid %s' % os.getpid())
    for value in ['小明', '小红', 'storya','xiaochuan','daq']:
        print('写入队列...', value)
        queue.put(value)
        time.sleep(5)

def read(queue):
    print('start read process, pid %s' % os.getpid())
    while queue:
        value = queue.get()
        print('读取队列 ，值：%s' % value)


if __name__ == '__main__':
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    pw.start()
    pr.start()
    pw.join()
    pr.terminate()