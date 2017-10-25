#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import multiprocessing
from MongoQueue import MongoQueue
from WebPageDownClass import WebPageDown
import threading
import time
import lxml.html
import re


def multi_crawler(page_url, delay=5, cache=None, callback=None, user_agent='fred_sp', proxy=None, num_retries=1, max_threads=10, timeout=60):
    crawler_queue = MongoQueue()
    # crawler_queue.clear()
    # cache.clear()
    # exit()

    crawler_queue.push(page_url)

    def process_queue():
        while True:
            try:
                url = crawler_queue.pop()
            except KeyError:
                break
            else:

                reg = re.compile(r'.*\d{1,10}\.html.*$') # 判断是 列表页面 还是 帖子文章页面
                if reg.match(url):
                    print(123)
                else: # 列表页
                    #  该页面的html
                    page_html = WebPageDown.down_web_page_html(url, {'User-agent': user_agent}, proxy=proxy,retry=num_retries)
                    tree = lxml.html.fromstring(page_html['html'])
                    list = tree.cssselect('div.titlelink.box>a')
                    for k, title in enumerate(list):
                        print('页面：%s ' % url)
                        article_url = 'https://bbs.hupu.com' + title.get('href')
                        article_title = title.text_content()

                        crawler_queue.push(article_url)

                        cache[article_url] = {'article_content': 'xxxx', 'title':article_title}
                        exit()


                if callback:
                    try:
                        links = callback(url, html) or []
                    except Exception as e:
                        print('Error in callback for: {}: {}'.format(url, e))
                    else:
                        for link in links:
                            crawler_queue.push(link)
                crawler_queue.complete(url)

    threads = []
    while threads or crawler_queue:

        for thread in threads:
            if not thread.is_alive():
                threads.remove(thread)
        while len(threads) < max_threads and crawler_queue.peek():

            thread = threading.Thread(target=process_queue)
            thread.setDaemon(True)
            thread.start()
            threads.append(thread)

        time.sleep(1)


def process_crawler(args, **kwargs):
    cpus = multiprocessing.cpu_count()
    print('cpu 核数：' + str(cpus))
    processes = []
    for i in range(cpus):
        print('启动第 %i 进程' % i)
        p = multiprocessing.Process(target=multi_crawler, args=[args], kwargs=kwargs)
        p.start()
        processes.append(p)

    for p in processes:
        p.join()

