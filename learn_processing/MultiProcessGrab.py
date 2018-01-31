#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import time, random
from multiprocessing import Pool
from MongoQueue import MongoQueue
from multiprocessing import Process,Queue
from WebPageDownClass import WebPageDown
import lxml.html
from SaveInfoClass import SaveInfo
from MongoCache import MongoCache

def grab_url():
    q = MongoQueue()  # 存储article 的队列

    for page in range(1, 5):
        url = 'https://bbs.hupu.com/lol'
        if page > 1:
            url = url + '-' + str(page)
            #  该页面的html
        page_html = WebPageDown.down_web_page_html(url, {'User-agent': 'fred_sq'}, proxy=None, retry=2)
        tree = lxml.html.fromstring(page_html['html'])
        list = tree.cssselect('div.titlelink.box>a')
        print('列表页面：%s ' % url)
        for k, title in enumerate(list):
            article_url = 'https://bbs.hupu.com' + title.get('href')
            article_title = title.text_content()
            q.push(article_url, article_title)
            # cache[article_url] = {'article_content': 'xxxx', 'title': article_title}



def down_article():
    global article_num
    q = MongoQueue()
    empty_num = 0;
    while True:
        data = q.pop()
        if data:
            print('帖子页面：%s ' % data['_id'])
            # data = cache[url] if cache[url] else None
            url = data['_id']
            title = data['title'] if data['title'] else None
            article_html = WebPageDown.down_web_page_html(url, {'User-agent': 'fred_sq'}, proxy=None, retry=1)

            if article_html['code'] == 200:
                article_tree = lxml.html.fromstring(article_html['html'])

                article_content = article_tree.cssselect('div.floor-show>div.floor_box>table>tbody>tr>td>div.quote-content')
                if article_content:
                    # cache[url] = article_content[0].text_content()
                    s = SaveInfo(title, url, db_name='article')
                    s(content=article_content[0].text_content())

                    article_num += 1
                    print('下载成功帖子数：%s' % article_num)
                else:
                    print('提取内容失败', url)
            else:
                print('抓取错误:', url)

            q.complete(url)
        else:
            print('队列空了')
            time.sleep(3)
            if empty_num <= 3:
                empty_num += 1
            else:
                exit()





if __name__ == "__main__":
    print('cpu数目：%s' % os.cpu_count())
    print('当前进程 %s' % os.getpid())
    article_num = 0

    # q = MongoQueue()
    # cache = MongoCache(db_name="thread")
    # print(q.getCount(), cache.getCount())
    # print(q.clear(), cache.clear())
    # exit()

    url = 'https://bbs.hupu.com/lol'
    pg = Process(target=grab_url)

    pg.start()  #抓取页面 url 进程


    dr_processes = []
    for i in range(3): #抓取页面进程
        dr = Process(target=down_article)
        dr.start()
        dr_processes.append(dr)

    pg.join()
    for dr in dr_processes:
        dr.join()
    print('all end')

