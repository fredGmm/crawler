#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import lxml.html
import urllib.request
import urllib.parse

class ScrapeCallback:
    def __init__(self):
        self.writer = csv.writer(open('./test.csv', 'w'))
        self.fields = ('id', 'link', 'page')
        self.writer.writerow(self.fields)

    def tt(self, url, html):
        tree = lxml.html.fromstring(html)
        row = []
        list = tree.cssselect('div.titlelink.box>a')
        for k, title in enumerate(list):
            #row.append(str(k)+ ','+title.get('href')+','+title.text_content().decode('utf-8').encode('GB2312'))

            row.append(title.get('href') + '\r')
        self.writer.writerow(row)


def download(url, user_agent='fred_spider', proxy=None, retry=3):
    print('下载如下链接：', url)
    headers = {'User-agent': user_agent}
    try:
        request = urllib.request.Request(url, headers=headers)

        opener = urllib.request.build_opener()
        if proxy:
            proxy_params = {urllib.parse.urlparse(url).scheme: proxy}
            opener.add_handler(urllib.request.ProxyHandler(proxy_params))

        html = opener.open(request).read()
    except urllib.request.URLError as e:
        print('下载遇到错误：', e.reason)
        html = None
        if retry > 0:
            if hasattr(e, 'code') and 400 <= e.code <= 600:
                return download(url, retry - 1)
    return html

if __name__ == "__main__":
    html = download('https://bbs.hupu.com/bxj')

    ScrapeCallback().tt('https://bbs.hupu.com/bxj', html)


