# -*- coding: utf-8 -*-

import scrapy
from hupu.items import HupuItem
from hupu.items import CommentItem
from hupu.items import OtherItem
from scrapy.shell import inspect_response
from scrapy.http.request import Request
from scrapy.utils.project import get_project_settings
import json
import re
import logging
import time


class HupuStaticViewSpider(scrapy.Spider):
    name = "hupu_static_view"
    allowed_domains = ["hupu.com"]
    # 去掉 __gads=ID=d140a94144ba1993:T=1505436772:S=ALNI_MaNd80C0poIVcASdbf8orkORfg6_w;
    cookie_str = 'PHPSESSID=nepe6b122jjla5hubir1gkcvg3; _dacevid3=06796c97.fd8f.79dc.efad.1bb101c56e65;  __dacevid3=0xcdffaaaa291e1499; cn_2815e201bfe10o53c980_dplus=%7B%22distinct_id%22%3A%20%2215ec1a1eaf74d3-0843db83817eab-3f63450e-13c680-15ec1a1eaf855d%22%2C%22sp%22%3A%20%7B%22%24_sessionid%22%3A%200%2C%22%24_sessionTime%22%3A%201506487169%2C%22%24dp%22%3A%200%2C%22%24_sessionPVTime%22%3A%201506487169%2C%22%24uid%22%3A%20%2206796c97.fd8f.79dc.efad.1bb101c56e65%22%2C%22%24recent_outside_referrer%22%3A%20%22%24direct%22%7D%2C%22initial_view_time%22%3A%20%221506486455%22%2C%22initial_referrer%22%3A%20%22%24direct%22%2C%22initial_referrer_domain%22%3A%20%22%24direct%22%7D; UM_distinctid=15ec1a1eaf74d3-0843db83817eab-3f63450e-13c680-15ec1a1eaf855d; _ga=GA1.2.185559595.1507696753; _HUPUSSOID=46d1e8aa-b464-490d-8ef4-624d5f0eef0f; shihuo-double11-views=11; AUM=dgTjQnLkKnbUF_zui89368LHjN5nt-yqlWtWpTno5j7lw; VUID=40A7E0B39DD44388A60B0F3DFA6511D8; CPLOGIN=39454880%7C1509048000000%7C0%7Cd0ad834836375a411367859ab137561e; CPLOGIN_INFO=%7B%22allname%22%3A%22%E8%99%9A%E6%8B%9F%E4%B9%8B%E5%AE%B6%22%2C%22agentId%22%3A%222334709%22%2C%22subname%22%3A%22%E8%99%9A%E6%8B%9F%E4%B9%8B%E5%AE%B6%22%2C%22memLevelImg%22%3A%220%22%2C%22isMigrated%22%3Afalse%2C%22hascertNo%22%3Afalse%2C%22isLocal%22%3Afalse%7D; vcid=3893f26813e71008d7a80b09c60fa373; NAGENTID=2334709; ipfrom=3aab6b6ec87397eca31f1dcd3bdcf58d%09Unknown; _CLT=918ebe7bb324d8673460f7af1d701a5c; u=18850874|6Jma5ouf5LmL5a62|533e|d032cf388bf469ee5cbbf1cc39f2309a|8bf469ee5cbbf1cc|6Jma5ouf5LmL5a62; us=f54317726dcbe3eb18d64771906131fc84313a2261cfd455180056533ff60a5c284880d95b975e2536655e44378b5a6c115249f1f6b11fbd92c85464634cb9aa; lastvisit=27096%091513905571%09%2Fajax%2Fcard.php%3Fuid%3D165402480851831%26ulink%3Dhttps%253A%252F%252Fmy.hupu.com%252F165402480851831%26fid%3D3441%26_%3D1513905; ua=20185713; __dacevst=8c87e67f.84074b9e|1513932718779; _cnzz_CV30020080=buzi_cookie%7C06796c97.fd8f.79dc.efad.1bb101c56e65%7C-1; Hm_lvt_39fc58a7ab8a311f2f6ca4dc1222a96e=1513921677,1513921679,1513921688,1513921695; Hm_lpvt_39fc58a7ab8a311f2f6ca4dc1222a96e=1513930919; _fmdata=EBF73F1CB6FEAEAD093036AC1F63F7EBF411CB6CF3B57C851F277B26FE3FD6765DAE2CCB7B583F6F0326CC573A3654DBD2C8330733272C55'
    cookie_dict = dict((line.split('=') for line in cookie_str.strip().split(";")))

     # 'https://bbs.hupu.com/get_nav?fup=174','https://bbs.hupu.com/get_nav?fup=234'
    urls = ['https://bbs.hupu.com/boards.php', ]

    start_urls = urls

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, cookies=self.cookie_dict)

    def parse(self, response):
        # inspect_response(response, self)
        # [各个板块对应的id ] bxj步行街 pgq破瓜区 it数码  xfl学府路 selfie爆照区  999万事屋   ent影视区   cars车友交流  acg ACG区  finance 股票区
        # music音乐区  literature文学区 love情感区 wallpaper手机壁纸区 hccares 虎扑助学基金会 fit 健康和运动健康

        # bxj 步行街
        bxj = response.xpath('//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="gby"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "bxj")]/../span/text()').extract()
        bxj_data = bxj[0] if len(bxj)>0 else ''
        bxj_res = re.findall(r'.(\d+).*$', bxj_data)
        bxj_num = bxj_res[0] if len(bxj_res) > 0 else 0

        # 破瓜区
        pgq = response.xpath('//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="gby"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "pogua")]/../span/text()').extract()
        pgq_data = pgq[0] if len(pgq) > 0 else ''
        pgq_res = re.findall(r'.(\d+).*$', pgq_data)
        pgq_num = pgq_res[0] if len(pgq_res) > 0 else 0

        # it数码
        itsm = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="gby"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "digital")]/../span/text()').extract()
        itsm_data = itsm[0] if len(itsm) > 0 else ''
        itsm_res = re.findall(r'.(\d+).*$', itsm_data)
        itsm_num = itsm_res[0] if len(itsm_res) > 0 else 0

        # xfl学府路
        xfl = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="gby"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "xuefu")]/../span/text()').extract()
        xfl_data = xfl[0] if len(xfl) > 0 else ''
        xfl_res = re.findall(r'.(\d+).*$', xfl_data)
        xfl_num = xfl_res[0] if len(xfl_res) > 0 else 0

        # 爆照区
        selfie = response.xpath('//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="gby"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "selfie")]/../span/text()').extract()
        selfie_data = selfie[0] if len(selfie) > 0 else ''
        selfie_res = re.findall(r'.(\d+).*$', selfie_data)
        selfie_num = selfie_res[0] if len(selfie_res) > 0 else 0

        # 万事屋
        nine999 = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="gby"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "999")]/../span/text()').extract()
        nine999_data = nine999[0] if len(nine999) > 0 else ''
        nine999_res = re.findall(r'.(\d+).*$', nine999_data)
        nine999_num = nine999_res[0] if len(nine999_res) > 0 else 0

        # 影视区
        ent = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="gby"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "ent")]/../span/text()').extract()
        ent_data = ent[0] if len(ent) > 0 else ''
        ent_res = re.findall(r'.(\d+).*$', ent_data)
        ent_num = ent_res[0] if len(ent_res) > 0 else 0

        # 车友交流
        cars = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="gby"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "cars")]/../span/text()').extract()
        cars_data = cars[0] if len(cars) > 0 else ''
        cars_res = re.findall(r'.(\d+).*$', cars_data)
        cars_num = cars_res[0] if len(cars_res) > 0 else 0

        # ACG区
        acg = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="gby"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "acg")]/../span/text()').extract()
        acg_data = acg[0] if len(acg) > 0 else ''
        acg_res = re.findall(r'.(\d+).*$', acg_data)
        acg_num = acg_res[0] if len(acg_res) > 0 else 0

        # 股票区
        finance = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="gby"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "finance")]/../span/text()').extract()
        finance_data = finance[0] if len(finance) > 0 else ''
        finance_res = re.findall(r'.(\d+).*$', finance_data)
        finance_num = finance_res[0] if len(finance_res) > 0 else 0

        # 音乐区
        muisc = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="gby"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "music")]/../span/text()').extract()
        muisc_data = muisc[0] if len(muisc) > 0 else ''
        muisc_res = re.findall(r'.(\d+).*$', muisc_data)
        muisc_num = muisc_res[0] if len(muisc_res) > 0 else 0

        # 文学区
        literature = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="gby"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "literature")]/../span/text()').extract()
        literature_data = literature[0] if len(literature) > 0 else ''
        literature_res = re.findall(r'.(\d+).*$', literature_data)
        literature_num = literature_res[0] if len(literature_res) > 0 else 0

        # 情感区
        love = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="gby"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "love")]/../span/text()').extract()
        love_data = love[0] if len(love) > 0 else ''
        love_res = re.findall(r'.(\d+).*$', love_data)
        love_num = love_res[0] if len(love_res) > 0 else 0

        # 虎扑助学基金会
        hccares = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="gby"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "hccares")]/../span/text()').extract()
        hccares_data = hccares[0] if len(hccares) > 0 else ''
        hccares_res = re.findall(r'.(\d+).*$', hccares_data)
        hccares_num = hccares_res[0] if len(hccares_res) > 0 else 0

        # 虎扑助学基金会
        fit = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="gby"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "fit")]/../span/text()').extract()
        fit_data = fit[0] if len(fit) > 0 else ''
        fit_res = re.findall(r'.(\d+).*$', fit_data)
        fit_num = fit_res[0] if len(fit_res) > 0 else 0

        # [NBA 各版块对应的id] shh湿乎乎  nba_draft_ncaa选秀nba  nba篮球场 4832天天nba dailyfantasy每日对抗
        # rockets火箭专区  warriors勇士 cavaliers骑士 spurs马刺 lakers湖人  celtics凯尔特人  thunder雷霆专区
        # clippers快船 timberwolves森林狼  mavericks独行侠  knicks尼克斯专区  bulls公牛专区 sixers76专区
        # nets篮网专区 jazz爵士专区 pacers步行者 blazers开拓者 heats热火专区 suns太阳专区 grizzlies灰熊专区
        # wizards奇才专区 magic魔术专区 pelicans鹈鹕专区
        # bucks雄鹿专区 kings国王专区 raptors猛龙专区 nuggets掘金专区 hawks老鹰专区  hornets黄蜂专区
        # pistons活塞专区  lurenwang路人王专区  fiba世界篮球-FIBA

        # 湿乎乎话题
        shh = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="basketball"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "vote")]/../span/text()').extract()
        shh_data = shh[0] if len(shh) > 0 else ''
        shh_res = re.findall(r'.(\d+).*$', shh_data)
        shh_num = shh_res[0] if len(shh_res) > 0 else 0

        # nba_draft_ncaa选秀nba
        nba_draft_ncaa = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="basketball"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "nba-draft-ncaa")]/../span/text()').extract()
        nba_draft_ncaa_data = nba_draft_ncaa[0] if len(nba_draft_ncaa) > 0 else ''
        nba_draft_ncaa_res = re.findall(r'.(\d+).*$', nba_draft_ncaa_data)
        nba_draft_ncaa_num = nba_draft_ncaa_res[0] if len(nba_draft_ncaa_res) > 0 else 0

        # nba篮球场
        nba = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="basketball"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "nba")]/../span/text()').extract()
        nba_data = nba[0] if len(nba) > 0 else ''
        nba_res = re.findall(r'.(\d+).*$', nba_data)
        nba_num = nba_res[0] if len(nba_res) > 0 else 0

        #  4832天天nba
        four832 = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="basketball"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "4832")]/../span/text()').extract()
        four832_data = four832[0] if len(four832) > 0 else ''
        four832_res = re.findall(r'.(\d+).*$', four832_data)
        four832_num = four832_res[0] if len(four832_res) > 0 else 0

        #  dailyfantasy每日对抗
        dailyfantasy = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="basketball"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "dailyfantasy")]/../span/text()').extract()
        dailyfantasy_data = dailyfantasy[0] if len(dailyfantasy) > 0 else ''
        dailyfantasy_res = re.findall(r'.(\d+).*$', dailyfantasy_data)
        dailyfantasy_num = dailyfantasy_res[0] if len(dailyfantasy_res) > 0 else 0

        #  rockets火箭专区
        rockets = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="basketball"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "rockets")]/../span/text()').extract()
        rockets_data = rockets[0] if len(rockets) > 0 else ''
        rockets_res = re.findall(r'.(\d+).*$', rockets_data)
        rockets_num = rockets_res[0] if len(rockets_res) > 0 else 0

        #  warriors勇士
        warriors = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="basketball"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "warriors")]/../span/text()').extract()
        warriors_data = warriors[0] if len(warriors) > 0 else ''
        warriors_res = re.findall(r'.(\d+).*$', warriors_data)
        warriors_num = warriors_res[0] if len(warriors_res) > 0 else 0

        #  cavaliers骑士
        cavaliers = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="basketball"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "cavaliers")]/../span/text()').extract()
        cavaliers_data = cavaliers[0] if len(cavaliers) > 0 else ''
        cavaliers_res = re.findall(r'.(\d+).*$', cavaliers_data)
        cavaliers_num = cavaliers_res[0] if len(cavaliers_res) > 0 else 0

        #  spurs马刺
        spurs = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="basketball"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "spurs")]/../span/text()').extract()
        spurs_data = spurs[0] if len(spurs) > 0 else ''
        spurs_res = re.findall(r'.(\d+).*$', spurs_data)
        spurs_num = spurs_res[0] if len(spurs_res) > 0 else 0

        #   lakers湖人
        lakers = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="basketball"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "lakers")]/../span/text()').extract()
        lakers_data = lakers[0] if len(lakers) > 0 else ''
        lakers_res = re.findall(r'.(\d+).*$', lakers_data)
        lakers_num = lakers_res[0] if len(lakers_res) > 0 else 0

        #   celtics凯尔特人
        celtics = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="basketball"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "celtics")]/../span/text()').extract()
        celtics_data = celtics[0] if len(celtics) > 0 else ''
        celtics_res = re.findall(r'.(\d+).*$', celtics_data)
        celtics_num = celtics_res[0] if len(celtics_res) > 0 else 0

        #   thunder雷霆专区
        thunder = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="basketball"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "thunder")]/../span/text()').extract()
        thunder_data = thunder[0] if len(thunder) > 0 else ''
        thunder_res = re.findall(r'.(\d+).*$', thunder_data)
        thunder_num = thunder_res[0] if len(thunder_res) > 0 else 0

        #   clippers快船
        clippers = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="basketball"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "clippers")]/../span/text()').extract()
        clippers_data = clippers[0] if len(clippers) > 0 else ''
        clippers_res = re.findall(r'.(\d+).*$', clippers_data)
        clippers_num = clippers_res[0] if len(clippers_res) > 0 else 0

        #   timberwolves森林狼
        timberwolves = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="basketball"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "timberwolves")]/../span/text()').extract()
        timberwolves_data = timberwolves[0] if len(timberwolves) > 0 else ''
        timberwolves_res = re.findall(r'.(\d+).*$', timberwolves_data)
        timberwolves_num = timberwolves_res[0] if len(timberwolves_res) > 0 else 0

        #   mavericks独行侠
        mavericks = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="basketball"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "mavericks")]/../span/text()').extract()
        mavericks_data = mavericks[0] if len(mavericks) > 0 else ''
        mavericks_res = re.findall(r'.(\d+).*$', mavericks_data)
        mavericks_num = mavericks_res[0] if len(mavericks_res) > 0 else 0

        #   knicks尼克斯专区
        knicks = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="basketball"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "knicks")]/../span/text()').extract()
        knicks_data = knicks[0] if len(knicks) > 0 else ''
        knicks_res = re.findall(r'.(\d+).*$', knicks_data)
        knicks_num = knicks_res[0] if len(knicks_res) > 0 else 0

        #   bulls公牛专区
        bulls = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="basketball"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "bulls")]/../span/text()').extract()
        bulls_data = bulls[0] if len(bulls) > 0 else ''
        bulls_res = re.findall(r'.(\d+).*$', bulls_data)
        bulls_num = knicks_res[0] if len(bulls_res) > 0 else 0

        #   sixers76专区
        sixers = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="basketball"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "sixers")]/../span/text()').extract()
        sixers_data = sixers[0] if len(sixers) > 0 else ''
        sixers_res = re.findall(r'.(\d+).*$', sixers_data)
        sixers_num = sixers_res[0] if len(sixers_res) > 0 else 0

        # nets篮网专区
        nets = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="basketball"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "nets")]/../span/text()').extract()
        nets_data = nets[0] if len(nets) > 0 else ''
        nets_res = re.findall(r'.(\d+).*$', nets_data)
        nets_num = nets_res[0] if len(nets_res) > 0 else 0

        # jazz爵士专区
        jazz = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="basketball"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "jazz")]/../span/text()').extract()
        jazz_data = jazz[0] if len(jazz) > 0 else ''
        jazz_res = re.findall(r'.(\d+).*$', jazz_data)
        jazz_num = jazz_res[0] if len(jazz_res) > 0 else 0

        # pacers步行者
        pacers = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="basketball"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "pacers")]/../span/text()').extract()
        pacers_data = pacers[0] if len(pacers) > 0 else ''
        pacers_res = re.findall(r'.(\d+).*$', pacers_data)
        pacers_num = pacers_res[0] if len(pacers_res) > 0 else 0

        #  blazers开拓者
        blazers = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="basketball"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "blazers")]/../span/text()').extract()
        blazers_data = blazers[0] if len(blazers) > 0 else ''
        blazers_res = re.findall(r'.(\d+).*$', blazers_data)
        blazers_num = blazers_res[0] if len(blazers_res) > 0 else 0

        #  heat热火专区
        heat = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="basketball"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "heat")]/../span/text()').extract()
        heat_data = heat[0] if len(heat) > 0 else ''
        heat_res = re.findall(r'.(\d+).*$', heat_data)
        heat_num = heat_res[0] if len(heat_res) > 0 else 0

        #  suns太阳专区
        suns = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="basketball"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "suns")]/../span/text()').extract()
        suns_data = suns[0] if len(suns) > 0 else ''
        suns_res = re.findall(r'.(\d+).*$', suns_data)
        suns_num = suns_res[0] if len(suns_res) > 0 else 0

        #  grizzlies灰熊专区
        grizzlies = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="basketball"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "grizzlies")]/../span/text()').extract()
        grizzlies_data = grizzlies[0] if len(grizzlies) > 0 else ''
        grizzlies_res = re.findall(r'.(\d+).*$', grizzlies_data)
        grizzlies_num = grizzlies_res[0] if len(grizzlies_res) > 0 else 0

        #  wizards奇才专区
        wizards = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="basketball"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "wizards")]/../span/text()').extract()
        wizards_data = wizards[0] if len(wizards) > 0 else ''
        wizards_res = re.findall(r'.(\d+).*$', wizards_data)
        wizards_num = wizards_res[0] if len(wizards_res) > 0 else 0

        #  magic魔术专区
        magic = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="basketball"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "magic")]/../span/text()').extract()
        magic_data = magic[0] if len(magic) > 0 else ''
        magic_res = re.findall(r'.(\d+).*$', magic_data)
        magic_num = magic_res[0] if len(magic_res) > 0 else 0

        #  pelicans鹈鹕专区
        pelicans = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="basketball"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "pelicans")]/../span/text()').extract()
        pelicans_data = pelicans[0] if len(pelicans) > 0 else ''
        pelicans_res = re.findall(r'.(\d+).*$', pelicans_data)
        pelicans_num = pelicans_res[0] if len(pelicans_res) > 0 else 0

        # bucks雄鹿专区
        bucks = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="basketball"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "bucks")]/../span/text()').extract()
        bucks_data = bucks[0] if len(bucks) > 0 else ''
        bucks_res = re.findall(r'.(\d+).*$', bucks_data)
        bucks_num = bucks_res[0] if len(bucks_res) > 0 else 0

        # kings国王专区
        kings = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="basketball"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "kings")]/../span/text()').extract()
        kings_data = kings[0] if len(kings) > 0 else ''
        kings_res = re.findall(r'.(\d+).*$', kings_data)
        kings_num = kings_res[0] if len(kings_res) > 0 else 0

        # raptors猛龙专区
        raptors = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="basketball"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "raptors")]/../span/text()').extract()
        raptors_data = raptors[0] if len(raptors) > 0 else ''
        raptors_res = re.findall(r'.(\d+).*$', raptors_data)
        raptors_num = raptors_res[0] if len(raptors_res) > 0 else 0

        # nuggets掘金专区
        nuggets = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="basketball"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "nuggets")]/../span/text()').extract()
        nuggets_data = nuggets[0] if len(nuggets) > 0 else ''
        nuggets_res = re.findall(r'.(\d+).*$', nuggets_data)
        nuggets_num = nuggets_res[0] if len(nuggets_res) > 0 else 0

        # hawks老鹰专区
        hawks = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="basketball"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "hawks")]/../span/text()').extract()
        hawks_data = hawks[0] if len(hawks) > 0 else ''
        hawks_res = re.findall(r'.(\d+).*$', hawks_data)
        hawks_num = hawks_res[0] if len(hawks_res) > 0 else 0

        # hornets黄蜂专区
        hornets = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="basketball"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "hornets")]/../span/text()').extract()
        hornets_data = hornets[0] if len(hornets) > 0 else ''
        hornets_res = re.findall(r'.(\d+).*$', hornets_data)
        hornets_num = hornets_res[0] if len(hornets_res) > 0 else 0

        # pistons活塞专区
        pistons = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="basketball"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "pistons")]/../span/text()').extract()
        pistons_data = pistons[0] if len(pistons) > 0 else ''
        pistons_res = re.findall(r'.(\d+).*$', pistons_data)
        pistons_num = pistons_res[0] if len(pistons_res) > 0 else 0

        # lurenwang路人王专区
        lurenwang = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="basketball"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "lurenwang")]/../span/text()').extract()
        lurenwang_data = lurenwang[0] if len(lurenwang) > 0 else ''
        lurenwang_res = re.findall(r'.(\d+).*$', lurenwang_data)
        lurenwang_num = lurenwang_res[0] if len(lurenwang_res) > 0 else 0

        #  fiba世界篮球-FIBA
        fiba = response.xpath(
            '//div[@id="content"]/div[@class="plate"]/div[@class="plate_03"]/div[@id="basketball"]/div[@class="plate_03_list"]/ul/li/a[contains(@href, "fiba")]/../span/text()').extract()
        fiba_data = fiba[0] if len(fiba) > 0 else ''
        fiba_res = re.findall(r'.(\d+).*$', fiba_data)
        fiba_num = fiba_res[0] if len(fiba_res) > 0 else 0

        logging.log(logging.INFO, 'bxj :' + str(bxj_num) + 'pgq :' + str(pgq_num) + 'shh : ' + str(shh_num) +
                    'fiba :' + str(fiba_num) + 'lurenwang :' + str(lurenwang_num))

        item = OtherItem()
        date_today = time.strftime('%Y%m%d', time.localtime())

        item['bxj'] = {'plate': 'bxj', 'num': bxj_num, 'date': date_today}
        item['pgq'] = {'plate': 'pgq', 'num': pgq_num, 'date': date_today}
        item['itsm'] = {'plate': 'itsm', 'num': itsm_num, 'date': date_today}
        item['xfl'] = {'plate': 'xfl', 'num': xfl_num, 'date': date_today}
        item['selfie'] = {'plate': 'selfie', 'num': selfie_num, 'date': date_today}
        item['nine999'] = {'plate': 'nine999', 'num': nine999_num, 'date': date_today}
        item['ent'] = {'plate': 'ent', 'num': ent_num, 'date': date_today}
        item['cars'] = {'plate': 'cars', 'num': cars_num, 'date': date_today}
        item['acg'] = {'plate': 'acg', 'num': acg_num, 'date': date_today}
        item['finance'] = {'plate': 'finance', 'num': finance_num, 'date': date_today}
        item['muisc'] = {'plate': 'muisc', 'num': muisc_num, 'date': date_today}
        item['literature'] = {'plate': 'literature', 'num': literature_num, 'date': date_today}
        item['love'] = {'plate': 'love', 'num': love_num, 'date': date_today}
        item['hccares'] = {'plate': 'hccares', 'num': hccares_num, 'date': date_today}
        item['fit'] = {'plate': 'fit', 'num': fit_num, 'date': date_today}
        item['shh'] = {'plate': 'shh', 'num': shh_num, 'date': date_today}
        item['nba_draft_ncaa'] = {'plate': 'nba_draft_ncaa', 'num': nba_draft_ncaa_num, 'date': date_today}
        item['nba'] = {'plate': 'nba', 'num': nba_num, 'date': date_today}
        item['four832'] = {'plate': 'four832', 'num': four832_num, 'date': date_today}
        item['dailyfantasy'] = {'plate': 'dailyfantasy', 'num': dailyfantasy_num, 'date': date_today}
        item['rockets'] = {'plate': 'rockets', 'num': rockets_num, 'date': date_today}
        item['warriors'] = {'plate': 'warriors', 'num': warriors_num, 'date': date_today}
        item['cavaliers'] = {'plate': 'cavaliers', 'num': cavaliers_num, 'date': date_today}
        item['spurs'] = {'plate': 'spurs', 'num': spurs_num, 'date': date_today}
        item['lakers'] = {'plate': 'lakers', 'num': lakers_num, 'date': date_today}
        item['celtics'] = {'plate': 'celtics', 'num': celtics_num, 'date': date_today}
        item['thunder'] = {'plate': 'thunder', 'num': thunder_num, 'date': date_today}
        item['clippers'] = {'plate': 'clippers', 'num': clippers_num, 'date': date_today}
        item['timberwolves'] = {'plate': 'timberwolves', 'num': timberwolves_num, 'date': date_today}
        item['mavericks'] = {'plate': 'mavericks', 'num': mavericks_num, 'date': date_today}
        item['knicks'] = {'plate': 'knicks', 'num': knicks_num, 'date': date_today}
        item['bulls'] = {'plate': 'bulls', 'num': bulls_num, 'date': date_today}
        item['sixers'] = {'plate': 'sixers', 'num': sixers_num, 'date': date_today}
        item['nets'] = {'plate': 'nets', 'num': nets_num, 'date': date_today}
        item['jazz'] = {'plate': 'jazz', 'num': jazz_num, 'date': date_today}
        item['pacers'] = {'plate': 'pacers', 'num': pacers_num, 'date': date_today}
        item['blazers'] = {'plate': 'blazers', 'num': blazers_num, 'date': date_today}
        item['heat'] = {'plate': 'heat', 'num': heat_num, 'date': date_today}
        item['suns'] = {'plate': 'suns', 'num': suns_num, 'date': date_today}
        item['grizzlies'] = {'plate': 'grizzlies', 'num': grizzlies_num, 'date': date_today}
        item['wizards'] = {'plate': 'wizards', 'num': wizards_num, 'date': date_today}
        item['magic'] = {'plate': 'magic', 'num': magic_num, 'date': date_today}
        item['pelicans'] = {'plate': 'pelicans', 'num': pelicans_num, 'date': date_today}
        item['bucks'] = {'plate': 'bucks', 'num': bucks_num, 'date': date_today}
        item['kings'] = {'plate': 'kings', 'num': kings_num, 'date': date_today}
        item['raptors'] = {'plate': 'raptors', 'num': raptors_num, 'date': date_today}
        item['nuggets'] = {'plate': 'nuggets', 'num': nuggets_num, 'date': date_today}
        item['hawks'] = {'plate': 'hawks', 'num': hawks_num, 'date': date_today}
        item['hornets'] = {'plate': 'hornets', 'num': hornets_num, 'date': date_today}
        item['pistons'] = {'plate': 'pistons', 'num': pistons_num, 'date': date_today}
        item['lurenwang'] = {'plate': 'lurenwang', 'num': lurenwang_num, 'date': date_today}
        item['fiba'] = {'plate': 'fiba', 'num': fiba_num, 'date': date_today}

        # esports 电竞数据, 直接调用的接口了-。-
        esports_data_url = 'https://bbs.hupu.com/get_nav?fup=234'
        yield scrapy.Request(esports_data_url, meta={'item': item}, callback=self.esports_data_parse, cookies=self.cookie_dict)
        yield item

    def esports_data_parse(self, response):
        # inspect_response(response, self)
        item = response.meta['item']
        logging.log(logging.INFO, json.loads(response.body))

        json_data = json.loads(response.body)

        data = json_data['data'] if json_data['status'] and len(json_data['data']) > 0 else []

        date_today = time.strftime('%Y%m%d', time.localtime())
        for value in data:
            if value['fname'] == '王者荣耀':
                item['wzry'] = {'plate':'wzry', 'num':value['tpostnum'], 'date':date_today}
            if value['fname'] == '英雄联盟':
                item['lol'] = {'plate': 'lol', 'num': value['tpostnum'], 'date': date_today}
            if value['fname'] == '绝地求生':
                item['pubg'] = {'plate': 'pubg', 'num': value['tpostnum'], 'date': date_today}
            if value['fname'] == '光荣使命':
                item['grsm'] = {'plate': 'grsm', 'num': value['tpostnum'], 'date': date_today}
            if value['fname'] == '终结者2':
                item['zjz2'] = {'plate': 'zjz2', 'num': value['tpostnum'], 'date': date_today}
            if value['fname'] == '全军出击':
                item['pubgm'] = {'plate': 'pubgm', 'num': value['tpostnum'], 'date': date_today}
            if value['fname'] == '刺激战场':
                item['cjzc'] = {'plate': 'cjzc', 'num': value['tpostnum'], 'date': date_today}
            if value['fname'] == 'QGhappy专区':
                item['qghappy'] = {'plate': 'qghappy', 'num': value['tpostnum'], 'date': date_today}
            if value['fname'] == '刀塔':
                item['dota2'] = {'plate': 'dota2', 'num': value['tpostnum'], 'date': date_today}
            if value['fname'] == '炉石传说':
                item['hs'] = {'plate': 'hs', 'num': value['tpostnum'], 'date': date_today}
            if value['fname'] == '守望先锋':
                item['ow'] = {'plate': 'ow', 'num': value['tpostnum'], 'date': date_today}
        yield item
