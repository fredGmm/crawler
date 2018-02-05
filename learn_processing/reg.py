#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
# import urllib.robotparser
# rp = urllib.robotparser.RobotFileParser()
# rp.set_url('http://example.webscraping.com/robots.txt')
# print(rp.read())

# 匹配url中 论坛模块名
str = 'https://bbs.hupu.com/bxj'
str2 = 'https://bbs.hupu.com/bxj-3'
print(re.findall(r'bbs.hupu.com/(\w+){0,4}-?\d*',str2)[0])

