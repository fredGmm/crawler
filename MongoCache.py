#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pymongo import MongoClient
from datetime import datetime, timedelta
import pickle
import zlib
from bson.binary import Binary


class MongoCache:
    def __init__(self, client=None, expires=timedelta(days=30)):
        self.conn = MongoClient('127.0.0.1', 27017) if client is None else client

        self.db = self.conn.cache
        self.db.webpage.create_index('timestamp', expire=expires.total_seconds())

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
            return pickle.loads(zlib.decompress(record['result']))
        else:
            raise KeyError(url + ' does not exist')

    def __setitem__(self, url, result):
        """Save value for this URL
        """
        # record = {'result': result, 'timestamp': datetime.utcnow()}
        record = {'result': Binary(zlib.compress(pickle.dumps(result))), 'timestamp': datetime.utcnow()}
        self.db.webpage.update({'_id': url}, {'$set': record}, upsert=True)

    def clear(self):
        self.db.webpage.drop()

