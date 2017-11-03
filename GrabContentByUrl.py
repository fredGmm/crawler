#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import urllib.parse
import urllib.robotparser
from datetime import datetime
import time
import lxml.html

from WebPageDownClass import WebPageDown
from MongoCache import MongoCache
from WebPageDownClass import Delay
from SaveInfoClass import SaveInfo
from GetImageFromHtml import GetImageFromHtml

import os
import sqlite3
import requests
from win32.win32crypt import CryptUnprotectData
import http
import win32crypt

import subprocess

# 从页面爬取帖子url
def find_article_url_in_page(page_url, page_num=1, delay_days=2, max_depth=1, user_agent='fred_spider', proxy=None, headers=None,
                             num_retry=2, is_save_cache = None):
    crawl_pages_queue = [page_url]
    seen = {page_url: 0}  # 防止重复
    article_url_num = 0  # 爬到的帖子数
    num_urls = 0

    # rp = get_robots(page_url)
    # rp.can_fetch(user_agent, page_url) # 检查是否允许爬虫
    delay = Delay(delay_days)
    headers = headers or {}

    if page_num > 10:  # hupu 超过十页 开始需要登录啦
        cookie_string = ''
        for i, j in getcookiefromchrome().items():
            cookie_string += i + '=' + j + ';'  # 拼接 cookie
        headers = {'Cookie': cookie_string}

    if user_agent:
        headers['User-agent'] = user_agent

    while crawl_pages_queue:
        url = crawl_pages_queue.pop()
        depth = seen[url]
        #  delay.wait(url)  # 延时
        html = WebPageDown.down_web_page_html(url, headers, proxy=proxy, retry=num_retry,)

        links = []
        if is_save_cache:
            tree = lxml.html.fromstring(html['html'])
            list = tree.cssselect('div.titlelink.box>a')  # 每个帖子的url集合

            for k, title in enumerate(list):
                print('第 %s 页' % page_num)
                article_url = 'https://bbs.hupu.com' + title.get('href')  # 每个帖子的url
                article_title = title.text_content()
                article_html = WebPageDown.down_web_page_html(article_url, headers, proxy=proxy, retry=2)
                if article_html['code'] != 200:
                    print('第 %s 页,略过这个帖子 %s ' % (page, article_url))
                    continue
                article_tree = lxml.html.fromstring(article_html['html'])

                #  article_content = article_tree.cssselect('div.floor-show>div.floor_box>table.case>tbody>tr>td>div.quote-content')  # 帖子主体
                article_content = article_tree.cssselect('div.floor-show>div.floor_box>table>tr>td>div.quote-content')

                if article_content:
                    # 图片采集
                    images = []
                    getImage = GetImageFromHtml()
                    images = getImage.fromHp(article_tree)

                    record = {'article_content': article_content[0].text_content(), 'title': article_title, 'images':images, 'category':'lol','timestamp': datetime.utcnow(), }

                    is_save_cache[article_url] = record
                    article_url_num += 1
                    links.append(article_url)

        print('总共下载了%s 帖子' % article_url_num)
        # if depth != max_depth:
        #     for link in links:
        #         link = normalize(page_url, link)
        #         if link not in seen:
        #             seen[link] = depth + 1
        #             if same_domain(page_url, link):
        #                 crawl_pages_queue.append(link)
        #
        # num_urls += 1
        # if num_urls == 500:
        #     break


def getcookiefromchrome(host='.hupu.com'):
    cookiepath = os.environ['LOCALAPPDATA'] + r"\Google\Chrome\User Data\Default\Cookies"
    sql = "select host_key,name,encrypted_value from cookies where host_key='%s'" % host
    with sqlite3.connect(cookiepath) as conn:
        cu = conn.cursor()
        cookies = {name: CryptUnprotectData(encrypted_value)[1].decode() for host_key, name, encrypted_value in
                   cu.execute(sql).fetchall()}

        return cookies

def get_robots(url):
    """Initialize robots parser for this domain
    """
    rp = urllib.robotparser.RobotFileParser()
    rp.set_url(urllib.parse.urljoin(url, '/robots.txt'))
    rp.read()
    return rp


def normalize(seed_url, link):
    link, _ = urllib.parse.urldefrag(link)  # remove hash to avoid duplicates
    return urllib.parse.urljoin(seed_url, link)


def same_domain(url1, url2):
    """Return True if both URL's belong to same domain
    """
    return urllib.parse.urlparse(url1).netloc == urllib.parse.urlparse(url2).netloc


C = MongoCache(db_name='hupu')
print(C.getCount())

# C.clear()
# C.RemoveOne(url='https:bbs.hupu.com//20188181.html')

# data = C['https://bbs.hupu.com/20188181.html']
# print(data['article_content'])
# exit()

start = time.clock()
for page in range(11, 20):
    url = 'https://bbs.hupu.com/lol'
    if page > 1:
        url = url + '-' + str(page)
    find_article_url_in_page(url, page_num=page,is_save_cache=C)
end = time.clock()
print(" run time is : %.03f seconds" % (end-start))


