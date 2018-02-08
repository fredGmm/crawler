#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import pymysql
import pymysql.cursors

#获取一个数据库连接，注意如果是UTF-8类型的，需要制定数据库
conn=pymysql.connect(host='45.78.48.4',user='root',passwd='ming1234~',db='web_arashi',port=3306,charset='utf8',cursorclass=pymysql.cursors.DictCursor)
cur=conn.cursor()#获取一个游标
select_ret = cur.execute('select food_name from food_choose where 1 =0')
data=cur.fetchall()
if not select_ret:
    print(select_ret, 'not')
print(select_ret,data)
exit(0)
for d in data :
    #注意int类型需要使用str函数转义
    print("ID: "+str(d[0])+'  用户名： '+d[1]+"  注册时间： "+d[2])
cur.close()#关闭游标
conn.close()#释放数据库资源