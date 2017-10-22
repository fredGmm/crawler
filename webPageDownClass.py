#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.parse
from datetime import datetime
import time

class webPageDownClass:

    def __init__(self, user_agent='fred_spider', proxy=None, delay_days=2, retry=2, cache=None):
        self.delay_days = Delay(delay_days)
        self.user_agent = user_agent
        self.proxy = proxy
        self.retry = retry
        self.cache = cache


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