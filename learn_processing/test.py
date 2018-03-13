#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

sys.path.append('/mnt/hgfs/python/scraping')
# sys.path.append('D:\code\python\scraping')
from WebPageDownClass import WebPageDown


# cookie = 'PHPSESSID=nepe6b122jjla5hubir1gkcvg3; _dacevid3=06796c97.fd8f.79dc.efad.1bb101c56e65; __dacevid3=0xcdffaaaa291e1499; cn_2815e201bfe10o53c980_dplus=%7B%22distinct_id%22%3A%20%2215ec1a1eaf74d3-0843db83817eab-3f63450e-13c680-15ec1a1eaf855d%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201506487169%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201506487169%2C%22%24uid%22%3A%20%2206796c97.fd8f.79dc.efad.1bb101c56e65%22%2C%22%24recent_outside_referrer%22%3A%20%22%24direct%22%7D%2C%22initial_view_time%22%3A%20%221506486455%22%2C%22initial_referrer%22%3A%20%22%24direct%22%2C%22initial_referrer_domain%22%3A%20%22%24direct%22%7D; UM_distinctid=15ec1a1eaf74d3-0843db83817eab-3f63450e-13c680-15ec1a1eaf855d; _ga=GA1.2.185559595.1507696753; _HUPUSSOID=46d1e8aa-b464-490d-8ef4-624d5f0eef0f; shihuo-double11-views=11; AUM=dgTjQnLkKnbUF_zui89368LHjN5nt-yqlWtWpTno5j7lw; VUID=40A7E0B39DD44388A60B0F3DFA6511D8; CPLOGIN=39454880%7C1509048000000%7C0%7Cd0ad834836375a411367859ab137561e; CPLOGIN_INFO=%7B%22allname%22%3A%22%E8%99%9A%E6%8B%9F%E4%B9%8B%E5%AE%B6%22%2C%22agentId%22%3A%222334709%22%2C%22subname%22%3A%22%E8%99%9A%E6%8B%9F%E4%B9%8B%E5%AE%B6%22%2C%22memLevelImg%22%3A%220%22%2C%22isMigrated%22%3Afalse%2C%22hascertNo%22%3Afalse%2C%22isLocal%22%3Afalse%7D; vcid=3893f26813e71008d7a80b09c60fa373; NAGENTID=2334709; ipfrom=3aab6b6ec87397eca31f1dcd3bdcf58d%09Unknown; _CLT=918ebe7bb324d8673460f7af1d701a5c; u=18850874|6Jma5ouf5LmL5a62|533e|d032cf388bf469ee5cbbf1cc39f2309a|8bf469ee5cbbf1cc|6Jma5ouf5LmL5a62; us=f54317726dcbe3eb18d64771906131fc84313a2261cfd455180056533ff60a5c284880d95b975e2536655e44378b5a6c115249f1f6b11fbd92c85464634cb9aa; ua=20182165; Hm_lvt_39fc58a7ab8a311f2f6ca4dc1222a96e=1513661451,1513661742,1513661782,1513663182; Hm_lpvt_39fc58a7ab8a311f2f6ca4dc1222a96e=1513663182; lastvisit=25216%091513663220%09%2Fajax%2Fcard.php%3Fuid%3D22604354126996%26ulink%3Dhttps%253A%252F%252Fmy.hupu.com%252F22604354126996%26fid%3D34%26_%3D15136632153; _fmdata=EBF73F1CB6FEAEAD093036AC1F63F7EBF411CB6CF3B57C851F277B26FE3FD6765DAE2CCB7B583F6F0326CC573A3654DBD2C8330733272C55; __dacevst=5ff2d336.29896088|1513670072795; _cnzz_CV30020080=buzi_cookie%7C06796c97.fd8f.79dc.efad.1bb101c56e65%7C-1'
# # cookie = 'currency=USD;country=UY;cousntry=UY;countfry=UY;countery=UY;countrry=UY;countrsy=UY;coeuntry=UY'
# # cookie = cookie.replace(' ','')
#
# cookie_dict = dict((line.split('=') for line in cookie.strip().split(";")))
# print(cookie_dict)
# exit(0)
# headers = {
#    # 'accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
#    # 'accept-language' : 'zh-CN,zh;q=0.9',
#    'user-agent' : 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
#    'cookies': 'SID=AAUWq91AyVEBDtiXnXTCzGds4bO4YibY2CdH-KosGgeWMRP3kHVdYUsuZ9v5ZGD-AOZ3sw.; HSID=Ak_Ob66zroGWGfOg7; SSID=Aytj7SyqvXB-xFPeU; APISID=zChe30jo0cpSIT4I/A-B6vtmKKFyiZNGqo; SAPISID=9d8-cPD1XdDvqWOO/AblqcREh7NX_IGpv0; NID=119=OXcQlLJTagB3pcyI-6pubPweZSJbcJoG2XVdG0Jq3Dw2knuhICSVdP0UOv5nCjoGD0jWPK76Y73gvi1BXuvtEyoKd6v4R173tt2F0suWZAD78qZ3M_qTO6F4UfK76tXjFDZ3nKGFJuR8ISZdRkceQg2N0OYT-9UdrLHClvLTr6Sn_qpEDV1Gfg88u21v8q4bYQwhJ9SskhpQQKQ; 1P_JAR=2017-12-18-6; SIDCC=AE4kn79jNPO_GtUFE2U_KiFvhruYiU8ZlSHzFQk4KBqSQEvmWzkyWmqPtSfsrac93-sSQvu2ejvoFdjQUE5I',
# }
# url = 'https://api.avgle.com/v1/videos/1'
# proxy = 'socks5://127.0.0.1:1080'
# html = WebPageDown.down_web_page_html(url, headers, proxy=None, retry=1)
#
# print(html['html'].decode('utf-8'))


