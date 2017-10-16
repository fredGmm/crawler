#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import urllib.parse
#import itertools
import re

# 连续最大的错误数
max_number = 5

error_num = 0





# num = 0
# for page in itertools.takewhile(lambda x: x<=20414400, itertools.count(1)):
# 	url = 'https://bbs.hupu.com/%d.html' % page
# 	html = download(url)
# 	if html is None:
# 		error_num += 1
# 		if error_num > max_number:
# 			break # 达到最大错误数
# 	else:
# 		error_num = 0
# 		print('success ', page)
# 		num += 1
# 		print(num)
# 		pass
# print(download("https://bbs.hupu.com/20405211.html"));


class Throttle:
    """限制 爬取次数
    """

    def __init__(self, delay):
        # 间隔是场
        self.delay = delay

        self.domains = {}

    def wait(self, url):
        domain = urlparse.urlparse(url).netloc
        last_accessed = self.domains.get(domain)

        if self.delay > 0 and last_accessed is not None:
            sleep_secs = self.delay - (datetime.now() - last_accessed).seconds
            if sleep_secs > 0:
                time.sleep(sleep_secs)
        self.domains[domain] = datetime.now()


def link_crawler(seed_url, link_regex):
    """爬取页面中 我们要访问的链接"""
    crawl_queue = [seed_url]

    seen = set(crawl_queue)
    host = '"https://bbs.hupu.com/'
    while crawl_queue:
        url = crawl_queue.pop()
        html = download(url).decode('utf-8')
        for id in get_links(html):
            seen.add(host + id + '.html')
        # if(re.match(link_regex, link)):
        # 	crawl_queue.append(link)

    return seen


def get_links(html):
    """返回页面上的链接"""
    webpage_regex = re.compile(
        r'<div class=\"titlelink box\" style=\"width:645px;\">\n<a\s+href=\"\/(\d{1,10}).html\" >')
    return webpage_regex.findall(html)


print(link_crawler("https://bbs.hupu.com/bxj", 13))
