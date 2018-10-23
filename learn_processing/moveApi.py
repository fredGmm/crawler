#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import sys

sys.path.append('/mnt/hgfs/code/python/learn_processing')

from WebPageDownClass import WebPageDown

headers = {
   'accept' : 'application/json, text/plain, */*',
   'accept-language' : 'zh-CN,zh;q=0.9',
   'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
   'Cookie': 'PHPSESSID=r39khi5nqoce0tbe1qtc0jikoi',
    'Host':'eolinker.me',
    'Origin':'http://eolinker.me',
    'Referer' : 'http://eolinker.me'
}
url = 'http://eolinker.me/server/index.php?g=Web&c=Api&o=getAllApiList'
# proxy = 'socks5://127.0.0.1:1080'
data = {
    'projectID': 2,
    'groupID' : 2,
    'apiRequestParam' : [],
    'apiResultParam' : [],
    'starred' : 0,
    'apiS':0

}
html = WebPageDown.down_web_page_html(url, headers, proxy=None, retry=1, data=data)
#
print(html['html'].decode('utf-8'))