# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.conf import settings
import pymysql
from hupu.items import HupuItem
from hupu.items import CommentItem
import time
import pymongo


class HupuPipeline(object):
    # def process_item(self, item, spider):
    #     return item
    # def __init__(self):
    #     port = settings['MONGODB_PORT']
    #     host = settings['MONGODB_HOST']
    #     db_name = settings['MONGODB_DBNAME']
    #     client = pymongo.MongoClient(host=host, port=port)
    #     db = client[db_name]
    #     self.post = db[settings['MONGODB_DOCNAME']]
    #
    # def process_item(self, item, spider):
    #     article_list = dict(item)
    #     self.post.insert(article_list)
    #     return item

    def process_item(self, item, spider):
        host = settings['MYSQL_HOSTS']
        user = settings['MYSQL_USER']
        psd = settings['MYSQL_PASSWORD']
        db = settings['MYSQL_DB']
        c = settings['CHARSET']

        # 链接 数据库
        conn = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c)
        cur = conn.cursor()

        if isinstance(item, HupuItem):
            # hupu_article_list sql语句等参数
            insert_sql = (
                "insert into hupu_article_list (article_id,article_title,artcile_author_uid,article_author_name,post_date,comment_num,browse_num) values (%s,%s,%s,%s,%s,%s,%s) ")
            select_sql = ("select 1 from hupu_article_list where article_id = %s")
            update_sql = ("update hupu_article_list set comment_num=%s,browse_num=%s where article_id=%s")

            # artcile_info sql 语句
            article_info_insert_sql = (
                "insert into hupu_article_info (article_id,uid,article_content,images,highlights_re,comment_num,browse_num,post_time,create_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s) ")

            article_select_sql = ("select 1 from hupu_article_info where article_id = %s")
            artcile_update_sql = (
                "update hupu_article_info set comment_num=%s,browse_num=%s, highlights_re=%s where article_id=%s")

            # 插入新数据，更新等参数
            insert_param = [item['article_id'], item['title'], item['author_id'], item['author_name'],
                            item['post_time'],
                            item['comment_num'], item['browse_num']]
            update_param = [item['comment_num'], item['browse_num'], item['article_id']]
            select_param = item['article_id']

            # artcile_info 参数
            article_info_insert_param = [item['article_id'], item['uid'], item['article_content'], item['all_images'],
                                         item['highlights_re'],
                                         item['comment_num'], item['browse_num'], item['article_post_time'],
                                         time.time()]
            article_info_update_param = [item['comment_num'], item['browse_num'], item['highlights_re'],
                                         item['article_id']]

            # hupu_article_list 处理
            try:
                select_ret = cur.execute(select_sql, select_param)
                if select_ret:
                    cur.execute(update_sql, update_param)
                else:
                    cur.execute(insert_sql, insert_param)

            except ValueError as e:
                print('mysql insert fail', e)
                conn.rollback()
            else:
                conn.commit()
            # hupu_article_info 数据处理
            try:
                article_info_select_ret = cur.execute(article_select_sql, select_param)

                if article_info_select_ret:
                    cur.execute(artcile_update_sql, article_info_update_param)
                else:
                    cur.execute(article_info_insert_sql, article_info_insert_param)
            except ValueError as e:
                print('mysql insert fail', e)
                conn.rollback()
            else:
                conn.commit()


        elif isinstance(item, CommentItem):
            comment_insert_sql = (
                "insert into highlights_re_info (article_id,comment_id,comment_uid,comment_content,comment_username,comment_create_time,highlights_num,create_time) values (%s,%s,%s,%s,%s,%s,%s,%s) ")

            comment_is_exist_sql = ("select 1 from highlights_re_info where comment_id = %s")
            comment_update_sql = (
                "update highlights_re_info set is_edit=%s,highlights_num=%s where comment_id=%s")
            select_param = item['comment_id']
            comment_insert_param = [item['article_id'], item['comment_id'], item['comment_uid'],
                                    item['comment_content'], item['comment_username'],
                                    item['comment_create_time'], item['highlights_num'], time.time()]
            comment_update_param = [0, item['highlights_num'], item['comment_id']]
            # hupu_article_list 处理
            try:
                select_ret = cur.execute(comment_is_exist_sql, select_param)
                if select_ret:
                    cur.execute(comment_update_sql, comment_update_param)
                cur.execute(comment_insert_sql, comment_insert_param)
            except ValueError as e:
                print('mysql insert fail', e)
                conn.rollback()
            else:
                conn.commit()

        conn.close()
        cur.close()
        return item
        # class CommentPipeline(object):
        #     def process_item(self, item, spider):
        #         host = settings['MYSQL_HOSTS']
        #         user = settings['MYSQL_USER']
        #         psd = settings['MYSQL_PASSWORD']
        #         db = settings['MYSQL_DB']
        #         c = settings['CHARSET']
        #
        #         # 链接 数据库
        #         conn = pymysql.connect(host=host, user=user, passwd=psd, db=db, charset=c)
        #         cur = conn.cursor()
        #
        #
        #         return item
