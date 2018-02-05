# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

# hupu 帖子相关信息
class HupuItem(scrapy.Item):
    # define the fields for your item here like:
    article_id = scrapy.Field()
    article_plate = scrapy.Field()
    title = scrapy.Field()
    author_name = scrapy.Field()
    author_id = scrapy.Field()
    post_time = scrapy.Field()
    comment_num = scrapy.Field()
    browse_num = scrapy.Field()

    article_content = scrapy.Field()
    all_images = scrapy.Field()
    article_post_time = scrapy.Field()
    highlights_re = scrapy.Field()
    uid = scrapy.Field()

# 高亮回复 相关信息
class CommentItem(scrapy.Item):
    comment_id = scrapy.Field()
    article_id = scrapy.Field()
    comment_username = scrapy.Field()
    comment_create_time = scrapy.Field()
    comment_uid = scrapy.Field()
    comment_content = scrapy.Field()
    highlights_num = scrapy.Field()
    article_post_time = scrapy.Field()





