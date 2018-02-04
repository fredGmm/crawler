#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from multiprocessing import Process,Queue
import time, random
from multiprocessing import Pool
import multiprocessing
import subprocess

import threading

local_class = threading.local()
def process_stu():
    std = local_class.student
    print('hello %s (in %s)' % (std, threading.current_thread().name))

def pro_thread(name):
    local_class.student = name
    process_stu()

t1 = threading.Thread(target=pro_thread, args=('stoya',))
t2 = threading.Thread(target=pro_thread, args=('daq',))
t1.start()
t2.start()
t1.join()
t2.join()




