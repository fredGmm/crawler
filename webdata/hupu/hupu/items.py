# -*- coding: utf-8 -*-

import scrapy

# hupu 帖子相关信息
class HupuItem(scrapy.Item):
    # define the fields for your item here like:
    article_id = scrapy.Field()
    article_plate = scrapy.Field()
    title = scrapy.Field()
    author_name = scrapy.Field()
    author_id = scrapy.Field()
    post_time = scrapy.Field()
    comment_num = scrapy.Field()
    browse_num = scrapy.Field()

    article_content = scrapy.Field()
    all_images = scrapy.Field()
    article_post_time = scrapy.Field()
    highlights_re = scrapy.Field()
    uid = scrapy.Field()

    post_hour = scrapy.Field()
    post_from = scrapy.Field()

# 高亮回复 相关信息
class CommentItem(scrapy.Item):
    comment_id = scrapy.Field()
    article_id = scrapy.Field()
    comment_username = scrapy.Field()
    comment_images = scrapy.Field()
    comment_create_time = scrapy.Field()
    comment_uid = scrapy.Field()
    comment_content = scrapy.Field()
    highlights_num = scrapy.Field()
    article_post_time = scrapy.Field()

# 用户相关信息
class UserItem(scrapy.Item):
    user_id = scrapy.Field()
    user_name = scrapy.Field()
    gender = scrapy.Field()
    bbs_reputation = scrapy.Field()
    bbs_level = scrapy.Field()
    associations = scrapy.Field()
    hupu_property = scrapy.Field()
    online_time = scrapy.Field()
    reg_time = scrapy.Field()
    last_login = scrapy.Field()
    self_introduction = scrapy.Field()
    favorite_sport = scrapy.Field()
    favorite_league = scrapy.Field()
    favorite_team = scrapy.Field()

    # 后期补充的属性
    visit_num = scrapy.Field()
    follower_num = scrapy.Field()
    followering_num = scrapy.Field()
    topic_num = scrapy.Field()
    re_topic_num = scrapy.Field()
    collect_num = scrapy.Field()


class OtherItem(scrapy.Item):
    bxj = scrapy.Field()
    pgq = scrapy.Field()
    itsm = scrapy.Field()
    xfl = scrapy.Field()
    selfie = scrapy.Field()
    nine999 = scrapy.Field()
    ent = scrapy.Field()
    cars = scrapy.Field()
    acg = scrapy.Field()
    finance = scrapy.Field()
    muisc = scrapy.Field()
    literature = scrapy.Field()
    love = scrapy.Field()
    hccares = scrapy.Field()
    fit = scrapy.Field()
    shh = scrapy.Field()
    nba_draft_ncaa = scrapy.Field()
    nba = scrapy.Field()
    four832 = scrapy.Field()
    dailyfantasy = scrapy.Field()
    rockets = scrapy.Field()
    warriors = scrapy.Field()
    cavaliers = scrapy.Field()
    spurs = scrapy.Field()
    lakers = scrapy.Field()
    celtics = scrapy.Field()
    thunder = scrapy.Field()
    clippers = scrapy.Field()
    timberwolves = scrapy.Field()
    mavericks = scrapy.Field()
    knicks = scrapy.Field()
    bulls = scrapy.Field()
    sixers = scrapy.Field()
    nets = scrapy.Field()
    jazz = scrapy.Field()
    pacers = scrapy.Field()
    blazers = scrapy.Field()
    heat = scrapy.Field()
    suns = scrapy.Field()
    grizzlies = scrapy.Field()
    wizards = scrapy.Field()
    magic = scrapy.Field()
    pelicans = scrapy.Field()
    bucks = scrapy.Field()
    kings = scrapy.Field()
    raptors = scrapy.Field()
    nuggets = scrapy.Field()
    hawks = scrapy.Field()
    hornets = scrapy.Field()
    pistons = scrapy.Field()
    lurenwang = scrapy.Field()
    fiba = scrapy.Field()

    # 电竞
    wzry = scrapy.Field()
    lol = scrapy.Field()
    pubg = scrapy.Field()
    grsm = scrapy.Field()
    zjz2 = scrapy.Field()
    pubgm = scrapy.Field()
    cjzc = scrapy.Field()
    qghappy = scrapy.Field()
    dota2 = scrapy.Field()
    hs = scrapy.Field()
    ow = scrapy.Field()



