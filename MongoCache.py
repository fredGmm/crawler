#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymongo import MongoClient
from datetime import datetime, timedelta
import pickle
import zlib
from bson.binary import Binary


class MongoCache:
    def __init__(self, expires=timedelta(days=30), db_name='Cache', collection='web_page'):

        self.conn = MongoClient('192.168.1.111', 27017, connect=False)
        self.db = getattr(self.conn, db_name)
        self.collection = getattr(self.db, collection)
        # self.db.webpage.create_index('timestamp', expireAfterSeconds=expires.total_seconds())

    def __contains__(self, url):
        try:
            self[url]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, url):
        record = self.db.webpage.find_one({'_id': url})
        if record:
            # return record['result']
            return record
            # return {'article_content': pickle.loads(zlib.decompress(record['article_content'])), 'title': record['title']}
        else:
            raise KeyError(url + ' does not exist')

    # 存入数据
    def __setitem__(self, url, record):
        # record = {'result': result, 'timestamp': datetime.utcnow()}
        # record = {'article_content': Binary(zlib.compress(pickle.dumps(data['article_content']))), 'title': data['title'],  'timestamp': datetime.utcnow(), }
        self.collection.update({'_id': url}, {'$set': record}, upsert=True)

    def RemoveOne(self, url):
        record = {'_id': url}
        self.db.webpage.remove(record)


    def getCount(self):
        return self.db.webpage.find().count()


    def clear(self):
        self.db.webpage.drop()

