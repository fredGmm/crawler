# -*- coding: utf-8 -*-


from scrapy.conf import settings
import pymysql
from hupu.items import HupuItem
from hupu.items import CommentItem
from hupu.items import UserItem
from hupu.items import OtherItem
import time
import logging
import json
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
    #     # article_list = dict(item)
    #     # self.post.insert(article_list)
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

        if isinstance(item, HupuItem) and int(time.strftime('%H',time.localtime())) > 10 and int(time.strftime('%H',time.localtime()))< 19:
            # hupu_article_list sql语句等参数
            insert_sql = (
                "insert into hupu_article_list (article_id,article_title,artcile_author_uid,article_author_name,post_date,post_hour,comment_num,browse_num,plate,post_from) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) ")
            select_sql = ("select * from hupu_article_list where article_id = %s")
            update_sql = ("update hupu_article_list set comment_num=%s,browse_num=%s where article_id=%s")

            # artcile_info sql 语句
            article_info_insert_sql = (
                "insert into hupu_article_info (article_id,uid,article_content,images,highlights_re,comment_num,browse_num,post_time,create_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s) ")

            article_select_sql = ("select * from hupu_article_info where article_id = %s")
            artcile_update_sql = (
                "update hupu_article_info set comment_num=%s,browse_num=%s, highlights_re=%s where article_id=%s")

            # 插入新数据，更新等参数
            insert_param = [item['article_id'], item['title'], item['author_id'], item['author_name'],
                            item['post_time'],item['post_hour'],
                            item['comment_num'], item['browse_num'], item['article_plate'],item['post_from']]
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
            # try:
            #     select_ret = cur.execute(select_sql, select_param)
            #     if select_ret:
            #         cur.execute(update_sql, update_param)
            #     else:
            #         cur.execute(insert_sql, insert_param)
            #
            # except ValueError as e:
            #     print('mysql insert fail', e)
            #     conn.rollback()
            # else:
            #     conn.commit()
            # # hupu_article_info 数据处理
            # try:
            #     article_info_select_ret = cur.execute(article_select_sql, select_param)
            #
            #     if article_info_select_ret:
            #         cur.execute(artcile_update_sql, article_info_update_param)
            #     else:
            #         cur.execute(article_info_insert_sql, article_info_insert_param)
            # except ValueError as e:
            #     print('mysql insert fail', e)
            #     conn.rollback()
            # else:
            #     conn.commit()

            if item['all_images']:

                images = json.loads(item['all_images'])

                for img in images:

                    if 'jpg' not in img and img.find('jpeg') == -1 and img.find('png') == -1 and img.find('gif') == -1:
                        continue
                    origin_url = img
                    img = img[:img.find('?')]
                    print(img)
                    image_insert_sql = (
                    "insert into hupu_images (url,origin_url,article_id,hupu_user_id,plate,type,is_deleted,create_time,update_time) values (%s,%s, %s,%s,%s,%s,%s,%s,%s)")
                    image_select_sql = ("select * from hupu_images where url=%s and article_id=%s")
                    image_update_sql = ("update hupu_images set url = %s where id=%s")
                    image_select_param = [img, item['article_id']]
                    image_insert_param = [img, origin_url,item['article_id'], item['uid'], 'xxx', 1, 0, time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()), time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())]


                    # hupu_images 数据处理
                    try:
                        image_select_ret = cur.execute(image_select_sql, image_select_param)
                        print(image_select_ret)
                        if image_select_ret:
                            # image_update_param = [img, image_select_ret['']]
                            # cur.execute(artcile_update_sql, article_info_update_param)
                            print(image_select_ret)
                        else:
                            cur.execute(image_insert_sql, image_insert_param)
                    except ValueError as e:
                        print('mysql insert fail', e)
                        conn.rollback()
                    else:
                        conn.commit()

        elif isinstance(item, CommentItem) and 0:
            comment_insert_sql = (
                "insert into ace_comments (article_id,comment_id,comment_uid,comment_content,comment_username,comment_images,comment_create_time,highlights_num,create_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s) ")

            comment_is_exist_sql = ("select 1 from ace_comments where comment_id = %s")
            comment_update_sql = (
                "update ace_comments set is_edit=%s,highlights_num=%s where comment_id=%s")
            select_param = item['comment_id']
            comment_insert_param = [item['article_id'], item['comment_id'], item['comment_uid'],
                                    item['comment_content'], item['comment_username'],item['comment_images'],
                                    item['comment_create_time'], item['highlights_num'], time.time()]
            comment_update_param = [0, item['highlights_num'], item['comment_id']]
            # hupu_article_list 处理
            try:
                select_ret = cur.execute(comment_is_exist_sql, select_param)
                if select_ret:
                    cur.execute(comment_update_sql, comment_update_param)
                else:
                    cur.execute(comment_insert_sql, comment_insert_param)
            except ValueError as e:
                print('mysql insert fail', e)
                conn.rollback()
            else:
                conn.commit()
        elif isinstance(item, UserItem):
            user_info_insert_sql = ("insert into hupu_user (user_id,user_name,gender,bbs_reputation,bbs_level,associations,hupu_property,online_time,reg_time,last_login,self_introduction,favorite_sport,favorite_league,favorite_team,visit_num,follower_num,followering_num,topic_num,re_topic_num,collect_num,create_time) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)")
            user_info_is_exist_sql = ("select 1 from hupu_user where user_id = %s")
            user_info_update_sql = (
            "update hupu_user set user_name=%s, bbs_level=%s,online_time=%s,last_login=%s,visit_num=%s,follower_num=%s,followering_num=%s,topic_num=%s,re_topic_num=%s,collect_num=%s,create_time=%s where user_id = %s")

            user_insert_param = [item['user_id'],item['user_name'], item['gender'], item['bbs_reputation'], item['bbs_level'],
                                 item['associations'],
                                 item['hupu_property'], item['online_time'], item['reg_time'], item['last_login'],
                                 item['self_introduction'],
                                 item['favorite_sport'], item['favorite_league'], item['favorite_team'],
                                 item['visit_num'], item['follower_num'], item['followering_num'], item['topic_num'],
                                 item['re_topic_num'], item['collect_num'], time.time()]
            user_select_param = [item['user_id']]
            user_update_param = [item['user_name'], item['bbs_level'], item['online_time'], item['last_login'], item['visit_num'],
                                 item['follower_num'], item['followering_num'],
                                 item['topic_num'], item['re_topic_num'], item['collect_num'], time.time(), item['user_id']]
            # user_info 处理
            try:
                select_ret = cur.execute(user_info_is_exist_sql, user_select_param)
                if select_ret:
                    cur.execute(user_info_update_sql, user_update_param)
                else:
                    cur.execute(user_info_insert_sql, user_insert_param)
            except ValueError as e:
                print('mysql insert fail', e)
                logging.log(logging.ERROR, user_info_insert_sql + '--- error :' + str(e))
                conn.rollback()
            else:
                conn.commit()

        elif isinstance(item, OtherItem) and 0:
            print(item['bxj'],item['pgq'],item['shh'])
            for key, plate_data in item.items():
                post_num_insert_sql = (
                "insert into plate_post_num (plate,num,date,create_time) values (%s,%s,%s,%s)")
                post_num_is_exist_sql = ("select 1 from plate_post_num where plate = %s and date = %s")
                post_num_update_sql = (
                    "update plate_post_num set num=%s ,update_time=%s where plate = %s and date = %s")

                post_num_insert_param = [plate_data['plate'], plate_data['num'], plate_data['date'], time.time()]
                post_num_select_param = [plate_data['plate'],plate_data['date']]
                post_num_update_param = [plate_data['num'], time.time(), plate_data['plate'], plate_data['date']]
                #  处理
                try:
                    select_ret = cur.execute(post_num_is_exist_sql, post_num_select_param)
                    if select_ret:
                        cur.execute(post_num_update_sql, post_num_update_param)
                    else:
                        cur.execute(post_num_insert_sql, post_num_insert_param)
                except ValueError as e:
                    print('mysql insert fail', e)
                    logging.log(logging.ERROR, post_num_insert_sql + '--- error :' + str(e))
                    conn.rollback()
                else:
                    conn.commit()

        conn.close()
        cur.close()
        return item