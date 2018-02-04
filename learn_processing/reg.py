#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import urllib.robotparser
rp = urllib.robotparser.RobotFileParser()
rp.set_url('http://example.webscraping.com/robots.txt')
print(rp.read())