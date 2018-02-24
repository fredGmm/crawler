#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
# import urllib.robotparser
# rp = urllib.robotparser.RobotFileParser()
# rp.set_url('http://example.webscraping.com/robots.txt')
# print(rp.read())

# 匹配url中 论坛模块名
# str = 'https://bbs.hupu.com/bxj'
# str2 = 'https://bbs.hupu.com/bxj-3'
# print(re.findall(r'bbs.hupu.com/(\w+){0,4}-?\d*',str2)[0])

# s = '1609卡路里'
# print(re.findall(r'^(\d+).*$', s))

# s = '主题 (8),收藏 (1)'
# print(re.findall(r'^.*主题 \((\d+)\)', s))
# print(re.findall(r'^.*回帖 \((\d+)\)', s))
# print(re.findall(r'^.*收藏 \((\d+)\)$', s))

# s = '关注62个人»'
# print(re.findall(r'.(\d+).*$', s))

# list = ['性别：']
#
# if len(list) > 0:
#     print(list[1] if len(list)>1 and '性别w' in list[0] else '保密')

# s = '\n        认证信息：虎扑官方帐号\xa0所属社团：认证用户社区声望：159573\n    \t社区等级：20\n    在线时间：1424小时    加入时间：2004-01-01\n        上次登录：2018-02-01\n    自我介绍：\n客服QQ公众号：800021359\n客服微信公众号：hupu2004'
#
# print(re.findall(r'.社区声望.(\d+)\n.*', s)[0])

s = '今日21207帖'
print(re.findall(r'.(\d+).*$', s))
