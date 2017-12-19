#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

sys.path.append('/mnt/hgfs/python/scraping')
# sys.path.append('D:\code\python\scraping')
from WebPageDownClass import WebPageDown

headers = {
   # 'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
   # 'accept-language' : 'zh-CN,zh;q=0.9',
   'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
   'cookies': 'SID=AAUWq91AyVEBDtiXnXTCzGds4bO4YibY2CdH-KosGgeWMRP3kHVdYUsuZ9v5ZGD-AOZ3sw.; HSID=Ak_Ob66zroGWGfOg7; SSID=Aytj7SyqvXB-xFPeU; APISID=zChe30jo0cpSIT4I/A-B6vtmKKFyiZNGqo; SAPISID=9d8-cPD1XdDvqWOO/AblqcREh7NX_IGpv0; NID=119=OXcQlLJTagB3pcyI-6pubPweZSJbcJoG2XVdG0Jq3Dw2knuhICSVdP0UOv5nCjoGD0jWPK76Y73gvi1BXuvtEyoKd6v4R173tt2F0suWZAD78qZ3M_qTO6F4UfK76tXjFDZ3nKGFJuR8ISZdRkceQg2N0OYT-9UdrLHClvLTr6Sn_qpEDV1Gfg88u21v8q4bYQwhJ9SskhpQQKQ; 1P_JAR=2017-12-18-6; SIDCC=AE4kn79jNPO_GtUFE2U_KiFvhruYiU8ZlSHzFQk4KBqSQEvmWzkyWmqPtSfsrac93-sSQvu2ejvoFdjQUE5I',
}
url = 'https://api.avgle.com/v1/videos/1'
proxy = 'socks5://127.0.0.1:1080'
html = WebPageDown.down_web_page_html(url, headers, proxy=None, retry=1)

print(html['html'].decode('utf-8'))













#!/usr/bin/env python
# import os
# import sqlite3
# import pwd

# _cookieName = "preferredLanguage"
#
# def getPreferredLanguageFromCookieDB():
#     retval="en-US"
#     cookieDBFilename = os.path.join(pwd.getpwuid(1000).pw_dir, ".config/google-chrome/Default/Cookies")
#     if os.path.isfile(cookieDBFilename):
#         connection = sqlite3.connect(cookieDBFilename)
#         querier = connection.cursor()
#         numCookiesMatching = int(querier.execute('SELECT COUNT(*) FROM cookies WHERE (host_key="127.0.0.1" or host_key="localhost") and name="%s"' % (_cookieName)).fetchone()[0])
#         if numCookiesMatching == 1:
#             retval = querier.execute('SELECT value FROM cookies WHERE (`cookies`.`host_key`="127.0.0.1" or `cookies`.`host_key`="localhost") and `cookies`.`name` = "%s"' % (_cookieName)).fetchone()[0]
#         elif numCookiesMatching == 0:
#             print("::getPreferredLanguageFromCookieDB > No cookie for '%s' found. Assuming wizard hasn't run yet, which is weird, but not critical" % (_cookieName))
#             retval="en-US"
#         else:
#             raise KeyError("Found %s cookies matching %s in file %s. This shouldn't have happened" % (numCookiesMatching, _cookieName, cookieDBFilename))
#             retval=None
#     else:
#         print("::getPreferredLanguageFromCookieDB > Cookie 'db' (actually, file) %s doesn't exist" % (cookieDBFilename))
#         retval="en-US"
#
#     return retval
#
#
# if __name__ == "__main__":
#     print "Prefered language: %s" % getPreferredLanguageFromCookieDB()