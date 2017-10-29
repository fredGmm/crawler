#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from selenium import webdriver

# http://wts.peopleyuqing.com/wechat/search.articles?keyword=19&page=1&rankType=0&sdate=0&edate=0&_=1509207206471
driver = webdriver.Chrome('C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe')

driver.get('http://www.baidu.com/')
driver.find_element_by_id('kw').send_keys('php')

driver.find_element_by_id('su').click()
driver.implicitly_wait(30)

ass = driver.find_element_by_css_selector('#content_left')
# print([art.text for art in ass])
print(ass.text)
driver.close()