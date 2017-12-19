# -*- coding: utf-8 -*-

import scrapy
from hupu.items import HupuItem
from scrapy.shell import inspect_response
from scrapy.http.request import Request

class HupuSpider(scrapy.Spider):
    name = "hupu"
    allowed_domains = ["hupu.com"]
    header_cookies = {

    }
    # urls = []
    # for page in range(19, 100):
    #     url = 'https://bbs.hupu.com/bxj'
    #     if page > 1:
    #         url = url + '-' + str(page)
    #     urls.append(url)
    # start_urls = urls
    start_urls = [
        'https://bbs.hupu.com/bxj'
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, cookies={'fda': 'true'})

    def parse(self, response):
        inspect_response(response, self)
        # exit(0)
        # for sel in response.xpath('//div[@class="show-list"]/ul[@class="for-list"]/li'):
        #     item = HupuItem()
        #     # print(sel.xpath('.//div[@class="titlelink box"]/a[contains(@href, "html")/@href').re(r'/(d+)\.html'))
        #     article_id = sel.xpath('.//div[@class="titlelink box"]/a[contains(@href, "html")]/@href').re(r'/(\d+)\.html')
        #
        #     item['article_id'] = article_id[0] if len(article_id) > 0 else 0
        #
        #     # data.xpath('string(.)') 优化
        #     title = sel.xpath('.//div[@class="titlelink box"]/a').xpath('string(.)').extract()
        #     item['title'] = title[0] if len(title) > 0 else ''
        #
        #     # if title:
        #     #     item['title'] = title
        #     # else:
        #     #     item['title'] = sel.xpath('.//div[@class="titlelink box"]/a/b/text()').extract()
        #
        #     author_name = sel.xpath('.//div[@class="author box"]/a/text()').extract()
        #     item['author_name'] = author_name[0] if len(author_name) else ''
        #
        #     author_id = sel.xpath('.//div[@class="author box"]/a[contains(@href, "hupu.com")]/@href').re(r'.*/(\d+)$')
        #     item['author_id'] = author_id[0] if len(author_id) > 0 else 0
        #
        #     post_time = sel.xpath('.//div[@class="author box"]/a[contains(@style, "color")]/text()').extract()
        #     item['post_time'] = post_time[0] if len(post_time) > 0 else 0
        #
        #     comment_num = sel.xpath('.//span[@class="ansour box"]/text()').re(r'^(\d{1,15})\s/\s.*$')
        #     browse_num = sel.xpath('.//span[@class="ansour box"]/text()').re(r'^.*\s/\s(\d{1,15})$')
        #     item['comment_num'] = comment_num[0] if comment_num else 0
        #     item['browse_num'] = browse_num[0] if browse_num else 0
        #     yield item
            # num = sel.xpath('span[@class=ansour box]/text()').extract()
