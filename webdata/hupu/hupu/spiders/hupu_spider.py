# -*- coding: utf-8 -*-

import scrapy
from hupu.items import HupuItem

class HupuSpider(scrapy.Spider):
    name = "hupu"
    allowed_domains = ["hupu.com"]
    start_urls = [
        "https://bbs.hupu.com/bxj",
    ]

    def parse(self, response):


        for sel in response.xpath('//div[@class="show-list"]/ul[@class="for-list"]/li'):
            item = HupuItem()
            item['article_id'] = sel.xpath('.//div[@class="titlelink box"]/a[contains(@href, "html")/@href').re(
                r'/(d+)\.html')
            title = sel.xpath('.//div[@class="titlelink box"]/a/text()').extract()
            # data.xpath('string(.)') 优化
            if title:
                item['title'] = title
            else:
                item['title'] = sel.xpath('.//div[@class="titlelink box"]/a/b/text()').extract()

            item['author_name'] = sel.xpath(
                './/div[@class="show-list"]/ul[@class="for-list"]/li/div[@class="author box"]/a/text()').extract()

            item['author_id'] = sel.xpath(
                '//div[@class="show-list"]/ul[@class="for-list"]/li/div[@class="author box"]/a[contains(@href, "hupu.com")]/@href').re(
                r'.*/(\d+)$')

            item['post_time'] = sel.xpath(
                '//div[@class="show-list"]/ul[@class="for-list"]/li/div[@class="author box"]/a[contains(@style, "color")]/text()').extract()

            item['comment_num'] = \
            sel.xpath('//div[@class="show-list"]/ul[@class="for-list"]/li/span[@class="ansour box"]/text()').re(
                r'^.*(\d{0,10})')
            yield item
            # num = sel.xpath('span[@class=ansour box]/text()').extract()