import urllib.request
url = "https://i10.hoopchina.com.cn/hupuapp/bbs/854/71064499034854/thread_71064499034854_20180131020727_s_160656_h_1334px_w_750px1018260953.jpeg"
# url = "http://images.dev.dodoedu.com/attachments/1095a03bd140ab74.jpg"

headers = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    # 'Accept-Encoding':'gzip, deflate',
    'Upgrade-Insecure-Requests': '1',
    # 'Cookie': '__gads=ID=2b1d2d4629e10087:T=1502422342:S=ALNI_MapJj4uFT0lKBxgxvDtj9L6AjSJeg; Hm_lvt_609cf0cb82b363063bcf56b050b31c06=1507796834; Hm_lpvt_609cf0cb82b363063bcf56b050b31c06=1507796834; UM_distinctid=15f0fe450055a9-0aacb9fd0a4a64-3e63430c-13c680-15f0fe45009577; CNZZDATA3980738=cnzz_eid%3D375819982-1507795998-null%26ntime%3D1507795998; CNZZDATA5299104=cnzz_eid%3D720537324-1508487488-null%26ntime%3D1508487488; AJSTAT_ok_times=1; CNZZDATA1254929547=202459006-1509005456-null%7C1509071800; Hm_lvt_444ece9ccd5b847838a56c93a0975a8b=1509008713,1509074912; Hm_lpvt_444ece9ccd5b847838a56c93a0975a8b=1509074912; CNZZDATA1259671153=1268634678-1511226188-https%253A%252F%252Fwww.baidu.com%252F%7C1511226188; Hm_lvt_1628f7c8d025473b441a8ba490edd441=1512439552; Hm_lpvt_1628f7c8d025473b441a8ba490edd441=1512439552; Hm_lvt_674430fbddd66a488580ec86aba288f7=1513132898,1513327292,1515145381; Hm_lpvt_674430fbddd66a488580ec86aba288f7=1515145381; CNZZDATA4343144=cnzz_eid%3D1379924068-1515145381-https%253A%252F%252Fwww.baidu.com%252F%26ntime%3D1515145381; CNZZDATA1260528602=830205212-1516873652-https%253A%252F%252Fwww.baidu.com%252F%7C1516873652; CNZZDATA1255738818=1995071737-1511861766-https%253A%252F%252Fwww.baidu.com%252F%7C1517381708; .CNBlogsCookie=7DC0E158877A3B3865D6D99E645D51E1D11BEF8934D86FB7FE0CC59A25794D09D739DFC03869EC2A86D72CBEE007B232227197C0483287817CDA55E064EA1CE3AB07A2494BB202502FF66E79672BBE0043007FBA; .Cnblogs.AspNetCore.Cookies=CfDJ8N7AeFYNSk1Put6Iydpme2YM5BXxs9Iw_G-2Z0oxgAomua6n29m8EgElmo-91D_2ROw8uiG3GRB08Wnf7oRomnCcgSKTaLeVrjmmYBe2oRQvRYF0sqak0m3kshjgcdZ8xpX38QK7GWaTB1G2EBWCX-i2NW_bSLqTcYlt-7hsvIJDA5VNVefTdhoNXdoKdvuXsUZvZaVzao_RacuoCTJe9730Y7Q-9AOMgkmTmMDkMxUqVXMzSDVN4l19fcrDOC7ZyH5wgHgoWE9akxoKpbv8i0QRnlDMVrVmM2axFdSX1Ki9; CNZZDATA1254486480=481500654-1519714184-https%253A%252F%252Fwww.baidu.com%252F%7C1519714184; uaid=ef7b9981e897d4ca720fa7770adadd7e; CNZZDATA5646633=cnzz_eid%3D1257097878-1519975944-https%253A%252F%252Fwww.baidu.com%252F%26ntime%3D1519975944; Hm_lvt_5f2c57e3e6679dd27bb04237bdadde15=1520214030; Hm_lpvt_5f2c57e3e6679dd27bb04237bdadde15=1520214030; _gat=1; _ga=GA1.2.37373735.1501748284; _gid=GA1.2.2052215384.1520212099', # 关键点啊，特么在cookie里埋标识
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
}
request = urllib.request.Request(url, headers=headers)
handler = urllib.request.HTTPCookieProcessor()
opener = urllib.request.build_opener(handler)


response = opener.open(request)


# f = urllib.request.urlopen(url)
with open("weixin4324.png", "wb") as code:
  code.write(response.read())















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