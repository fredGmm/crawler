#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import lxml.html
from down_page import download


# import chardet

class ScrapeCallback:
    def __init__(self, html):
        self.writer = csv.writer(open('./test.csv', 'w'))
        self.fields = ('link', 'title')
        self.writer.writerow(self.fields)
        self.html = html

    def __call__(self, page_html, host):
        # chardet.detect(rawdata) 查看编码类型
        tree = lxml.html.fromstring(page_html)
        row = []
        list = tree.cssselect('div.titlelink.box>a')
        for k, title in enumerate(list):
            # row.append(str(k)+ ','+title.get('href')+','+title.text_content().decode('utf-8').encode('GB2312'))

            row.append(host + title.get('href'))
            row.append(title.text_content())
        self.writer.writerow(row)



if __name__ == "__main__":
    html = download('https://bbs.hupu.com/bxj')

    ScrapeCallback().__call__('https://bbs.hupu.com/bxj', html)


