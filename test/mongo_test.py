#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymongo import MongoClient
conn = MongoClient('127.0.0.1', 27017)

url = 'bbs.hupu.com'
db = conn.cache
# db.webpage.insert({'url':'bbs.hupu.com', 'html':'fdsafasdfasf1111111111111'})

db.webpage.update({'_id': url}, {'$set': {'html': '网页内容'}}, upsert=True)
