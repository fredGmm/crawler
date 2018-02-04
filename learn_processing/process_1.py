#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from multiprocessing import Process
import time, random
from multiprocessing import Pool
import subprocess

"""Unix/Linux操作系统提供了一个fork()系统调用，它非常特殊。普通的函数调用，调用一次，返回一次，但是fork()调用一次，返回两次，因为操作系统自动把当前进程（称为父进程）复制了一份（称为子进程），然后，分别在父进程和子进程内返回。

子进程永远返回0，而父进程返回子进程的ID。这样做的理由是，一个父进程可以fork出很多子进程，所以，父进程要记下每个子进程的ID，而子进程只需要调用getppid()就可以拿到父进程的ID。"""

# print('进程 %s start' % os.getpid())
#
# pid = os.fork()
#
# if pid == 0:
#     print('1子进程 (%s) and  父进程 is %s.' % (os.getpid(), os.getppid()))
# else:
#     print('2子进程 %s 父进程 %s' % (os.getppid(), pid))


def run_task(name):
    print('子进程%s, pid: %s' % (name,os.getpid()))


if __name__ == '__main__':
    print('父进程 %s' % os.getpid())
    p = Process(target=run_task, args=('gmm',))
    print("子进程开始")
    p.start()
    p.join()
    print('结束')

# def long_task(name):
#     for i in range(2):
#         print('name')
#     # print('run task %s (%s) ...' % (name, os.getpid()))
#     # start = time.time()
#     # time.sleep(random.random() * 3)
#     # end = time.time()
#     # print('Task %s runs %0.2f s ...' % (name, (end - start)))
#
#
# if __name__ == "__main__":
#     print('cpu数目：%s' % os.cpu_count())
#     print('父进程 %s' % os.getpid())
#     p = Pool(4)
#     for i in range(5):
#         p.apply_async(long_task, args=(i,))
#
#     print('等所有的进程跑完吧')
#     p.close()
#     p.join()
#     print('end')

# print('$ cat cat scraping/mongo_test.py')
# p = subprocess.Popen(['cat'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
# output, err = p.communicate(b'set q=mx\npython.org\nexit\n')
# print(output.decode('utf-8'))
# print('Exit code:', p.returncode)
#
# print('Exit code:', )
