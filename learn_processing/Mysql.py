#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pymysql


class MysqlConn:
    def __init__(self, host, port, user, passwd, db):
        self.conn = pymysql.Connect(host=host, port=port, user=user, passwd=passwd, db=db, charset='utf8')
        self.conn.autocommit(False)
        self.cursor = self.conn.cursor()

    def find_article(self, sql):
        try:
            self.cursor.execute(sql)
            self.conn.commit()
            return self.cursor.fetchall()
        except Exception as e:
            print("Reason:", e)
            self.conn.rollback()
        self.conn.close()

    # def __del__(self):
    #     # if self.cur:
    #     #    self.cur.close()
    #     if self.conn:
    #         self.conn.close()


# sqlInsert = "insert into wxb_title(title) values('title2')"
# sqlUpdate = "update user set username='name41' where userd='4'"
# sqlDelete = "delete from user where userid='1'"

