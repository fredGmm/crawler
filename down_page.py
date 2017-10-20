#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import urllib.parse
import urllib.robotparser
from datetime import datetime
import time


def download(url, headers=None, proxy=None, retry=3, data=None):
    print('下载如下链接：', url)
    #headers = {'User-agent': user_agent}
    request = urllib.request.Request(url, headers=headers)
    opener = urllib.request.build_opener()

    if proxy:
        proxy_params = {urllib.parse.urlparse(url).scheme:proxy}
        opener.add_handler(urllib.request.ProxyHandler(proxy_params))

    try:
        response = opener.open(request)
        html = response.read()
        # code = response.code
    except urllib.request.URLError as e:
        print('下载遇到错误：', e.reason)
        html = ''
        if hasattr(e, 'code'):
            code = e.code
            if retry > 0 and 400 <= code <= 600:
                html = download(url, headers, proxy, retry - 1)
        else:
            code = None
    return html


# 从页面爬取帖子url
def find_article_url_in_page(page_url,delay_days=2, max_depth=1, user_agent='fred_spider', proxy=None, headers=None, num_retry=2, resolve_page_class=None):
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
        delay.wait(url)  # 延时
        html = download(url, headers, proxy=proxy, retry=num_retry)
        links = []
        if resolve_page_class:
            links.extend(resolve_page_class(url, html) or [])

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


# 频率限制
class Delay:
    def __init__(self, delay):
        self.delay = delay
        self.domains = {}

    def wait(self, url):
        domain = urllib.parse.urlsplit(url)
        last_visit = self.domains.get(domain)
        if self.delay > 0 and last_visit is not None:
            sleep_seconds = self.delay - (datetime.now() - last_visit).seconds
            if sleep_seconds > 0:
                time.sleep(sleep_seconds)
        self.domains[domain] = datetime.now()
        return domain


#  find_article_url_in_page('https://bbs.hupu.com/lol')
