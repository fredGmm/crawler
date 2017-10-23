#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.parse
from datetime import datetime
import time
import random
import urllib.request


class WebPageDown:
    def __init__(self, user_agent='fred_spider', proxy=None, delay_days=2, retry=2, cache=None):
        self.delay_days = Delay(delay_days)
        self.user_agent = user_agent
        self.proxy = proxy
        self.retry = retry
        self.cache = cache

    def __call__(self, url):
        result = None
        if self.cache:
            try:
                result=self.cache[url]
            except KeyError:
                pass
            else:
                if self.retry > 0 and 500 <= result['code'] < 600:
                    result = None

        if result is None:
            self.delay_days.wait(url)
            proxy = random.choice(self.proxy) if self.proxy else None
            headers = {'User-agent': self.user_agent}
            result = self.down_web_page_html(url, headers, retry=3, )
            if self.cache:
                self.cache[url] = result

        return result['html']

    def down_web_page_html(url, headers=None, proxy=None, retry=3, data=None):
        print('下载如下链接：', url)
        # headers = {'User-agent': user_agent}
        request = urllib.request.Request(url, headers=headers)
        opener = urllib.request.build_opener()

        if proxy:
            proxy_params = {urllib.parse.urlparse(url).scheme: proxy}
            opener.add_handler(urllib.request.ProxyHandler(proxy_params))
        try:
            response = opener.open(request)
            html = response.read()
            code = response.code
        except urllib.request.URLError as e:
            print('下载遇到错误：', e.reason)
            html = ''
            if hasattr(e, 'code'):
                code = e.code
                if retry > 0 and 400 <= code <= 600:
                    WebPageDown.down_web_page_html(url, headers, proxy, retry - 1)
            else:
                code = None
        return {'html': html, 'code': code}


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
