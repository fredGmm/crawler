#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import json
sys.path.append('E:\code\scrap\git\crawler')
from WebPageDownClass import WebPageDown


url = 'http://data.wxb.com/rank/article?category=15&page=1&pageSize=20&type=2&order='
# url = 'https://bbs.hupu.com/lol'
headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'http://data.wxb.com/rankArticle?cate=15',
    'Host': 'data.wxb.com',
    'Accept': 'application/json, text/plain, */*',
    'Cookie':'visit-wxb-id=6834c11a678b20f616223ad37d69cce5'
}
html = WebPageDown.down_web_page_html(url, headers, proxy=None, retry=2)

data = html['html'].decode('utf-8')
print(json.loads(data)['data'][0]['title'])

