#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymongo import MongoClient
from datetime import datetime, timedelta
import pickle
import zlib
from bson.binary import Binary


class MongoCache:
    def __init__(self, expires=timedelta(days=30)):

        self.conn = MongoClient('127.0.0.1', 27017)

        self.db = self.conn.cache
        #self.db.cache.create_index('timestamp', expire=3600)

    def __contains__(self, url):
        try:
            self[url]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, url):
        """Load value at this URL
        """
        record = self.db.webpage.find_one({'_id': url})
        if record:
            # return record['result']
            return {'article_content' : pickle.loads(zlib.decompress(record['article_content'])), 'title':record['title']}
        else:
            raise KeyError(url + ' does not exist')

    def __setitem__(self, url, data):
        """Save value for this URL
        """
        # record = {'result': result, 'timestamp': datetime.utcnow()}
        record = {'article_content': Binary(zlib.compress(pickle.dumps(data['article_content']))), 'title': data['title'],  'timestamp': datetime.utcnow(), }
        self.db.webpage.update({'_id': url}, {'$set': record}, upsert=True)

    def clear(self):
        self.db.webpage.drop()

