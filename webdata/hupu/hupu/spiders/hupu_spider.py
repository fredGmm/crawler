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
           # item = HupuItem()
           # item['title'] = sel.css('.titlelink.box a::text').extract()
           # item['num'] = sel.xpath('span[@class=ansour box]/text()').extract()

           title = sel.xpath('div[@class="titlelink box"]/a').extract()
           # num = sel.xpath('span[@class=ansour box]/text()').extract()
           print(title)
           # yield item

