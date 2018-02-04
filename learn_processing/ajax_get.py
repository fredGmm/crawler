#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import sys

# 简单测试拿取微小宝的接口数据，复用页面请求类 WebPageDownClass

sys.path.append('/mnt/hgfs/python/scraping')
from WebPageDownClass import WebPageDown

url = 'http://wts.peopleyuqing.com/wechat/hotarticle/getarticledaily?classid=102001&date=20171027&_=1509197386084'
html = WebPageDown.down_web_page_html(url, {"User-Agent": "fred_spider"}, proxy=None, retry=1)

json_data = json.loads(html['html'].decode("utf-8"))
print(json_data['hitcount'])
