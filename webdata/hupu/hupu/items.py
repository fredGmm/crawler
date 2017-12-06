# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HupuItem(scrapy.Item):
    # define the fields for your item here like:
    article_id = scrapy.Field()

    title = scrapy.Field()
    author_name = scrapy.Field()
    author_id = scrapy.Field()
    post_time = scrapy.Field()
    comment_num = scrapy.Field()
    browse_num = scrapy.Field()



