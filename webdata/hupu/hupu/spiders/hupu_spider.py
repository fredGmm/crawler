# -*- coding: utf-8 -*-

import scrapy
from hupu.items import HupuItem
from hupu.items import CommentItem
from scrapy.shell import inspect_response
from scrapy.http.request import Request
from scrapy.utils.project import get_project_settings
import json
import re
class HupuSpider(scrapy.Spider):
    name = "hupu"
    allowed_domains = ["hupu.com"]
    # 去掉 __gads=ID=d140a94144ba1993:T=1505436772:S=ALNI_MaNd80C0poIVcASdbf8orkORfg6_w;
    cookie_str = 'PHPSESSID=nepe6b122jjla5hubir1gkcvg3; _dacevid3=06796c97.fd8f.79dc.efad.1bb101c56e65;  __dacevid3=0xcdffaaaa291e1499; cn_2815e201bfe10o53c980_dplus=%7B%22distinct_id%22%3A%20%2215ec1a1eaf74d3-0843db83817eab-3f63450e-13c680-15ec1a1eaf855d%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201506487169%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201506487169%2C%22%24uid%22%3A%20%2206796c97.fd8f.79dc.efad.1bb101c56e65%22%2C%22%24recent_outside_referrer%22%3A%20%22%24direct%22%7D%2C%22initial_view_time%22%3A%20%221506486455%22%2C%22initial_referrer%22%3A%20%22%24direct%22%2C%22initial_referrer_domain%22%3A%20%22%24direct%22%7D; UM_distinctid=15ec1a1eaf74d3-0843db83817eab-3f63450e-13c680-15ec1a1eaf855d; _ga=GA1.2.185559595.1507696753; _HUPUSSOID=46d1e8aa-b464-490d-8ef4-624d5f0eef0f; shihuo-double11-views=11; AUM=dgTjQnLkKnbUF_zui89368LHjN5nt-yqlWtWpTno5j7lw; VUID=40A7E0B39DD44388A60B0F3DFA6511D8; CPLOGIN=39454880%7C1509048000000%7C0%7Cd0ad834836375a411367859ab137561e; CPLOGIN_INFO=%7B%22allname%22%3A%22%E8%99%9A%E6%8B%9F%E4%B9%8B%E5%AE%B6%22%2C%22agentId%22%3A%222334709%22%2C%22subname%22%3A%22%E8%99%9A%E6%8B%9F%E4%B9%8B%E5%AE%B6%22%2C%22memLevelImg%22%3A%220%22%2C%22isMigrated%22%3Afalse%2C%22hascertNo%22%3Afalse%2C%22isLocal%22%3Afalse%7D; vcid=3893f26813e71008d7a80b09c60fa373; NAGENTID=2334709; ipfrom=3aab6b6ec87397eca31f1dcd3bdcf58d%09Unknown; _CLT=918ebe7bb324d8673460f7af1d701a5c; u=18850874|6Jma5ouf5LmL5a62|533e|d032cf388bf469ee5cbbf1cc39f2309a|8bf469ee5cbbf1cc|6Jma5ouf5LmL5a62; us=f54317726dcbe3eb18d64771906131fc84313a2261cfd455180056533ff60a5c284880d95b975e2536655e44378b5a6c115249f1f6b11fbd92c85464634cb9aa; lastvisit=27096%091513905571%09%2Fajax%2Fcard.php%3Fuid%3D165402480851831%26ulink%3Dhttps%253A%252F%252Fmy.hupu.com%252F165402480851831%26fid%3D3441%26_%3D1513905; ua=20185713; __dacevst=8c87e67f.84074b9e|1513932718779; _cnzz_CV30020080=buzi_cookie%7C06796c97.fd8f.79dc.efad.1bb101c56e65%7C-1; Hm_lvt_39fc58a7ab8a311f2f6ca4dc1222a96e=1513921677,1513921679,1513921688,1513921695; Hm_lpvt_39fc58a7ab8a311f2f6ca4dc1222a96e=1513930919; _fmdata=EBF73F1CB6FEAEAD093036AC1F63F7EBF411CB6CF3B57C851F277B26FE3FD6765DAE2CCB7B583F6F0326CC573A3654DBD2C8330733272C55'
    cookie_dict = dict((line.split('=') for line in cookie_str.strip().split(";")))

    urls = []
    for page in range(1, 6):
        url = 'https://bbs.hupu.com/bxj-1'
        if page > 1:
            url = url + '-' + str(page)
        urls.append(url)

    for page in range(1, 6):
        url = 'https://bbs.hupu.com/lol-1'
        if page > 1:
            url = url + '-' + str(page)
        urls.append(url)

    start_urls = urls
    # start_urls = [
    #     'https://bbs.hupu.com/bxj-99'
    # ]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, cookies=self.cookie_dict)

    def parse(self, response):
        # inspect_response(response, self)
        response_url = response.url

        # 匹配它是属于 bxj（步行街） 还是 vote（湿乎乎） 还是 lol（英雄联盟）
        re_res = re.findall(r'bbs.hupu.com/(\w+){0,4}-?\d*', response_url)
        article_plate = re_res[0] if len(re_res) > 0 else 'bxj'

        for sel in response.xpath('//div[@class="show-list"]/ul[@class="for-list"]/li'):
            item = HupuItem()
            item['article_plate'] = article_plate
            # print(sel.xpath('.//div[@class="titlelink box"]/a[contains(@href, "html")/@href').re(r'/(d+)\.html'))
            article_id = sel.xpath('.//div[@class="titlelink box"]/a[contains(@href, "html")]/@href').re(r'/(\d+)\.html')

            item['article_id'] = article_id[0] if len(article_id) > 0 else 0

            # data.xpath('string(.)') 优化
            title = sel.xpath('.//div[@class="titlelink box"]/a').xpath('string(.)').extract()
            item['title'] = title[0] if len(title) > 0 else ''

            # if title:
            #     item['title'] = title
            # else:
            #     item['title'] = sel.xpath('.//div[@class="titlelink box"]/a/b/text()').extract()

            author_name = sel.xpath('.//div[@class="author box"]/a/text()').extract()
            item['author_name'] = author_name[0] if len(author_name) else ''

            author_id = sel.xpath('.//div[@class="author box"]/a[contains(@href, "hupu.com")]/@href').re(r'.*/(\d+)$')
            item['author_id'] = author_id[0] if len(author_id) > 0 else 0

            post_time = sel.xpath('.//div[@class="author box"]/a[contains(@style, "color")]/text()').extract()
            item['post_time'] = post_time[0] if len(post_time) > 0 else 0

            comment_num = sel.xpath('.//span[@class="ansour box"]/text()').re(r'^(\d{1,15})\s/\s.*$')
            browse_num = sel.xpath('.//span[@class="ansour box"]/text()').re(r'^.*\s/\s(\d{1,15})$')
            item['comment_num'] = comment_num[0] if comment_num else 0
            item['browse_num'] = browse_num[0] if browse_num else 0
            # yield item

        # for sel in response.xpath('//div[@class="show-list"]/ul[@class="for-list"]/li'):
        #     article_id = sel.xpath('.//div[@class="titlelink box"]/a[contains(@href, "html")]/@href').re(
        #         r'/(\d+)\.html')

            article_url = 'https://bbs.hupu.com/' + article_id[0] + '.html'

            # article_url = 'https://bbs.hupu.com/21016783.html'
            yield scrapy.Request(article_url, meta={'item': item}, callback=self.article_parse)

    # 抓取 帖子下面的亮贴，神回复怎能错过-。-
    def article_parse(self, response):
        comment_item = CommentItem() # 高亮回复
        item = response.meta['item']
        # inspect_response(response, self)
        title = response.xpath('//div[@class="bbs-hd-h1"]/h1/text()').extract()
        item['uid'] = item['author_id']
        content = response.xpath('//div[@class="floor-show"]/div[@class="floor_box"]/table/tbody/tr/td/div[@class="quote-content"]').xpath('string(.)').extract()
        item['article_content'] = content[0] if content else 0
        images = response.xpath('//div[@class="floor-show"]/div[@class="floor_box"]/table/tbody/tr/td/div[@class="quote-content"]').xpath('.//a/@href').extract()

        images2 = response.xpath('//div[@class="floor-show"]/div[@class="floor_box"]/table/tbody/tr/td/div[@class="quote-content"]').xpath('.//img/@src').extract()

        all_img = images + images2
        item['all_images'] = json.dumps(all_img)

        highlights_re = response.xpath('//div[@class="w_reply clearfix"]/div[@id="readfloor"]/div[@class="floor"]/@id').extract() # 高亮回复id
        if item:
            for comment_id in highlights_re:
                # user_url = response.xpath('//div[@id=47406]/div[@class="floor_box"]/div[@class="author"]/div[@class="left"]/a/@href').extract_first()
                comment_item['article_id'] = item['article_id']
                comment_item['comment_id'] = comment_id
                comment_item['comment_username'] = response.xpath(
                    '//div[@id=$val]/div[@class="floor_box"]/div[@class="author"]/div[@class="left"]/a/text()', val=comment_id).extract_first()

                comment_item['comment_create_time'] = response.xpath(
                    '//div[@id=$val]/div[@class="floor_box"]/div[@class="author"]/div[@class="left"]/span[@class="stime"]/text()', val=comment_id).extract_first()

                comment_item['comment_uid'] = response.xpath(
                    '//div[@id=$val]/div[@class="floor_box"]/div[@class="author"]/div[@class="left"]/span/@uid', val=comment_id).extract_first()

                comment_item['comment_content'] = response.xpath('//div[@id=$val]/div[@class="floor_box"]/table/tbody/tr/td/text()', val=comment_id).extract_first()
                if len(comment_item['comment_content']) < 3:
                    comment_item['comment_content'] = response.xpath('//div[@id=$val]/div[@class="floor_box"]/table/tbody/tr/td', val=comment_id).xpath('string(.)').extract_first()

                comment_item['highlights_num'] = response.xpath('//div[@id=$val]/div[@class="floor_box"]/div[@class="author"]/div[@class="left"]/span/span//span/text()',val=comment_id).extract_first()
                yield comment_item
        item['highlights_re'] = ','.join(highlights_re)
        artcile_post_time = response.xpath('//div[@class="floor-show"]/div[@class="floor_box"]/div[@class="author"]//div[@class="left"]/span[@class="stime"]/text()').extract()
        item['article_post_time'] = artcile_post_time[0] if artcile_post_time else ''  # 文章详情页里面的 发帖时间
        yield item







