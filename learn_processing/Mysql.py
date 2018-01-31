#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pymysql

conn = pymysql.Connect(host='192.168.1.111', port=3306, user='root', passwd='xiaoming', db='web_arashi', charset='utf8')
conn.autocommit(False)
cursor = conn.cursor()

sqlInsert = "insert into wxb_title(title) values('title2')"
sqlUpdate = "update user set username='name41' where userd='4'"
sqlDelete = "delete from user where userid='1'"
try:
    cursor.execute(sqlInsert)
    print(cursor.rowcount)
    # cursor.execute(sqlUpdate)
    # print(cursor.rowcount)
    # cursor.execute(sqlDelete)
    # print(cursor.rowcount)

    conn.commit()
except Exception as e:
    print("Reason:", e)
    conn.rollback()

cursor.close()
