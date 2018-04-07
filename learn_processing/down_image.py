#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.request
import sys
import time
import json
import os
from multiprocessing import Process

from multiprocessing import Pool
# sys.path.append('/mnt/hgfs/python/scraping/learn_processing')
from Mysql import MysqlConn


def down_image(number):
    print('我是第:%s号启动的，进程ID是 %s' % (number, os.getpid()))

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'Accept-Encoding':'gzip, deflate',
        'Upgrade-Insecure-Requests': '1',
        # 'Cookie': '__gads=ID=2b1d2d4629e10087:T=1502422342:S=ALNI_MapJj4uFT0lKBxgxvDtj9L6AjSJeg; Hm_lvt_609cf0cb82b363063bcf56b050b31c06=1507796834; Hm_lpvt_609cf0cb82b363063bcf56b050b31c06=1507796834; UM_distinctid=15f0fe450055a9-0aacb9fd0a4a64-3e63430c-13c680-15f0fe45009577; CNZZDATA3980738=cnzz_eid%3D375819982-1507795998-null%26ntime%3D1507795998; CNZZDATA5299104=cnzz_eid%3D720537324-1508487488-null%26ntime%3D1508487488; AJSTAT_ok_times=1; CNZZDATA1254929547=202459006-1509005456-null%7C1509071800; Hm_lvt_444ece9ccd5b847838a56c93a0975a8b=1509008713,1509074912; Hm_lpvt_444ece9ccd5b847838a56c93a0975a8b=1509074912; CNZZDATA1259671153=1268634678-1511226188-https%253A%252F%252Fwww.baidu.com%252F%7C1511226188; Hm_lvt_1628f7c8d025473b441a8ba490edd441=1512439552; Hm_lpvt_1628f7c8d025473b441a8ba490edd441=1512439552; Hm_lvt_674430fbddd66a488580ec86aba288f7=1513132898,1513327292,1515145381; Hm_lpvt_674430fbddd66a488580ec86aba288f7=1515145381; CNZZDATA4343144=cnzz_eid%3D1379924068-1515145381-https%253A%252F%252Fwww.baidu.com%252F%26ntime%3D1515145381; CNZZDATA1260528602=830205212-1516873652-https%253A%252F%252Fwww.baidu.com%252F%7C1516873652; CNZZDATA1255738818=1995071737-1511861766-https%253A%252F%252Fwww.baidu.com%252F%7C1517381708; .CNBlogsCookie=7DC0E158877A3B3865D6D99E645D51E1D11BEF8934D86FB7FE0CC59A25794D09D739DFC03869EC2A86D72CBEE007B232227197C0483287817CDA55E064EA1CE3AB07A2494BB202502FF66E79672BBE0043007FBA; .Cnblogs.AspNetCore.Cookies=CfDJ8N7AeFYNSk1Put6Iydpme2YM5BXxs9Iw_G-2Z0oxgAomua6n29m8EgElmo-91D_2ROw8uiG3GRB08Wnf7oRomnCcgSKTaLeVrjmmYBe2oRQvRYF0sqak0m3kshjgcdZ8xpX38QK7GWaTB1G2EBWCX-i2NW_bSLqTcYlt-7hsvIJDA5VNVefTdhoNXdoKdvuXsUZvZaVzao_RacuoCTJe9730Y7Q-9AOMgkmTmMDkMxUqVXMzSDVN4l19fcrDOC7ZyH5wgHgoWE9akxoKpbv8i0QRnlDMVrVmM2axFdSX1Ki9; CNZZDATA1254486480=481500654-1519714184-https%253A%252F%252Fwww.baidu.com%252F%7C1519714184; uaid=ef7b9981e897d4ca720fa7770adadd7e; CNZZDATA5646633=cnzz_eid%3D1257097878-1519975944-https%253A%252F%252Fwww.baidu.com%252F%26ntime%3D1519975944; Hm_lvt_5f2c57e3e6679dd27bb04237bdadde15=1520214030; Hm_lpvt_5f2c57e3e6679dd27bb04237bdadde15=1520214030; _gat=1; _ga=GA1.2.37373735.1501748284; _gid=GA1.2.2052215384.1520212099', # 关键点啊，特么在cookie里埋标识
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
    }
    rows_num = '0'

    with open('rows_num.txt', "w") as f:
        f.write(rows_num+'\r')

    db_conn = MysqlConn(host='45.78.48.4', port=3306, user='root', passwd='ming1234~', db='web_data')
    sql = "select id,article_id,images from hupu_article_info where images != '[]' order by id limit 0,1"

    try:
        db_conn.cursor.execute(sql)
        result = db_conn.cursor.fetchall()
        print(result)
        db_conn.conn.close()
        db_conn.cursor.close()
        if result[0][0] > 1000000000:
            print('算了算了')
            exit()
        with open('rows_num.txt', "w") as f:
            f.write(str(result[len(result) - 1][0]))

        for article in list(result):
            # images = article[2].strip('[ ]').split(',')
            image_list = json.loads(article[2])  # 图片列表
            for image in image_list:
                url = image

                if 'jpg' in url or url.find('jpeg') > -1 or url.find('png') > -1:
                    # url = url.strip('" "')
                    # url = "https://t12.baidu.com/it/u=2388568829,148893518&fm=173&s=01725C908A5108C81A07A8C3030070AB&w=640&h=1580&img.JPEG"
                    url = "http://shihuo.hupucdn.com/price/201801/2611/f5ab1a2169d474880d5828c7177c9d50.jpg"
                    # url = "https://i10.hoopchina.com.cn/hupuapp/bbs/854/71064499034854/thread_71064499034854_20180131020728_s_163310_h_1334px_w_750px1373773358.jpeg?x-oss-process=image/resize,w_800/format,webp"

                    if '?' in url:  # 有些是手机适配图片，如上面的链接
                        url = url[:url.find('?')]
                    print(url)
                    try:
                        request = urllib.request.Request(url, headers=headers)
                        handler = urllib.request.HTTPCookieProcessor()
                        opener = urllib.request.build_opener(handler)
                        response = opener.open(request)
                    except Exception as e:
                        print("出错了", e)
                        print("该链接:", url, 'id:', article[0])
                        continue

                    if response.code == 200:
                        image_name = str(article[0]) + '_' + str(article[1]) + '_' + str(int(time.time())) + '.jpg'
                        with open('../static/images/' + image_name, "wb") as code:
                            code.write(response.read())

    except ValueError as e:
        print('mysql insert fail', e)
        db_conn.rollback()
    else:
        db_conn.commit()


if __name__ == '__main__':
    print('cpu数目：%s' % os.cpu_count())
    print('父进程 %s' % os.getpid())

    p = Pool(4)
    for i in range(4):
        # db_conn = MysqlConn(host='45.78.48.4', port=3306, user='root', passwd='ming1234~', db='web_data')
        p.apply_async(down_image, args=(i,))

    print('等所有的进程跑完吧')
    p.close()
    p.join()
    print('end')
