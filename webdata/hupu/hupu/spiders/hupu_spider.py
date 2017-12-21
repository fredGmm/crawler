# -*- coding: utf-8 -*-

import scrapy
from hupu.items import HupuItem
from scrapy.shell import inspect_response
from scrapy.http.request import Request
from scrapy.utils.project import get_project_settings
import json

class HupuSpider(scrapy.Spider):
    name = "hupu"
    allowed_domains = ["hupu.com"]
    cookie_str = 'PHPSESSID=nepe6b122jjla5hubir1gkcvg3; _dacevid3=06796c97.fd8f.79dc.efad.1bb101c56e65; __dacevid3=0xcdffaaaa291e1499; cn_2815e201bfe10o53c980_dplus=%7B%22distinct_id%22%3A%20%2215ec1a1eaf74d3-0843db83817eab-3f63450e-13c680-15ec1a1eaf855d%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201506487169%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201506487169%2C%22%24uid%22%3A%20%2206796c97.fd8f.79dc.efad.1bb101c56e65%22%2C%22%24recent_outside_referrer%22%3A%20%22%24direct%22%7D%2C%22initial_view_time%22%3A%20%221506486455%22%2C%22initial_referrer%22%3A%20%22%24direct%22%2C%22initial_referrer_domain%22%3A%20%22%24direct%22%7D; UM_distinctid=15ec1a1eaf74d3-0843db83817eab-3f63450e-13c680-15ec1a1eaf855d; _ga=GA1.2.185559595.1507696753; _HUPUSSOID=46d1e8aa-b464-490d-8ef4-624d5f0eef0f; shihuo-double11-views=11; AUM=dgTjQnLkKnbUF_zui89368LHjN5nt-yqlWtWpTno5j7lw; VUID=40A7E0B39DD44388A60B0F3DFA6511D8; CPLOGIN=39454880%7C1509048000000%7C0%7Cd0ad834836375a411367859ab137561e; CPLOGIN_INFO=%7B%22allname%22%3A%22%E8%99%9A%E6%8B%9F%E4%B9%8B%E5%AE%B6%22%2C%22agentId%22%3A%222334709%22%2C%22subname%22%3A%22%E8%99%9A%E6%8B%9F%E4%B9%8B%E5%AE%B6%22%2C%22memLevelImg%22%3A%220%22%2C%22isMigrated%22%3Afalse%2C%22hascertNo%22%3Afalse%2C%22isLocal%22%3Afalse%7D; vcid=3893f26813e71008d7a80b09c60fa373; NAGENTID=2334709; ipfrom=3aab6b6ec87397eca31f1dcd3bdcf58d%09Unknown; _CLT=918ebe7bb324d8673460f7af1d701a5c; u=18850874|6Jma5ouf5LmL5a62|533e|d032cf388bf469ee5cbbf1cc39f2309a|8bf469ee5cbbf1cc|6Jma5ouf5LmL5a62; us=f54317726dcbe3eb18d64771906131fc84313a2261cfd455180056533ff60a5c284880d95b975e2536655e44378b5a6c115249f1f6b11fbd92c85464634cb9aa; ua=20182165; Hm_lvt_39fc58a7ab8a311f2f6ca4dc1222a96e=1513661451,1513661742,1513661782,1513663182; Hm_lpvt_39fc58a7ab8a311f2f6ca4dc1222a96e=1513663182; lastvisit=25216%091513663220%09%2Fajax%2Fcard.php%3Fuid%3D22604354126996%26ulink%3Dhttps%253A%252F%252Fmy.hupu.com%252F22604354126996%26fid%3D34%26_%3D15136632153; _fmdata=EBF73F1CB6FEAEAD093036AC1F63F7EBF411CB6CF3B57C851F277B26FE3FD6765DAE2CCB7B583F6F0326CC573A3654DBD2C8330733272C55; __dacevst=5ff2d336.29896088|1513670072795; _cnzz_CV30020080=buzi_cookie%7C06796c97.fd8f.79dc.efad.1bb101c56e65%7C-1'

    cookie_dict = dict((line.split('=') for line in cookie_str.strip().split(";")))

    urls = []
    for page in range(1, 100):
        url = 'https://bbs.hupu.com/bxj'
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

        for sel in response.xpath('//div[@class="show-list"]/ul[@class="for-list"]/li'):
            item = HupuItem()
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

            # article_url = 'https://bbs.hupu.com/21003851.html'
            yield scrapy.Request(article_url, meta={'item': item}, callback=self.article_parse)


    def article_parse(self, response):
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

        item['highlights_re'] = 0 # 高亮回复
        item['article_post_time'] = '2017-12-21 10:51' # 文章详情页里面的 发帖时间
        yield item







