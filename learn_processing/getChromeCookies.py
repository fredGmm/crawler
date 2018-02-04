#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sqlite3
import requests
from win32.win32crypt import CryptUnprotectData

def getcookiefromchrome(host='.oschina.net'):
    cookiepath=os.environ['LOCALAPPDATA']+r"\Google\Chrome\User Data\Default\Cookies"
    sql="select host_key,name,encrypted_value from cookies where host_key='%s'" % host
    with sqlite3.connect(cookiepath) as conn:
        cu=conn.cursor()
        cookies={name:CryptUnprotectData(encrypted_value)[1].decode() for host_key,name,encrypted_value in cu.execute(sql).fetchall()}
        print(cookies)
        return cookies

#运行环境windows 2012 server python3.4 x64 chrome 50
#以下是测试代码
#getcookiefromchrome()
#getcookiefromchrome('.baidu.com')

# url='http://my.oschina.net/'
url = 'https://www.zhihu.com/'

httphead={'User-Agent':'Safari/537.36',}

#设置allow_redirects为真，访问http://my.oschina.net/ 可以跟随跳转到个人空间
r=requests.get(url,headers=httphead,cookies=getcookiefromchrome('.zhihu.com'),allow_redirects=1)
print(r.text)