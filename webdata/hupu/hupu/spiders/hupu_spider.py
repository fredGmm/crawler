# -*- coding: utf-8 -*-

import scrapy
from hupu.items import HupuItem
from hupu.items import CommentItem
from hupu.items import UserItem
from scrapy.shell import inspect_response
from scrapy.http.request import Request
from scrapy.utils.project import get_project_settings
import json
import re
import logging
import time


class HupuSpider(scrapy.Spider):
    name = "hupu"
    allowed_domains = ["hupu.com"]
    # 去掉 __gads=ID=d140a94144ba1993:T=1505436772:S=ALNI_MaNd80C0poIVcASdbf8orkORfg6_w;
    cookie_str = 'PHPSESSID=nepe6b122jjla5hubir1gkcvg3; _dacevid3=06796c97.fd8f.79dc.efad.1bb101c56e65;  __dacevid3=0xcdffaaaa291e1499; cn_2815e201bfe10o53c980_dplus=%7B%22distinct_id%22%3A%20%2215ec1a1eaf74d3-0843db83817eab-3f63450e-13c680-15ec1a1eaf855d%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201506487169%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201506487169%2C%22%24uid%22%3A%20%2206796c97.fd8f.79dc.efad.1bb101c56e65%22%2C%22%24recent_outside_referrer%22%3A%20%22%24direct%22%7D%2C%22initial_view_time%22%3A%20%221506486455%22%2C%22initial_referrer%22%3A%20%22%24direct%22%2C%22initial_referrer_domain%22%3A%20%22%24direct%22%7D; UM_distinctid=15ec1a1eaf74d3-0843db83817eab-3f63450e-13c680-15ec1a1eaf855d; _ga=GA1.2.185559595.1507696753; _HUPUSSOID=46d1e8aa-b464-490d-8ef4-624d5f0eef0f; shihuo-double11-views=11; AUM=dgTjQnLkKnbUF_zui89368LHjN5nt-yqlWtWpTno5j7lw; VUID=40A7E0B39DD44388A60B0F3DFA6511D8; CPLOGIN=39454880%7C1509048000000%7C0%7Cd0ad834836375a411367859ab137561e; CPLOGIN_INFO=%7B%22allname%22%3A%22%E8%99%9A%E6%8B%9F%E4%B9%8B%E5%AE%B6%22%2C%22agentId%22%3A%222334709%22%2C%22subname%22%3A%22%E8%99%9A%E6%8B%9F%E4%B9%8B%E5%AE%B6%22%2C%22memLevelImg%22%3A%220%22%2C%22isMigrated%22%3Afalse%2C%22hascertNo%22%3Afalse%2C%22isLocal%22%3Afalse%7D; vcid=3893f26813e71008d7a80b09c60fa373; NAGENTID=2334709; ipfrom=3aab6b6ec87397eca31f1dcd3bdcf58d%09Unknown; _CLT=918ebe7bb324d8673460f7af1d701a5c; u=18850874|6Jma5ouf5LmL5a62|533e|d032cf388bf469ee5cbbf1cc39f2309a|8bf469ee5cbbf1cc|6Jma5ouf5LmL5a62; us=f54317726dcbe3eb18d64771906131fc84313a2261cfd455180056533ff60a5c284880d95b975e2536655e44378b5a6c115249f1f6b11fbd92c85464634cb9aa; lastvisit=27096%091513905571%09%2Fajax%2Fcard.php%3Fuid%3D165402480851831%26ulink%3Dhttps%253A%252F%252Fmy.hupu.com%252F165402480851831%26fid%3D3441%26_%3D1513905; ua=20185713; __dacevst=8c87e67f.84074b9e|1513932718779; _cnzz_CV30020080=buzi_cookie%7C06796c97.fd8f.79dc.efad.1bb101c56e65%7C-1; Hm_lvt_39fc58a7ab8a311f2f6ca4dc1222a96e=1513921677,1513921679,1513921688,1513921695; Hm_lpvt_39fc58a7ab8a311f2f6ca4dc1222a96e=1513930919; _fmdata=EBF73F1CB6FEAEAD093036AC1F63F7EBF411CB6CF3B57C851F277B26FE3FD6765DAE2CCB7B583F6F0326CC573A3654DBD2C8330733272C55'
    cookie_dict = dict((line.split('=') for line in cookie_str.strip().split(";")))

    urls = []
    for page in range(1, 10):
        url = 'https://bbs.hupu.com/bxj'
        if page > 1:
            url = url + '-' + str(page)
        urls.append(url)
    for page in range(1, 10):
        url = 'https://bbs.hupu.com/lol'
        if page > 1:
            url = url + '-' + str(page)
        urls.append(url)

    for page in range(1, 10):
        url = 'https://bbs.hupu.com/vote'
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
        # 记录日志
        logging.log(logging.INFO, '请求url :' + response_url)
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

            # 帖子详情
            article_url = 'https://bbs.hupu.com/' + article_id[0] + '.html'
            print(article_url)
            # article_url = 'https://bbs.hupu.com/21393360.html'
            yield scrapy.Request(article_url, meta={'item': item}, callback=self.article_parse,cookies=self.cookie_dict)

    # 抓取 帖子下面的亮贴，神回复怎能错过-。-
    def article_parse(self, response):
        # inspect_response(response, self)
        comment_item = CommentItem() # 高亮回复
        item = response.meta['item']
        # inspect_response(response, self)
        title = response.xpath('//div[@class="bbs-hd-h1"]/h1/text()').extract()
        item['uid'] = item['author_id']

        time_data = response.xpath('//div[@class="floor-show"]/div[@class="floor_box"]/div[@class="author"]/div[@class="left"]/span[@class="stime"]/text()').extract()
        post_time = time_data[0] if time_data else ''

        # 发帖 的24小时 时间，
        item['post_hour'] = time.strptime(post_time, '%Y-%m-%d %H:%M').tm_hour if post_time else 0

        post_from_data = response.xpath('//div[@class="floor-show"]/div[@class="floor_box"]/table/tbody/tr/td/div[@class="quote-content"]/small/a/text()').extract()

        post_from_str = post_from_data[0] if len(post_from_data) > 0 else ''

        if re.search(r'iPhone', post_from_str):
            post_from = 'iPhone'
        elif re.search(r'Android', post_from_str):
            post_from = 'Android'
        elif re.search(r'm.hupu.com', post_from_str):
            post_from = 'wap'  # 手机网页上
        else:
            post_from = 'web'

        item['post_from'] = post_from

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
                    logging.log(logging.INFO, '用户评论 :' + comment_item['comment_content'])
                comment_item['highlights_num'] = response.xpath('//div[@id=$val]/div[@class="floor_box"]/div[@class="author"]/div[@class="left"]/span/span//span/text()',val=comment_id).extract_first()
                yield comment_item
        item['highlights_re'] = ','.join(highlights_re)
        artcile_post_time = response.xpath('//div[@class="floor-show"]/div[@class="floor_box"]/div[@class="author"]//div[@class="left"]/span[@class="stime"]/text()').extract()
        item['article_post_time'] = artcile_post_time[0] if artcile_post_time else ''  # 文章详情页里面的 发帖时间
        yield item
        user_info_url = 'https://my.hupu.com/' + item['author_id'] + '/profile'
        # user_info_url = 'https://my.hupu.com/' + '52011257892977' + '/profile' # 4822766296690 52011257892977 189695810822085
        yield scrapy.Request(user_info_url, meta={'item': item}, callback=self.user_parse,cookies=self.cookie_dict)

    # 抓取用户信息
    def user_parse(self, response):
        # inspect_response(response, self)
        user_item = UserItem()  # 用户信息
        item = response.meta['item']
        # 记录日志
        logging.log(logging.INFO, '用户id :' + item['author_id'])
        user_item['user_id'] = item['author_id']

        for sel in response.xpath('//div[@id="content"]/table[@class="profile_table"][1]/tr'):

            td_data = sel.xpath('.//td/text()').extract()

            if '性别' in td_data[0] :
                user_item['gender'] = self.get_gender(td_data[1]) if len(td_data) > 1 else 0
            if '等级' in td_data[0] :
                user_item['bbs_level'] = td_data[1] if len(td_data) > 1 else 0
            if '社团' in td_data[0] :
                user_item['associations'] = td_data[1] if len(td_data) > 1 else 0
            if '现金' in td_data[0]:
                hupu_property_data = td_data[1] if len(td_data) > 1 else 0
                property = re.findall(r'^(\d+).*$', hupu_property_data)
                user_item['hupu_property'] = property[0] if len(property) > 0 else 0
            if '在线' in td_data[0]:
                online_time_data = td_data[1] if len(td_data) > 1 else 0
                online_time = re.findall(r'^(\d+).*$', online_time_data)
                user_item['online_time'] = online_time[0] if len(online_time) > 0 else 0
            if '注册' in td_data[0]:
                user_item['reg_time'] = td_data[1] if len(td_data) > 1 else 0
            if '最后' in td_data[0]:
                user_item['last_login'] = td_data[1] if len(td_data) > 1 else 0
            if '自我' in td_data[0]:
                user_item['self_introduction'] = td_data[1] if len(td_data) > 1 else ''

        # common_path = response.xpath('//div[@id="content"]/table[@class="profile_table"][1]')

        # 档案中 ，有些包含地区有些没有，造成资料行数不一致
        # tr_count = len(response.xpath('//div[@id="content"]/table[@class="profile_table"][1]/tr').extract())
        # is_offset = 1 if tr_count > 8 else 0

        # profile = response.xpath('//div[@id="content"]/table[@class="profile_table"]/tr/td/text()').extract()

        # user_item['gender'] = profile[1] if len(profile[1]) > 0 else '保密'
        # gender_res = common_path.xpath('.//tr[1]/td/text()').extract()
        # gender_val = gender_res[1] if len(gender_res) > 1 else '保密'
        # user_item['gender'] = self.get_gender(gender_val)

        # user_item['bbs_reputation'] = 0

        # 社区等级
        # level_tr = 3 if is_offset else 2
        # bbs_level_res = common_path.xpath('.//tr[$val]/td/text()', val=level_tr).extract()
        # user_item['bbs_level'] = bbs_level_res[1] if len(bbs_level_res) > 1 else 0

        # 所属社团
        # associations_tr = 4 if is_offset else 3
        # associations_res = common_path.xpath('.//tr[$val]/td/text()', val=associations_tr).extract()
        # user_item['associations'] = associations_res[1] if len(associations_res) > 1 else 0

        # 社区资产
        # property_tr = 5 if is_offset else 4
        # hupu_property_res = common_path.xpath('.//tr[$val]/td/text()', val=property_tr).extract()
        # hupu_property_data =  hupu_property_res[1] if len(hupu_property_res) > 1 else 0
        # property = re.findall(r'^(\d+).*$', hupu_property_data)
        # user_item['hupu_property'] = property[0] if len(property) > 0 else 0

        # 在线时间
        # online_time_tr = 6 if is_offset else 5
        # online_time_res = common_path.xpath('.//tr[$val]/td/text()', val=online_time_tr).extract()
        # online_time_data = online_time_res[1] if len(online_time_res) > 1 else 0
        # online_time = re.findall(r'^(\d+).*$', online_time_data)
        # user_item['online_time'] = online_time[0] if len(online_time) > 0 else 0

        # reg_time_tr = 7 if is_offset else 6
        # reg_time_res = common_path.xpath('.//tr[$val]/td/text()', val=reg_time_tr).extract()
        # user_item['reg_time'] = reg_time_res[1] if len(reg_time_res) > 1 else 0
        #
        # last_login_tr = 8 if is_offset else 7
        # last_login_res =  common_path.xpath('.//tr[$val]/td/text()', val=last_login_tr).extract()
        # user_item['last_login'] = last_login_res[1] if len(last_login_res) > 1 else 0
        #
        # introduction_tr = 9 if is_offset else 8
        # self_introduction_res = common_path.xpath('.//tr[$val]/td/text()', val=introduction_tr).extract()
        # user_item['self_introduction'] = self_introduction_res[1] if len(self_introduction_res) > 1 else ''

        # 喜欢的事情
        common_path_favorite = response.xpath('//div[@id="content"]/table[@class="profile_table"][2]')
        favorite_sport_res = common_path_favorite.xpath('.//tr[1]/td/text()').extract()
        user_item['favorite_sport'] = favorite_sport_res[1] if len(favorite_sport_res) > 1 else ''
        # 最喜欢的联赛
        favorite_league_res = common_path_favorite.xpath('.//tr[2]/td/text()').extract()
        user_item['favorite_league'] = favorite_league_res[1] if len(favorite_league_res) > 1 else ''

        favorite_team_res = common_path_favorite.xpath('.//tr[3]/td/text()').extract()
        user_item['favorite_team'] = favorite_team_res[1] if len(favorite_team_res) > 1 else ''

       # yield user_item
        user_info_other_url = 'https://my.hupu.com/' + item['author_id']
        # user_info_other_url = 'https://my.hupu.com/' + '268318221130217'  # 4822766296690 52011257892977 189695810822085
        yield scrapy.Request(user_info_other_url, meta={'user_item': user_item}, callback=self.user_other_parse, cookies=self.cookie_dict)

    # 粉丝，关注人数，社区声望-，访问人数
    def user_other_parse(self, response):
        # inspect_response(response, self)
        user_item = response.meta['user_item']
        # 记录日志
        logging.log(logging.INFO, '用户id 额外信息 :' + user_item['user_id'])
        # 访问数
        user_visit_data = response.xpath('//div[@class="personal_right"]/h3[@class="mpersonal"]/span[@class="f666"]/text()').extract()
        user_visit_num = re.findall(r'^.(\d+).*$', user_visit_data[0]) if len(user_visit_data) > 0 else []
        user_item['visit_num'] = user_visit_num[0] if len(user_visit_num) > 0 else 0

        # 粉丝数
        follower_data = response.xpath('//div[@id="following"]/p[@class="more"]/a[contains(@href, "follower")]/text()').extract()
        follower_num = re.findall(r'^(\d+).*$', follower_data[0]) if len(follower_data) > 0 else []
        user_item['follower_num'] = follower_num[0] if len(follower_num) > 0 else 0

        # 关注人数
        followering_data = response.xpath('//div[@id="following"]/p[@class="more"]/a[contains(@href, "following")]/text()').extract()
        followering_num = re.findall(r'.(\d+).*$', followering_data[0]) if len(followering_data) > 0 else []
        user_item['followering_num'] = followering_num[0] if len(followering_num) > 0 else 0

        # 社区声望, 这个比较难得抓取，数据不在标签内，并且上级标签是保持一致
        string_data = response.xpath('//div[@class="personal_right"]/div[@class="personalinfo"]').xpath('string(.)').extract()
        bbs_reputation_data = string_data[0] if len(string_data) > 0 else ''
        reputation_res = re.findall(r'.社区声望.(\d+)\n.*', bbs_reputation_data)
        user_item['bbs_reputation'] = reputation_res[0] if len(reputation_res) > 0 else 0

        user_info_topic_url = 'https://my.hupu.com/' + user_item['user_id'] + '/topic'
        # user_info_topic_url = 'https://my.hupu.com/' + '210000370364932' + '/topic'
        yield scrapy.Request(user_info_topic_url, meta={'user_item': user_item}, callback=self.user_topic_parse,
                             cookies=self.cookie_dict)

    # 回帖数，收藏数，主题帖数，
    def user_topic_parse(self, response):
        # inspect_response(response, self)
        user_item = response.meta['user_item']
        data = response.xpath('//div[@class="tabs_header"]/form/ul/li/a[contains(@href, "topic")]/span').xpath("string(.)").extract()
        topic_data_str = ','.join(data)
        # 主题数
        topic_data = re.findall(r'^.*主题 \((\d+)\)', topic_data_str)
        user_item['topic_num'] = topic_data[0] if len(topic_data) > 0 else 0

        # 回帖数
        re_data = re.findall(r'^.*回帖 \((\d+)\)', topic_data_str)
        user_item['re_topic_num'] = re_data[0] if len(re_data) > 0 else 0

        # 收藏数
        collect_data = re.findall(r'^.*收藏 \((\d+)\)$', topic_data_str)
        user_item['collect_num'] = collect_data[0] if len(collect_data) > 0 else 0

        yield user_item

    @classmethod
    def get_gender(cls, gender_val):
        if gender_val == '男':
            return 2
        elif gender_val == '女':
            return 1
        else:
            return 0
