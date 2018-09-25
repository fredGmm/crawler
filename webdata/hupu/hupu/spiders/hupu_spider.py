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
import os
import urllib.request
from os import path


class HupuSpider(scrapy.Spider):
    name = "hupu"
    allowed_domains = ["hupu.com"]
    # 去掉 __gads=ID=d140a94144ba1993:T=1505436772:S=ALNI_MaNd80C0poIVcASdbf8orkORfg6_w;
    cookie_str = '_dacevid3=4819cb5a.690d.f68f.3cf3.c7ff9c1431cf;_cnzz_CV30020080=buzi_cookie%7C4819cb5a.690d.f68f.3cf3.c7ff9c1431cf%7C-1; PHPSESSID=8eef5ff57f0a73b6a86b69c51f61a64b; __dacevid3=0x5c0888ed5b55a224; __dacemvst=4607398e.25593d82; _HUPUSSOID=a50545ef-d8bc-4f9e-b22c-3bdea9d6da23; _CLT=918ebe7bb324d8673460f7af1d701a5c; lastvisit=332%091536299241%09%2Ferror%2F%40_%40.php%3F; _fmdata=gc7eUe7%2FFZ0tTaFl8v59g0pokS3aUfK9aMafRGLWgwojvpPdgcgdwHF0db9n%2BdxuPeylAWpMOoQmvxte6i9wlddXRyErTYhV5QICZez80Yk%3D; u=18850874|6Jma5ouf5LmL5a62|533e|d032cf388bf469ee5cbbf1cc39f2309a|8bf469ee5cbbf1cc|6Jma5ouf5LmL5a62; us=f7d105b75c496b72a0ba8c655a5eee216deb64819a3dae95093cb839878c567bd137ce49fb1de6ada7e146a306945c215b0a0febe8316898a5d200709876b476; ua=20490762; Hm_lvt_39fc58a7ab8a311f2f6ca4dc1222a96e=1536390543,1536807215; Hm_lpvt_39fc58a7ab8a311f2f6ca4dc1222a96e=1536807224; __dacevst=64ab0b00.ec98c989|1536809033801'
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

    def __init__(self, is_down_image= ''):
        self.is_down_image = is_down_image


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
            # article_url = 'https://bbs.hupu.com/19162124.html'  # 21663262
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

        post_from_data = response.xpath('//div[@class="floor-show"]/div[@class="floor_box"]/table/tbody/tr/td/div[@class="quote-content"]/small').xpath('string(.)').extract()

        post_from_str = post_from_data[0] if len(post_from_data) > 0 else ''
        logging.info(item['article_id'] + '来源：' + post_from_str)
        if re.search(r'iPhone', post_from_str):
            post_from = 'iPhone'
        elif re.search(r'Android', post_from_str):
            post_from = 'Android'
        elif re.search(r'm\.hupu\.com', post_from_str): # https://bbs.hupu.com/21750357.html 发自 m.hupu.com
            post_from = 'wap'  # 手机网页上
        else:
            post_from = 'web'

        item['post_from'] = post_from

        content = response.xpath('//div[@class="floor-show"]/div[@class="floor_box"]/table/tbody/tr/td/div[@class="quote-content"]').xpath('string(.)').extract()
        item['article_content'] = content[0] if content else 0
        images = response.xpath('//div[@class="floor-show"]/div[@class="floor_box"]/table/tbody/tr/td/div[@class="quote-content"]').xpath('.//a/@href').extract()

        images2 = response.xpath('//div[@class="floor-show"]/div[@class="floor_box"]/table/tbody/tr/td/div[@class="quote-content"]').xpath('.//img/@src').extract()

        images3 = response.xpath('//div[@class="floor-show"]/div[@class="floor_box"]/table/tbody/tr/td/div[@class="quote-content"]').xpath('.//img/@data-original').extract()

        all_img = images + images2 + images3
        # 有些事惰加载，有些事默认图片;注意是用切片复制，否则会遇到循环删除的坑
        for img in all_img[:]:
            if 'placeholder.png' in img:
                all_img.remove(img)
        if self.is_down_image:
            self.down_image(item['article_id'], all_img)

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

                comment_images = response.xpath('//div[@id=$val]/div[@class="floor_box"]/table/tbody',
                                                val=comment_id).xpath('.//img/@src').extract()
                comment_images2 = response.xpath('//div[@id=$val]/div[@class="floor_box"]/table/tbody',
                                                 val=comment_id).xpath('.//img/@data-original').extract()

                comment_all_images = comment_images + comment_images2
                for comment_img in comment_all_images[:]:
                    if 'placeholder.png' in comment_img:
                        all_img.remove(comment_img)

                comment_item['comment_images'] = json.dumps(comment_all_images)
                if self.is_down_image:
                    self.down_image(str(item['article_id']), comment_all_images)

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
        print('进入用户 %s', item['author_id'])
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

    @classmethod
    def down_image(cls, article_id, image_urls):
        print('我是贴子:%s 的，进程ID是 %s' % (article_id, os.getpid()))

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            # 'Accept-Encoding':'gzip, deflate',
            'Upgrade-Insecure-Requests': '1',
            # 'Cookie': '__gads=ID=2b1d2d4629e10087:T=1502422342:S=ALNI_MapJj4uFT0lKBxgxvDtj9L6AjSJeg; Hm_lvt_609cf0cb82b363063bcf56b050b31c06=1507796834; Hm_lpvt_609cf0cb82b363063bcf56b050b31c06=1507796834; UM_distinctid=15f0fe450055a9-0aacb9fd0a4a64-3e63430c-13c680-15f0fe45009577; CNZZDATA3980738=cnzz_eid%3D375819982-1507795998-null%26ntime%3D1507795998; CNZZDATA5299104=cnzz_eid%3D720537324-1508487488-null%26ntime%3D1508487488; AJSTAT_ok_times=1; CNZZDATA1254929547=202459006-1509005456-null%7C1509071800; Hm_lvt_444ece9ccd5b847838a56c93a0975a8b=1509008713,1509074912; Hm_lpvt_444ece9ccd5b847838a56c93a0975a8b=1509074912; CNZZDATA1259671153=1268634678-1511226188-https%253A%252F%252Fwww.baidu.com%252F%7C1511226188; Hm_lvt_1628f7c8d025473b441a8ba490edd441=1512439552; Hm_lpvt_1628f7c8d025473b441a8ba490edd441=1512439552; Hm_lvt_674430fbddd66a488580ec86aba288f7=1513132898,1513327292,1515145381; Hm_lpvt_674430fbddd66a488580ec86aba288f7=1515145381; CNZZDATA4343144=cnzz_eid%3D1379924068-1515145381-https%253A%252F%252Fwww.baidu.com%252F%26ntime%3D1515145381; CNZZDATA1260528602=830205212-1516873652-https%253A%252F%252Fwww.baidu.com%252F%7C1516873652; CNZZDATA1255738818=1995071737-1511861766-https%253A%252F%252Fwww.baidu.com%252F%7C1517381708; .CNBlogsCookie=7DC0E158877A3B3865D6D99E645D51E1D11BEF8934D86FB7FE0CC59A25794D09D739DFC03869EC2A86D72CBEE007B232227197C0483287817CDA55E064EA1CE3AB07A2494BB202502FF66E79672BBE0043007FBA; .Cnblogs.AspNetCore.Cookies=CfDJ8N7AeFYNSk1Put6Iydpme2YM5BXxs9Iw_G-2Z0oxgAomua6n29m8EgElmo-91D_2ROw8uiG3GRB08Wnf7oRomnCcgSKTaLeVrjmmYBe2oRQvRYF0sqak0m3kshjgcdZ8xpX38QK7GWaTB1G2EBWCX-i2NW_bSLqTcYlt-7hsvIJDA5VNVefTdhoNXdoKdvuXsUZvZaVzao_RacuoCTJe9730Y7Q-9AOMgkmTmMDkMxUqVXMzSDVN4l19fcrDOC7ZyH5wgHgoWE9akxoKpbv8i0QRnlDMVrVmM2axFdSX1Ki9; CNZZDATA1254486480=481500654-1519714184-https%253A%252F%252Fwww.baidu.com%252F%7C1519714184; uaid=ef7b9981e897d4ca720fa7770adadd7e; CNZZDATA5646633=cnzz_eid%3D1257097878-1519975944-https%253A%252F%252Fwww.baidu.com%252F%26ntime%3D1519975944; Hm_lvt_5f2c57e3e6679dd27bb04237bdadde15=1520214030; Hm_lpvt_5f2c57e3e6679dd27bb04237bdadde15=1520214030; _gat=1; _ga=GA1.2.37373735.1501748284; _gid=GA1.2.2052215384.1520212099', # 关键点啊，特么在cookie里埋标识
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
        }

        try:
            # print('总共%s 条记录' % len(result))
            date = time.strftime('%Y%m%d%H0000', time.localtime())
            for image in image_urls:
                url = image
                if 'jpg' in url or url.find('jpeg') > -1 or url.find('png') > -1 or url.find('gif') > -1:
                    # url = url.strip('" "')
                    # url = "https://t12.baidu.com/it/u=2388568829,148893518&fm=173&s=01725C908A5108C81A07A8C3030070AB&w=640&h=1580&img.JPEG"
                    # url = "http://shihuo.hupucdn.com/price/201801/2611/f5ab1a2169d474880d5828c7177c9d50.jpg"
                    # url = "https://i10.hoopchina.com.cn/hupuapp/bbs/854/71064499034854/thread_71064499034854_20180131020728_s_163310_h_1334px_w_750px1373773358.jpeg?x-oss-process=image/resize,w_800/format,webp"

                    if '?' in url:  # 有些是手机适配图片，如上面的链接
                        url = url[:url.find('?')]
                    print(url)
                    try:
                        request = urllib.request.Request(url, headers=headers)
                        handler = urllib.request.HTTPCookieProcessor()
                        opener = urllib.request.build_opener(handler)
                        response = opener.open(request)
                    except Exception as e:
                        print("出错了", e)
                        print("该链接:", url, 'id:', article_id)
                        continue

                    if response.code == 200:
                        file_extension = os.path.splitext(url)
                        ext = file_extension[1] if len(file_extension) > 1 else '.jpg'
                        image_name = str(article_id) + '.html' + ext

                        image_path = os.path.dirname(os.path.realpath(__file__)) + '/../static/images_' + str(
                            date) + '/'
                        if not os.path.exists(image_path):
                            os.makedirs(image_path)

                        i=2
                        while os.path.exists(image_path + image_name):
                            s = str(i)
                            image_name = str(article_id) + '.html' + '('+s+')' + ext
                            i = i + 1

                        with open( image_path + image_name, "wb") as code:
                            code.write(response.read())

        except ValueError as e:
            print('mysql insert fail', e)

        else:
            print('结束')
