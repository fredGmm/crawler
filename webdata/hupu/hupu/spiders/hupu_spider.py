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
            # print(sel.xpath('.//div[@class="titlelink box"]/a[contains(@href, "html")/@href').re(r'/(d+)\.html'))
            item['article_id'] = sel.xpath('.//div[@class="titlelink box"]/a[contains(@href, "html")]/@href').re(r'/(\d+)\.html')

            # data.xpath('string(.)') 优化
            item['title'] = sel.xpath('.//div[@class="titlelink box"]/a').xpath('string(.)').extract()

            # if title:
            #     item['title'] = title
            # else:
            #     item['title'] = sel.xpath('.//div[@class="titlelink box"]/a/b/text()').extract()

            item['author_name'] = sel.xpath('.//div[@class="author box"]/a/text()').extract()

            item['author_id'] = sel.xpath('.//div[@class="author box"]/a[contains(@href, "hupu.com")]/@href').re(r'.*/(\d+)$')

            item['post_time'] = sel.xpath('.//div[@class="author box"]/a[contains(@style, "color")]/text()').extract()

            comment_num = sel.xpath('.//span[@class="ansour box"]/text()').re(r'^(\d{1,15})\s/\s.*$')
            browse_num = sel.xpath('.//span[@class="ansour box"]/text()').re(r'^.*\s/\s(\d{1,15})$')
            item['comment_num'] = comment_num[0] if comment_num else 0
            item['browse_num'] = browse_num[0] if browse_num else 0
            yield item
            # num = sel.xpath('span[@class=ansour box]/text()').extract()
