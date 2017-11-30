#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from WebPageDownClass import WebPageDown
import json
import urllib.parse
import pymysql
import time

conn = pymysql.Connect(host='192.168.1.111', port=3306, user='root', passwd='xiaoming', db='web_arashi', charset='utf8')
cursor = conn.cursor()
headers = {
    'Accept': 'application/json, text/plain, */*',
    'Host' : 'data.wxb.com',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    # 'Accept-Encoding':'gzip, deflate',
    'Referer' : 'http://data.wxb.com/rank?category=15',
    'X-Requested-With': 'XMLHttpRequest',
    'Cookie': 'visit-wxb-id=6834c11a678b20f616223ad37d69cce5;', # 关键点啊，特么在cookie里埋标识
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
}

# article_html = WebPageDown.down_web_page_html(ajax_url, headers, proxy=None, retry=2)
#
# data = json.loads(article_html['html'])

ajax_url = 'http://data.wxb.com/rank/article?category=15&%s&type=2&order=index_scores-desc'
for page in range(1, 10):
    param = urllib.parse.urlencode({'pageSize':20, 'page':page})
    url = (ajax_url % param)
    article_html = WebPageDown.down_web_page_html(url, headers, proxy=None, retry=2)
    data = json.loads(article_html['html'])
    print('页码' ,page,'数目', len(data['data']))

    for row in data['data']:
        timeArray = time.strptime(row['update_time'], "%Y-%m-%d %H:%M:%S")

        sqlInsert = "insert into wxb_title(title,date) values('%s','%s')"
        sql = (sqlInsert % (row['title'], time.strftime("%Y%m%d", timeArray)))
        cursor.execute(sql)
        conn.commit()
        # print(row['title'])



