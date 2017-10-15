#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymongo import MongoClient
conn = MongoClient('localhost', 27017)
db = conn.testdb
db.col.insert({"name":'yanying','province':'江苏','age':25})
