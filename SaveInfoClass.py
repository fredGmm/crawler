#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import chardet
import lxml.html
from MongoCache import MongoCache

class SaveInfo:
    def __init__(self, title, url):

        self.title = title
        self.url = url
        #  self.content = content

    def __call__(self,url, title, content):
        cache = MongoCache()
        cache[url] = {'title':title, 'article_content':content}

        # chardet.detect(rawdata) 查看编码类型

    if __name__ == "__main__":
        cache = MongoCache()
        cache.clear()










