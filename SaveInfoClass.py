#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# import chardet
import lxml.html
from MongoCache import MongoCache

class SaveInfo:
    def __init__(self, title, url, db_name='Cache'):

        self.title = title
        self.url = url
        self.db_name= db_name
        #  self.content = content

    def __call__(self, content):
        cache = MongoCache(db_name=self.db_name)
        cache[self.url] = {'title': self.title, 'article_content': content}

        # chardet.detect(rawdata) 查看编码类型

    if __name__ == "__main__":
        cache = MongoCache()
        cache.clear()










