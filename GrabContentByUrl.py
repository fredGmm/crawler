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


# 从页面爬取帖子url
def find_article_url_in_page(page_url, delay_days=2, max_depth=1, user_agent='fred_spider', proxy=None, headers=None,
                             num_retry=2, save_info_class=1):
    crawl_pages_queue = [page_url]
    seen = {page_url: 0}  # 防止重复
    article_url_num = 0  # 爬到的帖子数
    num_urls = 0

    # rp = get_robots(page_url)
    # rp.can_fetch(user_agent, page_url) # 检查是否允许爬虫

    delay = Delay(delay_days)
    headers = headers or {}
    if user_agent:
        headers['User-agent'] = user_agent

    while crawl_pages_queue:
        url = crawl_pages_queue.pop()
        depth = seen[url]
        #  delay.wait(url)  # 延时
        html = WebPageDown.down_web_page_html(url, headers, proxy=proxy, retry=num_retry)

        links = []
        if save_info_class:
            tree = lxml.html.fromstring(html['html'])
            list = tree.cssselect('div.titlelink.box>a')

            for k, title in enumerate(list):
                article_url = 'https://bbs.hupu.com' + title.get('href')
                article_title = title.text_content()

                article_html = WebPageDown.down_web_page_html('https://bbs.hupu.com/20565022.html', headers, proxy=proxy, retry=2)
                article_tree = lxml.html.fromstring(article_html['html'])
                #  article_content = article_tree.cssselect('div.floor-show>div.floor_box>table.case>tbody>tr>td>div.quote-content')
                article_content = article_tree.cssselect('div.floor-show>div.floor_box>table>tr>td>div.quote-content')

                s = SaveInfo(article_title, article_url)
                s(content=article_content[0].text_content())

                links.append(article_url)

        print(links)
        exit()

        if depth != max_depth:
            for link in links:
                link = normalize(page_url, link)
                if link not in seen:
                    seen[link] = depth + 1
                    if same_domain(page_url, link):
                        crawl_pages_queue.append(link)

        num_urls += 1
        if num_urls == 500:
            break


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

# C = MongoCache()
# data = C['https://bbs.hupu.com/20188181.html']
# print(data['article_content'])
# exit()
find_article_url_in_page('https://bbs.hupu.com/lol')
