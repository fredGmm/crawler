#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from multiprocessing import Process,Queue
import time, random
from multiprocessing import Pool
import multiprocessing
import subprocess

import threading

# def loop():
#     print('线程开跑 ，name：%s' % threading.current_thread().name)
#     n = 0
#     while n<5:
#         n = n+1
#         print('第 %s 个 thread %s ' % (n, threading.current_thread().name))
#         time.sleep(1)
#
#
# print('线程开始，name: %s' % threading.current_thread().name)
# t = threading.Thread(target=loop, name='')
# t.start()
# t.join()
# print('end')

# queue_count = 12
# lock = threading.Lock()
#
#
# def change(count):
#     global queue_count
#     queue_count = queue_count + count
#     queue_count = queue_count - count
#
#
# def run_thread(n):
#     for i in range(10000000):
#         lock.acquire()
#         try:
#              change(n)
#         finally:
#             lock.release()
#
#
# t1 = threading.Thread(target=run_thread, args=(5, ))
# t2 = threading.Thread(target=run_thread, args=(8, ))
# # t3 = threading.Thread(target=change, args=(3, ))
# # t4 = threading.Thread(target=change, args=(8, ))
# t1.start()
# t2.start()
#
# t1.join()
# t2.join()
#
# print(queue_count)

# def loop():
#     x = 0
#     while True:
#         x=x ^ 1
#
# for i in range(1):
#     t = threading.Thread(target=loop)
#     t.start()





